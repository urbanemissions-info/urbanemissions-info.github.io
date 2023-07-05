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
        var city = line.trim();
        options += '<option value="' + city + '">' + capitalizeFirstLetter(city) + '</option>';
    }
    }

    // Set the options in the select box
    document.getElementById("citySelect").innerHTML = options;

    //Preselct
    document.getElementById("citySelect").selectedIndex = "0"


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
  
  var dailyElement = document.getElementById("daily");
  var timeseriesElement = document.getElementById("timeseries");
  var hourlyElement = document.getElementById("hourly");

  var dailyhrefElement = document.getElementById("daily_href");
  var timeserieshrefElement = document.getElementById("timeseries_href");
  var hourlyhrefElement = document.getElementById("hourly_href");
  
  if (parameter_selected=='precip'){
    dailyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_precip_daysum_1by4.png";
    timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_precip.png";
    hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_precip.mp4";

    dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_precip_daysum_1by4.png";
    timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_precip.png";
    hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_precip.mp4";
    
  } else if (parameter_selected=='temp2m'){
    dailyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_temp2m_dayngt_2by4.png";
    timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_temp2m.png";
    hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_temp.mp4";

    dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_temp2m_dayngt_2by4.png";
    timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_temp2m.png";
    hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_temp.mp4";

  } else if (parameter_selected =='winds'){
    dailyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_winds_dayngt_2by4.png";
    timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_winds.png";
    hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_winds.mp4";

    dailyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/stitched_winds_dayngt_2by4.png";
    timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_winds.png";
    hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_winds.mp4";
  } else {
    dailyElement.src = "";
    dailyElement.alt = "Not available";
    timeseriesElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_pblht.png";
    hourlyElement.src = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_pblht.mp4";

    dailyhrefElement.href = "";
    timeserieshrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/timeseries_pblht.png";
    hourlyhrefElement.href = "https://urbanemissions.info/forecasts/"+city_selected+"/animation_pblht.mp4";
  }

  // Reload the video to reflect the new source
  var video = document.getElementById("animation");
  video.load();
  
}

const capitalizeFirstLetter = (inputString = "") => {
    if (inputString === null) {
      return null;
    }
    return inputString.replace(/_/g, " ").replace(/(?:^|\s)\S/g, (a) => a.toUpperCase());
  };