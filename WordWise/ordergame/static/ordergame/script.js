function shuffleWord(words){
    for(let i = words.length - 1; i>=0; i--){
        const rindex = Math.floor(Math.random()*(words.length));//random index from 0 to the length - 1
        [words[i], words[rindex]] = [words[rindex], words[i]];
    }
    return words;
}

document.addEventListener("DOMContentLoaded", function(){
    //Words Part
    let words = sent_data.match(/[\w'-]+|[.?]/g);
    words = shuffleWord(words);
    let clicks = 0;
    let finished = false;

    const wordLine = document.getElementById("word-line");

    //Get modal popup

    const popup = document.getElementById("popup");
    const popupMessage = document.getElementById("popup-message");
    const popupClose = document.getElementById("popup-close");

    words.forEach(word => {
        const wordBlock = document.createElement("div");
        wordBlock.classList.add("word-block");
        wordBlock.textContent = word;
        wordLine.appendChild(wordBlock);

        wordBlock.addEventListener('click', function(){
            moveToSentence(word, wordBlock);
        });
    });

    //Words arrange Part

    function moveToSentence(text, element) {
        element.remove();
        clicks += 1;
        const blankBlocks = document.getElementById("blank-blocks");
        const wordInSen = document.createElement("div");
        wordInSen.classList.add("word-block");
        wordInSen.textContent = text;
        blankBlocks.appendChild(wordInSen);

        wordInSen.addEventListener('click', function(){
            moveToSelector(text, wordInSen);
        });
    }

    function moveToSelector(text, element) {
        element.remove();
        const wordLine = document.getElementById("word-line");
        const wordBlock = document.createElement("div");
        wordBlock.classList.add("word-block");
        wordBlock.textContent = text;
        wordLine.appendChild(wordBlock);
        wordLine.style.visibility = "visible";

        wordBlock.addEventListener('click', function(){
            moveToSentence(text, wordBlock);
            if (wordLine.children.length === 0) {
                wordLine.style.visibility = "hidden";
            }
        });
    }

    // Popup part
    function showPopup(correctness) {
        popup.setAttribute("data-correct", correctness); // Set correctness as attribute
        popupMessage.textContent = correctness ? "✅ Correct!" : "❌ Incorrect. Try again!";
        popupClose.classList = correctness ? "popup-close-pass" : "popup-close-fail";
        popupClose.textContent = correctness ? "Next" : "Retry";
        popup.style.display = "block";
    }

    popupClose.addEventListener("click", function () {
        popup.style.display = "none";
        if (popup.getAttribute("data-correct") === "true") {
            window.location.reload(true);
        }
    });


    //OK Button Part
    const check_button = document.getElementById("check-btn")
    check_button.addEventListener('click', async function(){
        const usrSenElem = document.getElementById("blank-blocks").children;
        var finalSen = ""
        for(let word of usrSenElem){
            finalSen += word.textContent;
        }
        if(finalSen == sent_data.replace(/\s+/g, '')){
            showPopup(correctness=true);
            const score = clicks/usrSenElem.length;
            if(!finished && username){
                try {
                    scoredata = {
                        gamescore : score,
                        sentence : sent_data
                    }
                    const response = await fetch(addscurl, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCSRFToken()
                        },
                        body: JSON.stringify(scoredata)
                    })
                    const result = await response.json()
                    console.log(result.success)
                    finished = true;
                } catch(error) {
                    console.error("Error:", error);
                }
            }
        } else {
            showPopup(correctness=false);
        }
    });
});

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}