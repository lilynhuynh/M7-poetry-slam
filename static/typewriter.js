/* Typewriter animation effect provided by Geoof Graham
 * https://css-tricks.com/snippets/css/typewriter-effect/
 */

document.getElementById("generatePoem").addEventListener("click", callGeneratePoem);
// set up text to print, each item in array is new line
var aText = [];
var iSpeed = 100; // time delay of print out
var iIndex = 0; // start printing array at this posision
var iScrollAt = 20; // start scrolling up at this many lines
var iTextPos = 0; // initialise text position
var sContents = ''; // initialise contents variable
var iRow; // initialise current row
var iArrLength = 0; // the length of the text array

function callGeneratePoem() {
    console.log("Clicked generate poem!")
    var destination = document.getElementById("poem-generation");
    destination.innerHTML = "Generating poem..."

    fetch("http://127.0.0.1:5000/generate-poem", {
        method: "GET"
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            return response.json()
        })
        .then(data => {
            console.log("Poem received!", data)

            // Populate aText with the poem
            aText = Object.values(data)
            aText.push("")
            iIndex = 0; // Reset the typewriter position
            iTextPos = 0;
            iArrLength = aText[0].length

            // Clear the "Generating poem..." message
            destination.innerHTML = "";
            console.log("Transformed poem:", aText)

            // Start the typewriter effect
            typewriter();
        })
        .catch(error => {
            console.error("Error fetching poem:", error);
            destination.innerHTML = "Failed to generate poem. Please try again.";
        });
}

function typewriter() {
    sContents = ' ';
    iRow = Math.max(0, iIndex - iScrollAt);
    var destination = document.getElementById("poem-generation");

    while (iRow < iIndex) {
        sContents += aText[iRow++] + '<br /><br />';
    }
    destination.innerHTML = sContents + aText[iIndex].substring(0, iTextPos) + "_";
    if (iTextPos++ == iArrLength) {
        iTextPos = 0;
        iIndex++;
        if (iIndex != aText.length) {
            iArrLength = aText[iIndex].length;
            setTimeout("typewriter()", 500);
        }
    } else {
        setTimeout("typewriter()", iSpeed);
    }
}