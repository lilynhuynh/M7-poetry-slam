/*
CSCI 3725 Computational Creativity
M7 Poetry Slam

This file consists of the JavaScript encoding of the mousehover effect by
Online Tutorial's on YouTube (please reference the README for more details).

Authors: Lily Huynh
Last Updated: November 26, 2024

Bugs:
- No known bugs at the moment
*/

// Initialize the cursor and body DOM elements from index.html
let cursor = document.querySelector("#cursor");
let body = document.querySelector("body");

// Create a event listener for whenever the mouse moves on the browser
document.onmousemove = function(event) {
    // Updates cursor's pixel location on body element
    cursor.style.top = event.pageY + "px";
    cursor.style.left = event.pageX + "px";

    body.style.backgroundPositionX = event.pageX/-4 + "px";
    body.style.backgroundPositionY = event.pageY/-4 + "px";

    let element = document.createElement("div");
    element.className = "element";
    body.prepend(element);

    element.style.left = cursor.getBoundingClientRect().x + "px";
    element.style.top = cursor.getBoundingClientRect().y + "px";

    // Generates random text that floats off cursor
    function randomText() {
        var text = ("abcdefghijklmnopqrstuvwxyz").split("");
        letter = text[Math.floor(Math.random() * text.length)];
        return letter;
    }

    // Timeout function to dissipate random text that floats off cursor
    setTimeout(function() {
        let text = document.querySelectorAll(".element")[0];
        let directionX = Math.random() < .5 ? -1 : 1;
        let directionY = Math.random() < .5 ? -1 : 1;

        text.style.left = parseInt(text.style.left) - (directionX * (Math.random() * 500)) + "px";
        text.style.top = parseInt(text.style.top) - (directionY * (Math.random() * 500)) + "px";
        text.style.opacity = 0;
        text.style.transform = "scale(0.55)";
        text.innerHTML = randomText();

        setTimeout(function() {
            element.remove()
        }, 1000)
    }, 10)

}

