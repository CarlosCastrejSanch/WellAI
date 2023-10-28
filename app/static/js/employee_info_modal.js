// Get the modal
var employeeInfoModal = document.getElementById("employeeInfoModal");

// Get the button that opens the modal
var displayInfoBtn = document.getElementById("displayInfoBtn");

// Get the <span> element that closes the modal
var span = document.getElementById("closeInfoModal");
const mySelect = document.getElementById('time-select');
// When the user clicks the button, open the modal 
function showEmployeeInfo(employee_id){
  employeeInfoModal.style.display = "block";

// Display AVG Chart


$.ajax({
    type: 'POST',
    url: `/avg_chart_doctor_employee`,
    data: { employee_id: employee_id },
    success: function(response) {
 // Update the line chart with the filtered data
 var info_dict = response;

 var categories = Object.keys(info_dict);
 var scoreLabels = ["bajo", "normal", "alto", "muy_alto"];

 var datasets = [];
 for (var i = 0; i < scoreLabels.length; i++) {
     var data = [];
     for (var j = 0; j < categories.length; j++) {
         data.push(info_dict[categories[j]][scoreLabels[i]]);
     }

     var dataset = {
         label: scoreLabels[i],
         data: data,
         backgroundColor: getBackgroundColor(i),
         borderColor: getBorderColor(i),
         borderWidth: 1
     };

     datasets.push(dataset);
 }

 var ctx2 = document.getElementById('avgChart').getContext('2d');
 var avgChart = new Chart(ctx2, {
     type: 'bar',
     data: {
         labels: categories,
         datasets: datasets
     },
     options: {
         responsive: true,
         scales: {
             x: {
                 grid: {
                     display: false
                 }
             },
             y: {
                 beginAtZero: true,
                 ticks: {
                     precision: 0
                 }
             }
         }
     }
 });


 function getBackgroundColor(index) {
    var colors = ["rgba(54, 162, 235, 0.6)", "rgba(75, 192, 192, 0.6)", "rgba(255, 206, 86, 0.6)", "rgba(255, 99, 132, 0.6)"];
    return colors[index % colors.length];
}

function getBorderColor(index) {
    var colors = ["rgba(54, 162, 235, 1)", "rgba(75, 192, 192, 1)", "rgba(255, 206, 86, 1)", "rgba(255, 99, 132, 1)"];
    return colors[index % colors.length];
}

avgChart.data = {
    labels: categories,
    datasets: datasets
};
avgChart.update();

console.log(avgChart.data["datasets"])
    },
    error: function(error) {
        console.log(error);
    }
});




// Display Anwers Chart
  $.ajax({
    type: 'POST',
    url: `/filter_by_employee`,
    data: { employee_id: employee_id, time:mySelect.value },
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


mySelect.addEventListener('change', () => {
  const selectedValue = mySelect.value;

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



}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    employeeInfoModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == employeeInfoModal) {
    employeeInfoModal.style.display = "none";
  }
}






mySelect.addEventListener('change', () => {
    const selectedValue = mySelect.value;

    $.ajax({
    type: 'POST',
    url: `/filter_by_employee`,
    data: { time: selectedValue },
    success: function(response) {
 // Update the line chart with the filtered data
 var data = response;
 var dates = [];
 var values = [];
 // Extract unique dates and values
 data.forEach(function(entry) {
     if (!dates.includes(entry.date)) {
         dates.push(entry.date);
     }
     if (!values.includes(entry.value)) {
         values.push(entry.value);
     }
 });
 // Count occurrences for each date-value pair
 var counts = {};
 data.forEach(function(entry) {
     var key = entry.date + '|' + entry.value;
     counts[key] = (counts[key] || 0) + 1;
 });
 // Prepare data for chart
 var chartData = {
     labels: dates,
     datasets: []
 };
 values.forEach(function(value) {
     var dataset = {
         label: value,
         data: [],
         backgroundColor: 'rgba(54, 162, 235, 0.5)' // Set a color for the bars
     };

     dates.forEach(function(date) {
         var key = date + '|' + value;
         dataset.data.push(counts[key] || 0);
     });

     chartData.datasets.push(dataset);
 });



 myChart.data = chartData;
 myChart.update();
    },
    error: function(error) {
        console.log(error);
    }
});




});
