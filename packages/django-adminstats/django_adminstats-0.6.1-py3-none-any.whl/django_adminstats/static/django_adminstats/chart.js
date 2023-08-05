document.addEventListener('DOMContentLoaded', function() {
    var content = document.getElementById('content-main');
    var chartElement = document.createElement('div');
    chartElement.id = 'chart';
    content.insertBefore(chartElement, content.firstChild);
    var dataElement = document.getElementById('chart-data');
    // set up axis
    var axisCells = dataElement.querySelectorAll('#chart-axis th');
    var axixRow = ['_axis'];
    for (var idx = 0; idx < axisCells.length; idx++) {
        axixRow.push(axisCells[idx].dataset.value);
    }
    var columns = [axixRow];
    var lines = dataElement.querySelectorAll('.chart-line');
    for (var idx = 0; idx < lines.length; idx++) {
        var label = lines[idx].querySelector('th');
        var cells = lines[idx].querySelectorAll('td');
        var row = [label.textContent];
        for (var jdx = 0; jdx < cells.length; jdx++) {
            row.push(cells[jdx].textContent);
        }
        columns.push(row);
    }
    var chart = c3.generate({
        bindto: chartElement,
        data: {
            x: '_axis',
            columns: columns,
            type: dataElement.dataset.chartType,
        },
        axis: {
            x: {
                type: 'timeseries',
                label: { text: 'Time'}
            }
        }
    });
});
