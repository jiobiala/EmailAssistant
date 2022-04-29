navigator
        .mediaDevices
        .getUserMedia({audio: true})
        .then(stream => { handlerFunction(stream) });



    function handlerFunction(stream) {
        rec = new MediaRecorder(stream);
        rec.ondataavailable = e => {
            audioChunks.push(e.data);
            if (rec.state === "inactive") {
                let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
                sendData(blob);
            }
        }
    }

    function sendData(data) {

        var e = $("#inputEmail").val();

        var form = new FormData();
        form.append('file', data, 'data.mp3');
        form.append('title', 'data.mp3');
        form.append('email', e)

        //Chrome inspector shows that the post data includes a file and a title.
        $.ajax({
            type: 'POST',
            url: '/login_email',
            data: form,
            cache: false,
            processData: false,
            contentType: false,

        }).done(function(data) {
            if(data.loc === "/login_password"){
                var msg = new SpeechSynthesisUtterance();
                msg.text = " please say your password, click the screen to start recording and click again to stop";
                window.speechSynthesis.speak(msg);
                window.location.href = '/login_password';
            }else{
                $(email).replaceWith(data)
            }



        });
    }

    document.body.addEventListener("click", function(event) {
        if (rec.state === "inactive"){
            audioChunks = [];
            rec.start();
        }else {
            rec.stop();
        }
    });

