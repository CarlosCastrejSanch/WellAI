const questionSelect = document.getElementById('question-select');
const lastSubmitSelect = document.getElementById('last-submit-select');
const roleSelect = document.getElementById('role-select');
const genderSelect = document.getElementById('gender-select');

questionSelect.addEventListener('change', () => {
    const selectedValue = questionSelect.value;

    $.ajax({
    type: 'POST',
    url: `/filter_by_question`,
    data: { question: selectedValue },
    success: function(response) {
        // Update the line chart with the filtered data
        var data = response;
        var categories = [...new Set(data.map(item => item.category))];
        var dates = [...new Set(data.map(item => item.date))];
        var values = [...new Set(data.map(item => item.value))];
        var scores = [...new Set(data.map(item => item.score))];
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


lastSubmitSelect.addEventListener('change', () => {
    const selectedValue = lastSubmitSelect.value;
    $.ajax({
    type: 'POST',
    url: `/filter_by_last_submit`,
    data: { lastSubmitSelect: selectedValue },
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


roleSelect.addEventListener('change', () => {
    const selectedValue = roleSelect.value;
    $.ajax({
    type: 'POST',
    url: `/filter_by_role`,
    data: { role: selectedValue },
    success: function(response) {
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



genderSelect.addEventListener('change', () => {
    const selectedValue = genderSelect.value;
    $.ajax({
    type: 'POST',
    url: `/filter_by_gender`,
    data: { gender: selectedValue },
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

