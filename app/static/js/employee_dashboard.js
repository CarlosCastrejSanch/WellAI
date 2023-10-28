
const mySelect = document.getElementById('time-select2');

mySelect.addEventListener('change', () => {
    const selectedValue = mySelect.value;
    const employee_id = document.getElementById('employee_id').value;
    $.ajax({
    type: 'POST',
    url: `/filter_by_employee`,
    data: { employee_id: employee_id, time:selectedValue },
    success: function(response) {
        // Update the line chart with the filtered data
        var data = response;
        var categories = [...new Set(data.map(item => item.category))];
        var dates = [...new Set(data.map(item => item.date))];
        var values = [...new Set(data.map(item => item.value))];

        // Prepare data for sub-bar charts
        var subChartData = {};
        categories.forEach(function(category) {
            subChartData[category] = {};
            dates.forEach(function(date) {
                subChartData[category][date] = {};
                values.forEach(function(value) {
                    subChartData[category][date][value] = 0;
                });
            });
        });

        // Calculate data for sub-bar charts
        data.forEach(function(item) {
            subChartData[item.category][item.date][item.value]++;
        });

        // Prepare data for main chart
        var myChartData = {
            labels: categories,
            datasets: []
        };

        values.forEach(function(value, index) {
            var dataset = {
                label: value,
                data: [],
                backgroundColor: generateColor(index), // Generate unique color for each dataset
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                hoverBackgroundColor: 'rgba(54, 162, 235, 0.7)',
                hoverBorderColor: 'rgba(54, 162, 235, 1)',
                barPercentage: 0.5
            };

            categories.forEach(function(category) {
                var count = 0;
                dates.forEach(function(date) {
                    count += subChartData[category][date][value];
                });
                dataset.data.push(count);
            });

            myChartData.datasets.push(dataset);
        });


        myChart.data = myChartData;
        myChart.update();
    },
    error: function(error) {
        console.log(error);
    }
});


});
