let currentLetterElement = null;
let chordData = {}; // Object to store chords for each position

// List of chords to display in the grid (you can add more chords as needed)
const chords = ['Am', 'Em', 'C', 'G', 'D', 'F', 'A', 'E', 'B', 'Dm', 'Bm', 'G7', 'Cmaj7', 'A7', 'D7', '+'];

// Function to generate lyrics with clickable letters
function generateLyrics() {
    const inputText = document.getElementById("lyrics-input").value.trim();

    // Check if input is empty
    if (inputText === '') {
        alert("Please provide some lyrics first.");
        return;
    }

    // Process the text to break it into clickable letters
    const lyricsContainer = document.getElementById("lyrics-container");
    lyricsContainer.innerHTML = ''; // Clear previous content

    // Convert the input text into clickable spans for each letter
    for (let i = 0; i < inputText.length; i++) {
        const letter = inputText[i];

        // Skip non-Hebrew characters or space for now
        if (letter === ' ' || !/[\u0590-\u05FF]/.test(letter)) {
            lyricsContainer.innerHTML += letter;
        } else {
            const letterSpan = document.createElement('span');
            letterSpan.classList.add('letter');
            letterSpan.textContent = letter;
            letterSpan.setAttribute('data-index', i); // Store index for easy reference
            lyricsContainer.appendChild(letterSpan);
        }
    }

    // Load existing chords from localStorage if available
    loadChords();
}

// Use event delegation to handle clicks on any letter span
document.getElementById('lyrics-container').addEventListener('click', function(event) {
    // Check if the clicked element is a letter span
    if (event.target && event.target.classList.contains('letter')) {
        showChordPopup(event);
    }
});

// Show the popup for selecting a chord
function showChordPopup(event) {
    console.log("Letter clicked", event.target.textContent); // Debugging click event
    currentLetterElement = event.target;
    const letterIndex = currentLetterElement.getAttribute('data-index');

    // If there's an existing chord, select it in the grid
    const existingChord = chordData[letterIndex] || '';

    // Get the popup element and its content
    const popup = document.getElementById('chord-popup');
    const popupContent = document.querySelector('.popup-content');

    // Clear previous grid and add buttons for each chord
    popupContent.innerHTML = ''; // Clear existing buttons

    // Add buttons for each chord
    chords.forEach(chord => {
        const button = document.createElement('button');
        button.textContent = chord;
        button.onclick = function () {
            if (chord == '+') {
                chord = prompt("Enter custom:");
            }
            addChord(chord); // Add chord on button click
            closePopup(); // Close the popup
        };
        popupContent.appendChild(button);
    });

    // Display the popup
    popup.style.display = 'block';

    // Add class to prevent body scrolling when popup is open
    document.body.classList.add('popup-open');
}

// Function to close the popup
function closePopup() {
    // Get the popup element and hide it
    const popup = document.getElementById('chord-popup');
    popup.style.display = 'none';

    // Remove the class from the body to allow scrolling again
    document.body.classList.remove('popup-open');
    currentLetterElement = null;

}



// Add the selected chord and save it
function addChord(chord) {
    const letterIndex = currentLetterElement.getAttribute('data-index');
    
    // Save the chord data for this letter position
    chordData[letterIndex] = chord;

    // Insert the chord in the lyrics after the letter
    const chordSpan = document.createElement('span');
    chordSpan.classList.add('chord');
    chordSpan.textContent = `[${chord}]`; // Display the chord in brackets
    currentLetterElement.insertAdjacentElement('afterend', chordSpan);

    // Save the chords to localStorage
    saveChords();
}
// Save the chords to localStorage
function saveChords() {
    localStorage.setItem('chords', JSON.stringify(chordData));
}

// Load chords from localStorage
function loadChords() {
    const storedChords = localStorage.getItem('chords');
    if (storedChords) {
        chordData = JSON.parse(storedChords);
    }
}

function bakeLyrics() {
    const lyricsContainer = document.getElementById('lyrics-container');

    // Get all the text from the container, preserving spaces and newlines
    let lyricsWithChords = '';

    // Function to recursively process child elements and preserve newlines
    function extractText(node) {
        if (node.nodeType === 3) { // Text node
            return node.textContent; // Return the text content as is
        }
        if (node.nodeType === 1) { // Element node
            let text = '';
            if (node.nodeName === 'BR') {
                text += '\n'; // Convert <br> to newline
            } else if (node.nodeName === 'P' || node.nodeName === 'DIV') {
                text += '\n'; // Add newline before block-level elements
            }
            // Recursively handle child nodes
            for (let child of node.childNodes) {
                text += extractText(child);
            }
            if (node.nodeName === 'P' || node.nodeName === 'DIV') {
                text += '\n'; // Add newline after block-level elements
            }
            return text;
        }
        return '';
    }

    // Extract all text from the lyrics-container and preserve formatting
    lyricsWithChords = extractText(lyricsContainer);

    // Now send this preserved text to the Flask backend
    fetch('/process-lyrics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lyrics: lyricsWithChords })
    })
    .then(response => response.blob())
    .then(blob => {
        // Trigger the download of the baked file
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'baked_lyrics.txt'; // Download filename
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error baking lyrics:', error);
    });
}

