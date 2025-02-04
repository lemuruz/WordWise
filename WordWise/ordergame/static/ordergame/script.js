function shuffleWord(words){
    for(let i = words.length - 1; i>=0; i--){
        const rindex = Math.floor(Math.random()*(words.length));//random index from 0 to the length - 1
        [words[i], words[rindex]] = [words[rindex], words[i]];
    }
    return words;
}

function moveToSentence(text){
    const senLine = document.getElementById("blank-blocks")

    const wordInSen = document.createElement("div");
    wordInSen.classList.add("word-block");
    wordInSen.textContent = text;
    senLine.appendChild(wordInSen);

    wordInSen.addEventListener('click', function(){
        moveToSelector(text);
        wordInSen.remove();
    });
}

function moveToSelector(text){
    const wordLine = document.getElementById("word-line");
    
    const wordBlock = document.createElement("div");
    wordBlock.classList.add("word-block");
    wordBlock.textContent = text;
    wordLine.appendChild(wordBlock);

    wordBlock.addEventListener('click', function(){
        moveToSentence(text);
        wordBlock.remove();
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // Split sentence while keeping punctuation as separate words
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
            moveToSentence(word);
            wordBlock.remove();
        });
    });
});