function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}

function filterNotes() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let notes = document.querySelectorAll("#notesList li");

    notes.forEach(note => {
        let text = note.innerText.toLowerCase();
        note.style.display = text.includes(input) ? "" : "none";
    });
}
