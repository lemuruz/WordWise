function submitSentence(event){
    event.preventDefault();

    let formData = new FormData(document.getElementById("sentenceForm"));

    fetch(submit_url, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest" 
        }
    }).then(response => response.json())
    .then(data => {
        console.log(data.success)
        if(data.success) {
            //TO Add popup
            document.getElementById("show-error").style.display = "none";
            document.getElementById("popup").style.display = "flex";
            document.getElementById("sentenceForm").reset();
        } else {
            document.getElementById("show-error").style.display = "inline-block";
        }
    })
    .catch(error => console.error("Error:", error));
}

document.addEventListener("DOMContentLoaded", function(){
    const popup = document.getElementById("popup");
    const popup_close = document.getElementById("popup-close");
    popup_close.addEventListener("click", function() {
        popup.style.display = "none";
    });
});