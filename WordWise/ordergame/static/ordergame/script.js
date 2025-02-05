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

    console.log(words);

    const wordLine = document.getElementById("word-line");

    words.forEach(word => {
        const wordBlock = document.createElement("div");
        wordBlock.classList.add("word-block");
        wordBlock.textContent = word;
        wordLine.appendChild(wordBlock);

        wordBlock.addEventListener('click', function(){
            moveToSentence(word, wordBlock);
        });
    });

    function moveToSentence(text, element) {
        element.remove();
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

    //OK Button Part
    const check_button = document.getElementById("check-btn")
    check_button.addEventListener('click', function(){
        const usrSenElem = document.getElementById("blank-blocks").children;
        var finalSen = ""
        for(let word of usrSenElem){
            finalSen += word.textContent;
        }
        console.log(finalSen);
    });
});
