// Array to store cities CSV data
var rows = [];
// Function to parse CSV data
function parseCSV(csvData) {
    var selectBox = document.getElementById("citySelect");

    var lines = csvData.split("\n");
    var options = "";

    // Iterate through each line of the CSV
    for (var i = 0; i < lines.length; i++) {
    var line = lines[i].trim();
    

    // Add an option for each city
    if (line != "") {
        var city = line.trim().split(',')[0];
        options += '<option value="' + city + '">' + capitalizeFirstLetter(city) + '</option>';
        rows.push(line.trim())
    }
    }

    // Set the options in the select box
    document.getElementById("citySelect").innerHTML = options;

    //Preselct
    //document.getElementById("citySelect").selectedIndex = "0"
}

// Read and parse the CSV file
function loadCSV() {
    fetch("data/cities.csv")
      .then(function(response) {
        if (response.ok) {
          return response.text();
        }
        throw new Error("Error: " + response.status);
      })
      .then(function(csvData) {
        console.log(csvData)
        parseCSV(csvData);
      })
      .catch(function(error) {
        console.log(error);
      });
}

// Call the loadCSV function to fetch and populate the select box
loadCSV();

function updateHeading() {
  var cityElement = document.getElementById("citySelect");
  var city_selected = cityElement.value;

  var parameterElement = document.getElementById("parameterSelect");
  var parameter_selected = parameterElement.value;

  var headingElement = document.getElementById("selectedHeading");
  headingElement.textContent = "Air Quality Forecasts : "+city_selected;

  updateURLS(city_selected, parameter_selected);
}

const capitalizeFirstLetter = (inputString = "") => {
    if (inputString === null) {
      return null;
    }
    return inputString.replace(/_/g, " ").replace(/(?:^|\s)\S/g, (a) => a.toUpperCase());
  };

  function getUserLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          var userLat = position.coords.latitude;
          var userLng = position.coords.longitude;
          selectDefaultCity(userLat, userLng);
        },
        error => console.error(error)
      );
    } else {
      console.log("Geolocation is not supported by this browser.");
    }
  }

  // Determine default city based on user's coordinates
  function selectDefaultCity(userLat, userLng) {
    var defaultCity = null;

    for (var i = 0; i < rows.length; i++) {
      var row = rows[i];
      var swLat = parseFloat(row.split(',')[2]);
      var swLng = parseFloat(row.split(',')[1]);
      var neLat = parseFloat(row.split(',')[4]);
      var neLng = parseFloat(row.split(',')[3]);

      if (userLat >= swLat && userLat <= neLat && userLng >= swLng && userLng <= neLng) {
        defaultCity = row.split(',')[0];
        // Preselect in the select box
        document.getElementById("citySelect").selectedIndex = i;
        break;
      }
    }

    if (defaultCity) {
      console.log("Default city: " + defaultCity);
      // Set the default city as the selected value in your HTML form or display it as desired
    } else {
      defaultCity = 'goa'
      console.log("No default city found for user location");
    }

    var headingElement = document.getElementById("selectedHeading");
    headingElement.textContent = "Air Quality Forecasts : "+defaultCity;

    var parameterElement = document.getElementById("parameterSelect");
    var parameter_selected = parameterElement.value;
    updateURLS(defaultCity, parameter_selected);
    
  }

  function updateURLS(city_name, paramater_name) {
    var dailyElement = document.getElementById("daily");
    var timeseriesElement = document.getElementById("timeseries");
    var hourlyElement = document.getElementById("hourly");

    var dailyhrefElement = document.getElementById("daily_href");
    var timeserieshrefElement = document.getElementById("timeseries_href");
    var hourlyhrefElement = document.getElementById("hourly_href");

    if (paramater_name=='precip'){
      dailyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_precip_daysum_1by4.png";
      timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_precip.png";
      hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/animation_precip.mp4";
  
      dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_precip_daysum_1by4.png";
      timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_precip.png";
      hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/animation_precip.mp4";
      
    } else if (paramater_name=='temp2m'){
      dailyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_temp2m_dayngt_2by4.png";
      timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_temp2m.png";
      hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/animation_temp.mp4";
  
      dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_temp2m_dayngt_2by4.png";
      timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_temp2m.png";
      hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/animation_temp.mp4";
  
    } else if (paramater_name =='winds'){
      dailyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_winds_dayngt_2by4.png";
      timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_winds.png";
      hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/animation_winds.mp4";
  
      dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/stitched_winds_dayngt_2by4.png";
      timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_winds.png";
      hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/animation_winds.mp4";
    } else {
      dailyElement.src = "";
      dailyElement.alt = "Not available";
      timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_pblht.png";
      hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_name+"/animation_pblht.mp4";
  
      dailyhrefElement.href = "";
      dailyhrefElement.alt = "";
      timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/timeseries_pblht.png";
      hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_name+"/animation_pblht.mp4";
    }
  
    // Reload the video to reflect the new source
    var video = document.getElementById("animation");
    video.load();
  }