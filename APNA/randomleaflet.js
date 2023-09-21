// Process quotes csv
function displayRandomQuote(csvData) {
    var lines = csvData.split("\n");
    // Iterate through each line of the CSV leaving the header
    lines = lines.slice(1, lines.length);
  
    var randomIndex = Math.floor(Math.random() * lines.length);
    var randomurl = lines[randomIndex].trim();

    console.log(lines.length)

    document.getElementById("apna-url").src = randomurl.split(',')[4];
  }

// Read and parse the CSV file
function loadleafletCSV() {
    fetch("APNA_URLs.csv")
      .then(function(response) {
        if (response.ok) {
          return response.text();
        }
        throw new Error("Error: " + response.status);
      })
      .then(function(csvData) {
        console.log(csvData)
        displayRandomQuote(csvData);
      })
      .catch(function(error) {
        console.log(error);
      });
}

// Display a random quote when the page loads
loadleafletCSV();