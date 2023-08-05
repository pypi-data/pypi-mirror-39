import collections
import typing

import django.core.exceptions
import django.http
import django.urls
from django import forms
from django.contrib.admin.widgets import AutocompleteSelect
from django.views.generic.list import BaseListView
from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from . import models, registry


def add_description(text: str):
    def inner(func: typing.Callable) -> typing.Callable:
        func.short_description = text
        return func
    return inner


@add_description(_('Duplicate'))
def copy_chart(_admin, _request, queryset):
    for chart in queryset:
        new = models.Chart.objects.create(
            title=str(_('Copy of {}')).format(chart.title),
            chart_type=chart.chart_type,
            until_type=chart.until_type,
            until_date=chart.until_date,
            period_count=chart.period_count,
            period_step=chart.period_step,
        )
        for criteria in chart.criteria.all():
            models.Criteria.objects.create(
                chart=new,
                stats_key=criteria.stats_key,
                filter_query=criteria.filter_query,
                group_query=criteria.group_query,
                axis_query=criteria.axis_query,
            )


class QueryAutocompleteJsonView(BaseListView):
    """Handle Widget's AJAX requests for data."""
    paginate_by = 20
    stats_key = ''

    def get(self, request, *args, **kwargs):
        """
        Return a JsonResponse with search results of the form:
        {
            results: [{id: "123" text: "foo"}],
        }
        """
        if not self.has_perm(request):
            return django.http.JsonResponse(
                {'error': '403 Forbidden'}, status=403)

        try:
            reg = registry.REGISTRY[self.stats_key]
        except KeyError:
            return django.http.HttpResponseBadRequest("Invalid stats key")
        term = self.request.GET.get('term', '')
        results = []
        for item in self.get_options(reg, term):
            results.append({'id': item, 'text': item})
        return django.http.JsonResponse({'results': results})

    def get_options(self, reg: registry.Registry, term: str) -> list:
        """Return queryset based on ModelAdmin.get_search_results()."""
        return reg.query_options(term)

    def has_perm(self, request, obj=None):
        """Check if user has permission to access the related model."""
        return request.user.has_perm('django_adminstats.view_chart')


class FilterAutocompleteJsonView(QueryAutocompleteJsonView):
    def get_options(self, reg: registry.Registry, term: str) -> list:
        return reg.query_options(term, is_filter=True)


class QueryAutocomplete(AutocompleteSelect):

    allow_multiple_selected = True
    is_required = False

    def __init__(self):
        super().__init__(None, None)
        self.choices = ()

    def get_url(self):
        return django.urls.reverse(
            'admin:django_adminstats_query_autocomplete', args=[''])

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        subgroup = []
        # just show the existing selected options, everything they can get
        # from select2
        for part in value:
            subgroup.append(self.create_option(
                name, part, part, True, 0,
                subindex=None, attrs=attrs,
            ))
        return [(None, subgroup, 0)]

    def value_omitted_from_data(self, data, files, name):
        # this is required otherwise django won't save blank values
        return False

    def format_value(self, value):
        """Return selected values as a list."""
        if value is None:
            return []
        return [s for s in value.split('&') if s != '']

    def value_from_datadict(self, data, _files, name):
        return '&'.join(data.getlist(name))

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['data-token-separator'] = '&'
        attrs['data-select-on-close'] = 'true'
        attrs['data-ajax--delay'] = '250'
        attrs['class'] = 'adminstats-autocomplete'
        return attrs


class FilterAutocomplete(QueryAutocomplete):

    def get_url(self):
        return django.urls.reverse(
            'admin:django_adminstats_filter_autocomplete', args=[''])


class CriteriaForm(forms.ModelForm):
    stats_key = forms.ChoiceField(choices=registry.REGISTRY.choices())

    class Meta:
        model = models.Criteria
        fields = ['stats_key', 'filter_query', 'group_query', 'axis_query']
        widgets = {
            'filter_query': FilterAutocomplete,
            'group_query': QueryAutocomplete,
            'axis_query': QueryAutocomplete,
        }


class CriteriaInline(admin.TabularInline):
    form = CriteriaForm
    model = models.Criteria
    min_num = 1
    extra = 0


class ChartAdmin(admin.ModelAdmin):
    change_form_template = 'django_adminstats/chart/change_form.html'
    inlines = [CriteriaInline]
    list_display = ('title', 'chart_type', 'show_action_links')
    list_filter = ('chart_type',)
    chart_template = 'django_adminstats/chart/chart.html'
    actions = [copy_chart]

    class Media:
        js = ('django_adminstats/chart_form.js',)
        css = {'all': ('django_adminstats/chart_form.css',)}

    def get_urls(self):
        return [
            url(
                r'^(?P<chart_id>\w+)/chart$',
                self.admin_site.admin_view(self.view_chart),
                name='django_adminstats_chart'),
            url(
               r'^filter_autocomplete/(?P<stats_key>.*)$',
               self.filter_autocomplete_view,
               name='django_adminstats_filter_autocomplete'),
            url(
               r'^query_autocomplete/(?P<stats_key>.*)$',
               self.query_autocomplete_view,
               name='django_adminstats_query_autocomplete'),
            ] + super().get_urls()

    @add_description(_('Actions'))
    def show_action_links(self, obj):
        return format_html(
            '<a href="{url}">{text}</a>',
            text=_('Show Chart'), url='{}/chart'.format(obj.pk))

    @staticmethod
    def query_autocomplete_view(request, stats_key):
        return QueryAutocompleteJsonView.as_view(stats_key=stats_key)(request)

    @staticmethod
    def filter_autocomplete_view(request, stats_key):
        return FilterAutocompleteJsonView.as_view(stats_key=stats_key)(request)

    def view_chart(self, request, chart_id):
        if not self.has_change_permission(request):
            return django.http.HttpResponseForbidden()
        chart = self.get_object(request, chart_id)  # type: models.Chart
        if chart is None:
            return django.http.HttpResponseNotFound()
        if request.method != 'GET':
            return django.http.HttpResponseNotAllowed(('GET',))

        exceptions = []
        chart_header = list(chart.dates())
        chart_rows = collections.OrderedDict()
        for criteria in chart.criteria.all():
            try:
                group_data = registry.REGISTRY.query(criteria)
            except (ValueError, django.core.exceptions.FieldError) as ex:
                exceptions.append(ex)
            else:
                for group, data in group_data.items():
                    row = [0] * len(chart_header)
                    for date, value in data.items():
                        try:
                            date_idx = chart_header.index(date)
                            row[date_idx] = value
                        except ValueError:
                            pass
                    label = registry.REGISTRY[criteria.stats_key].label
                    chart_rows[(label, group)] = row

        context = {
            'title': _('View Chart: %s') % chart.title,
            'media': self.media,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': getattr(self.model, '_meta'),
            'chart': chart,
            'header': chart_header,
            'rows': chart_rows,
            'exceptions': exceptions,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))
        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.chart_template, context)


admin.site.register(models.Chart, ChartAdmin)
