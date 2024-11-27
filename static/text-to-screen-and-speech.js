/*
CSCI 3725 Computational Creativity
M7 Poetry Slam

This file consists of the JavaScript encoding of the typewriter effect by
Geoff Graham (reference README for more details) and text-to-speech feature.
This file calls for the poem.py whenever the button is clicked and fetches
the poem data once finished generating to execute the typewriter and
text-to-speech feature on the poem data.

Authors: Lily Huynh
Last Updated: November 26, 2024

Bugs:
- If you do not have text-to-speech available on your browser, the feature
  will not work.
*/

// Calls callGeneratePoem() when the button is clicked on index.html
generateButton = document.getElementById("generatePoem");
generateButton.addEventListener("click", callGeneratePoem);

// Initializes the variables used for "text-to-screen-and-speech" features
var poemData = []; // Poem data fetched from poem.py
var iSpeed = 200; // Time delay of print out
var iIndex = 0; // Start printing array at this posision
var iScrollAt = 20; // Start scrolling up at this many lines
var iTextPos = 0; // Initialise text position
var sContents = ''; // Initialise contents variable
var iRow; // Initialise current row
var iArrLength = 0; // The length of the text array
var typewriterGenerated = false; // Boolean for recitePoem() is called once

// Initializes speechSynthesis (if available) to load voices
if ('speechSynthesis' in window) {
    speechSynthesis.onvoiceschanged = () => {
        voices = window.speechSynthesis.getVoices();
    };
}

/*
This function fetches the link to "generate-poem" within __init__.py to
interact with poem.py and its associated classes. Once (and if) the poem has
finished generating, its data is fetched in json format to be used when
iterating within typewriter() and recitePoem().
*/
function callGeneratePoem() {
    console.log("Clicked generate poem!")
    console.log("Check out the poem generation process in the terminal!")
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
            // Populate poemData with the recieved poem
            poemData = Object.values(data)
            poemData.push("") // Adds extra line to notify end of poem
            iIndex = 0; // Reset the typewriter position
            iTextPos = 0;
            iArrLength = poemData[0].length

            // Clear the "Generating poem..." message
            destination.innerHTML = "";

            // Start the typewriter effect
            typewriterGenerated = false
            typewriter();
        })
        .catch(error => {
            console.error("Error fetching poem:", error);
            destination.innerHTML = "Failed to generate poem. Please try again.";
        });
}

/*
Typewriter effect where each line is read and then each of its characters
are populated onto the innerHTML with a "_" after to emulate a keyboard
writing the text onto the screen. It also calls the recitePoem() function
if the boolean is still false, meaning the it has not be called yet.
*/
function typewriter() {
    sContents = ' ';
    iRow = Math.max(0, iIndex - iScrollAt);
    var destination = document.getElementById("poem-generation");

    while (iRow < iIndex) {
        sContents += poemData[iRow++] + '<br /><br />';
    }
    destination.innerHTML = sContents + poemData[iIndex].substring(0, iTextPos) + "_";

    if (typewriterGenerated == false) {
        typewriterGenerated = true;
        recitePoem();
    }

    if (iTextPos++ == iArrLength) {
        iTextPos = 0;
        iIndex++;
        if (iIndex != poemData.length) {
            iArrLength = poemData[iIndex].length;
            setTimeout("typewriter()", 300);
        }
    } else {
        setTimeout("typewriter()", iSpeed);
    }
}

/*
This function uses the loaded voices from speechSyntehsis (if available)
and joins the poem data receieved by periods for the voice to "speak" and
pause after each sentence. The voice is currently set to "Good News".
*/
function recitePoem() {
    if ('speechSynthesis' in window) {
        // Double check if voices have been loaded
        if (voices.length === 0) {
            voices = window.speechSynthesis.getVoices();
        }
        var recite = new SpeechSynthesisUtterance(poemData.join(". "));
        recite.pitch = 1.0;
        recite.rate = 0.5;
        recite.volume = 1.0;
        recite.voice = voices[51];
        window.speechSynthesis.speak(recite);
    } else {
        console.log("Text-to-speech is not supported.")
    }
}