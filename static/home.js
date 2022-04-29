document.body.addEventListener("click", function(event) {
        var msg = new SpeechSynthesisUtterance();
        msg.text = "please say your email_address, click the screen to start recording and click again to stop";
        window.speechSynthesis.speak(msg);
        document.location = '/login_email', true;
    });
