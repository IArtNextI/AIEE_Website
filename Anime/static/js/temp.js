function blobToFile(theBlob, fileName) {
    theBlob.lastModifiedDate = new Date();
    theBlob.name = fileName;
    return theBlob;
}

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        let state = 0;

        const mediaRecorder = new MediaRecorder(stream);

        audioChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", () => {
            let audioBlob = new Blob(audioChunks, { 'type' : 'audio/wav' });
            let anime = blobToFile(audioBlob, "anime.wav");
            let audioUrl = URL.createObjectURL(anime);
            let xhr = new XMLHttpRequest();
            let absu = document.getElementById("absu").innerText
            absu = absu.trim();
            xhr.open("POST", absu, true);
            let b = new FormData();
            b.append("" + (state + 1), anime, "anime.wav");
            xhr.send(b);
            audioChunks = [];
            state += 1;
        });

        let countDownDate = new Date(new Date().getTime() + 100000).getTime();

        let first = true;
        let ok = true;

        let curstate = "none";

        let x = setInterval(function() {
            let now = new Date().getTime();

            let distance = countDownDate - now;

            let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((distance % (1000 * 60)) / 1000);

            document.getElementById("demo").innerHTML = "Time left: "
            + minutes + "m " + seconds + "s ";

            if (distance < 0) {
                if (curstate == "none") {
                    countDownDate = new Date(new Date().getTime() + 130000).getTime();
                    mediaRecorder.start();
                    curstate = "reading";
                }
                else if (curstate == "reading") {
                    mediaRecorder.stop();
                    document.getElementById('task-d').innerText = document.getElementById('2task-descr').innerText;        
                    countDownDate = new Date(new Date().getTime() + 60000).getTime();
                    curstate = "1q";
                    let tmp = document.getElementById('task-h').innerText;
                    tmp = "Task " + (parseInt(document.getElementById('userv').innerText) + 1) + '.2';
                    document.getElementById('task-h').innerText = tmp;
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/1q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 1/6";
                    mediaRecorder.start();
                }
                else if (curstate == "1q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 40000).getTime();
                    curstate = "2q";
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/2q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 2/6";
                    mediaRecorder.start();
                }
                else if (curstate == "2q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 40000).getTime();
                    curstate = "3q";
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/3q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 3/6";
                    mediaRecorder.start();
                }
                else if (curstate == "3q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 40000).getTime();
                    curstate = "4q";
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/4q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 4/6";
                    mediaRecorder.start();
                }
                else if (curstate == "4q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 40000).getTime();
                    curstate = "5q";
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/5q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 5/6";
                    mediaRecorder.start();
                }
                else if (curstate == "5q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 40000).getTime();
                    curstate = "6q";
                    document.getElementById("iframeAudio").src = 'https://s3.us-east-2.amazonaws.com/aiee-public-files/Var' + (parseInt(document.getElementById("userv").innerText) + 1) + '/6q.mp3'
                    document.getElementById('task-t').innerText = "You are answering question 6/6";
                    mediaRecorder.start();
                }
                else if (curstate == "6q") {
                    mediaRecorder.stop();
                    countDownDate = new Date(new Date().getTime() + 100000).getTime();
                    curstate = "wait";
                    document.getElementById('task-d').innerText = document.getElementById('3t').innerText;
                    document.getElementById('task-t').innerText = document.getElementById('3td').innerText;
                    let tmp = document.getElementById('task-h').innerText;
                    tmp = "Task " + (parseInt(document.getElementById('userv').innerText) + 1) + '.3';
                    document.getElementById('task-h').innerText = tmp;
                }
                else if (curstate == "wait") {
                    mediaRecorder.start();
                    curstate = "monologue";
                    countDownDate = new Date(new Date().getTime() + 130000).getTime();
                }
                else if (curstate == "monologue") {
                    mediaRecorder.stop();
                }
            }         
        })
});