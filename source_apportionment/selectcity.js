
function convertToLowercase(str) {
  return str.toLowerCase();
}

function checkValueInList(value, list) {
  if (list.includes(value)) {
    return true;
  } else {
    return false;
  }
}

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

  var headingElement = document.getElementById("selectedHeading");
  headingElement.textContent = "Source apportionment : "+city_selected;
  
  var apna_href_Element = document.getElementById("apna_href");
  
  var list_2017 = ["Agra", "Amritsar", "Bengaluru", "Bhopal", "Bhubaneshwar", "Chandigarh", "Chennai", "Coimbatore", "Dehradun", "Indore",
                  "Jaipur", "Kanpur", "Kochi", "Ludhiana", "Nagpur", "Patna", "Pune", "Raipur", "Ranchi", "Varanasi"]
  
  var isValueInList = checkValueInList(city_selected, list_2017);
  
  if (isValueInList) {
    apna_href_Element.href = "https://urbanemissions.info/wp-content/uploads/apna/docs/india_apna_"+'2017'+"_"+convertToLowercase(city_selected)+".pdf";
  } else{
    apna_href_Element.href = "https://urbanemissions.info/wp-content/uploads/apna/docs/india_apna_"+'2019'+"_"+convertToLowercase(city_selected)+".pdf";
  }

  
  
  var source_apportionment_Element = document.getElementById("source_apportionment");
  source_apportionment_Element.data = "plots/"+city_selected+"_source_apportionment_pie.svg";

  
}

const capitalizeFirstLetter = (inputString = "") => {
    if (inputString === null) {
      return null;
    }
    return inputString.replace(/_/g, " ").replace(/(?:^|\s)\S/g, (a) => a.toUpperCase());
  };
