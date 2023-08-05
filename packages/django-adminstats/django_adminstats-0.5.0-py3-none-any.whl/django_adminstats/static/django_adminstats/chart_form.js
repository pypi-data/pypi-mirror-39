(function($) {
    function findField(name, fieldType, parent=null) {
        var spec = ('.field-' + name + ' ' + fieldType
                    + ', .grp-row.' + name + ' ' + fieldType);
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function findFieldRow(name, parent=null) {
        var spec = ('.field-' + name + ', .grp-row.' + name);
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function selectUntilType(elem) {
        var opt = elem.options[elem.selectedIndex];
        findFieldRow('until_date').toggle(opt.value == 's');
    }

    function changeStats(origin) {
        var row = origin.parentNode.parentNode;
        var queryFieldNames = ['filter', 'group', 'axis'];
        for (var idx=0; idx<queryFieldNames.length; idx++) {
            var select = row.querySelector(
                '.field-'+queryFieldNames[idx]+'_query select');
            if (select.dataset['ajax-OrigUrl'] == undefined) {
                select.dataset['ajax-OrigUrl'] = select.dataset['ajax-Url'];
            }
            // need to specify a baseURL, but we don't use it
            var url = new URL(select.dataset['ajax-OrigUrl'],
                              'https://example/');
            select.dataset['ajax-Url'] = (url.pathname + origin.value);
            // we need to reinitialize the jquery plugin so it recognizes
            // the new settings
            $(select).djangoAdminSelect2().on("select2:unselecting",
                // work-around for issue #3320 in select2
                function (e) {
                    // make sure we are on the list and not within input box
                    if (e.params._type === 'unselecting') {
                        $(this).val([]).trigger('change');
                        e.preventDefault();
                    }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Hide Until date if Until type is not "Specific Date"
        var untilTypeField = findField('until_type', 'select');
        untilTypeField.on('change', function() {selectUntilType(this)});
        selectUntilType(untilTypeField[0]);
        // go through criteria entries and set up autocomplete URLs
        var criteriaRows = document.querySelectorAll(
            '#criteria-group .form-row');
        for (var idx=0; idx<criteriaRows.length; idx++) {
            var select = criteriaRows[0].querySelector(
                '.field-stats_key select');
            changeStats(select);
            select.addEventListener(
                'change', function(event) { changeStats(this); });
        }

    });
})(django.jQuery)
