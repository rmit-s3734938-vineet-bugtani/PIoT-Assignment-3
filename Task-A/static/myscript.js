window.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("voice-search");
    const result = document.getElementsByName("search")[0];

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (typeof SpeechRecognition === "undefined") {
        button.remove();
        const message = document.getElementById("message");
        message.removeAttribute("hidden");
        message.setAttribute("aria-hidden", "false");
    } else {
        let listening = false;
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-IN';
        const start = () => {
            recognition.start();
            button.textContent = "Stop listening";
        };
        const stop = () => {
            recognition.stop();
            button.textContent = "Start listening";
        };
        const onResult = event => {
            result.value = "";
            for (const res of event.results) {
                var text = res[0].transcript;
                if(text == 'clear'){
                    text = '';
                }
                result.value = text;
                document.getElementsByClassName("search-form")[0].submit()
            }
        };
       
        
        recognition.addEventListener("result", onResult);

        button.addEventListener("click", () => {
            listening ? stop() : start();
            listening = !listening;
        });
    }
});