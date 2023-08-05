import collections
from datetime import date
from typing import Mapping

import django.db.models.functions as db_functions
from django.contrib.contenttypes.models import ContentType
import django.db.models as db_models


from .qs import QuerySpec

from . import Step


class Registration:

    date_field = 'date'

    def get_queryset(self):
        raise NotImplementedError

    def get_span_queryset(self, start, end, _period_step):
        qs = self.get_queryset().annotate(
            _date_field=db_functions.Cast(self.date_field,
                                          db_models.DateField()))
        kwargs = {'_date_field__gte': start, '_date_field__lt': end}
        return qs.filter(**kwargs)

    def get_x_parameters(self, period_step: Step):
        args = {}
        if period_step == Step.DAY:
            args['date'] = db_functions.TruncDay(
                self.date_field, output_field=db_models.DateField())
            args['month'] = db_functions.TruncMonth(self.date_field)
            args['year'] = db_functions.TruncYear(self.date_field)
        if period_step == Step.MONTH:
            args['date'] = db_functions.TruncMonth(
                self.date_field, output_field=db_models.DateField())
            args['year'] = db_functions.TruncYear(self.date_field)
        if period_step == Step.YEAR:
            args['date'] = db_functions.TruncYear(
                self.date_field, output_field=db_models.DateField())
        return args, 'date'

    def query(self, start: date, end: date,
              period_step: Step, query_spec: QuerySpec):
        qs = self.get_span_queryset(start, end, period_step)
        x_annotations, x_value = self.get_x_parameters(period_step)
        return query_spec.update_queryset(
            qs, x_annotations=x_annotations, x_value=x_value)

    def get_data(self, start: date, end: date,
                 period_step: Step, axis_text: str, group_text: str,
                 filter_text: str) -> Mapping[str, Mapping[date, str]]:
        query_spec = QuerySpec(axis_text=axis_text, group_text=group_text,
                               filter_text=filter_text)
        qs = self.query(start, end, period_step, query_spec)
        result = {}
        group_fields = ['_django_adminstats_group_{}'.format(index)
                        for index in range(len(query_spec.group_parts))]
        axis_fields = ['_django_adminstats_axis_{}'.format(index)
                       for index in range(len(query_spec.axis_parts))]
        for item in qs:
            group_key = ' / '.join(str(item[field]) for field in group_fields)
            value = ' / '.join(str(item[field]) for field in axis_fields)
            if group_key not in result:
                result[group_key] = {}
            result[group_key][item['_django_adminstats_x']] = value
        return result


class Registry(collections.OrderedDict):

    def register(self, reg: Registration):
        self[reg.key] = reg

    def __getitem__(self, key: str) -> Registration:
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: Registration):
        super().__setitem__(key, value)

    def choices(self):
        for key, value in self.items():
            yield key, value.label

    def query(self, criteria):
        stats = self[criteria.stats_key]
        start, end = criteria.chart.span()
        return stats.get_data(start, end, Step(criteria.chart.period_step),
                              criteria.axis_spec, criteria.group_spec,
                              criteria.filter_spec)


class ModelRegistration(Registration):

    def __init__(self, model):
        self.model = model
        self.meta = getattr(self.model, '_meta')
        if not self.meta:
            raise RuntimeError(
                'Model {} is missing Meta class'.format(self.model))

    def get_queryset(self):
        return self.model.objects

    @property
    def key(self):
        return '{}.{}'.format(self.meta.app_label, self.meta.model_name)

    @property
    def label(self):
        return self.meta.verbose_name_plural.title()

    def _filter(self, cls):
        """Given an individual filter token and a model, find the next model"""
        # first check if _meta (model)
        meta = getattr(cls, '_meta', None)
        if meta is not None:
            ff = getattr(meta, '_forward_fields_map', None)
            if ff is not None:
                return ff
            return dict((f.name, f) for f in meta.fields)
        # check if it's a ForeignKey or something
        related = getattr(cls, 'related_model', None)
        if related is not None:
            return self._filter(related)
        raise NotImplementedError

    def filter_options(self, text: str = '') -> set:
        """Given a filter string, return the next options"""
        cls = self.model
        options = self._filter(cls)
        for part in text.split('__'):
            if part in options:
                cls = options[part]
            options = self._filter(cls)
        return set(options.keys())

    def validate_filter(self, text: str):
        cls = self.model
        sub_parts = text.split('__')
        cls = self._filter(sub_parts[0], cls)
        for sub_part in sub_parts[1:]:
            pass
        pass


class MetricRegistration(Registration):

    def __init__(self, metric, model=None):
        # metric is probably a lazy object
        self.metric = metric
        self.model = model
        lazy_func = getattr(metric, '_setupfunc')
        if lazy_func:
            contents = lazy_func.__closure__[1].cell_contents
            self.ref = contents['ref']
            domain = contents['domain']
            lazy_func = getattr(domain, '_setupfunc')
            if lazy_func:
                contents = lazy_func.__closure__[1].cell_contents
                self.domain_ref = contents['ref']
            else:
                self.domain_ref = metric.domain.ref
        else:
            self.ref = metric.ref

    @property
    def key(self):
        if self.model is None:
            return 'trackstats:{}.{}'.format(self.domain_ref, self.ref)
        meta = getattr(self.model, '_meta')
        return 'trackstats:{}.{}:{}'.format(self.domain_ref, self.ref,
                                            meta.label_lower)

    @property
    def label(self):
        return '{} {} Stats'.format(self.domain_ref, self.ref).title()

    def get_queryset(self):
        from trackstats.models import StatisticByDate, StatisticByDateAndObject
        if self.model is None:
            return StatisticByDate.objects.filter(metric=self.metric)
        object_type = ContentType.objects.get_for_model(self.model)
        return StatisticByDateAndObject.objects.filter(
            metric=self.metric, object_type=object_type)

    def get_span_queryset(self, start: date, end: date,
                          period_step: Step):
        from trackstats.models import Period
        kwargs = {self.date_field + '__gte': start,
                  self.date_field + '__lt': end}
        if period_step == Step.DAY:
            kwargs['period'] = Period.DAY
        elif period_step == Step.MONTH:
            kwargs['period'] == Period.MONTH
        else:
            # trackstats doesn't actually support year
            kwargs['period'] = Period.LIFETIME
        return self.get_queryset().filter(**kwargs)

    def get_data(self, start: date, end: date,
                 period_step: Step, axis_text: str, group_text: str,
                 filter_text: str) -> Mapping[str, Mapping[date, str]]:
        if axis_text != '':
            raise ValueError('Axis not supported for tracstats')
        if group_text != '':
            raise ValueError('Group not supported for tracstats')
        return super().get_data(start, end, period_step, 'value',
                                'object_id' if self.model else '', filter_text)


REGISTRY = Registry()


def register(registration: Registration):
    REGISTRY.register(registration)


def register_model(model):
    register(ModelRegistration(model))


def register_metric(metric, cls=None):
    register(MetricRegistration(metric, cls))


def get_registry_ids():
    return REGISTRY.keys()
