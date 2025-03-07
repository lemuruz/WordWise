document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("wordSearch");
    const wordList = document.getElementById("wordList");
    const selectedWordsList = document.getElementById("selectedWordsList");
    const selectedWords = new Set();  // Store selected word IDs

    function renderWordList(query = "") {
        wordList.innerHTML = "";
        const filteredWords = words.filter(word => 
            word.word.toLowerCase().includes(query.toLowerCase()) || 
            word.word_type.toLowerCase().includes(query.toLowerCase())
        ).slice(0, 5);

        filteredWords.forEach(word => {
            if (!selectedWords.has(word.id)) {
                const li = document.createElement("li");
                li.textContent = `${word.word} (${word.word_type})`;
                li.dataset.id = word.id;
                li.addEventListener("click", () => selectWord(word));
                wordList.appendChild(li);
            }
        });
    }

    function selectWord(word) {
        selectedWords.add(word.id);
        renderSelectedWords();
        renderWordList(searchInput.value);
    }

    function removeWord(wordId) {
        selectedWords.delete(wordId);
        renderSelectedWords();
        renderWordList(searchInput.value);
    }

    function renderSelectedWords() {
        selectedWordsList.innerHTML = "";
        selectedWords.forEach(wordId => {
            const word = words.find(w => w.id == wordId);
            const li = document.createElement("li");
            li.textContent = `${word.word} (${word.word_type})`;
            const removeBtn = document.createElement("button");
            removeBtn.textContent = "✖";
            removeBtn.addEventListener("click", () => removeWord(word.id));
            li.appendChild(removeBtn);
            selectedWordsList.appendChild(li);
        });
    }

    searchInput.addEventListener("input", () => {
        renderWordList(searchInput.value);
    });

    document.getElementById("createDeckForm").addEventListener("submit", async function (event) {
        event.preventDefault();

        const deckName = document.getElementById("deckName").value.trim();
        if (!deckName || selectedWords.size === 0) {
            alert("Please enter a deck name and select at least one word.");
            return;
        }

        const requestData = {
            deck_name: deckName,
            words: Array.from(selectedWords)
        };

        try {
            const response = await fetch("/flashcard/createDeck/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify(requestData)
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                document.getElementById("createDeckForm").reset();
                selectedWords.clear();
                renderSelectedWords();
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while creating the deck.");
        }
    });

    function getCSRFToken() {
        return document.cookie
            .split("; ")
            .find(row => row.startsWith("csrftoken="))
            ?.split("=")[1];
    }

    renderWordList();  // Initialize word list on page load
});

async function checkUser() {
    try {
        const response = await fetch("/user/info/");
        
        if (!response.ok) {
            throw new Error("Failed to fetch user info");
        }

        const result = await response.json();
        document.getElementById("user-label").textContent = "Logged in as: " + result.username;

    } catch (error) {
        console.error("Error fetching user info:", error);
        document.getElementById("user-label").textContent = "Not logged in";
    }
}
window.onload = checkUser;