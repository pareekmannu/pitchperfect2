let mediaRecorder;
let audioChunks = [];

document.getElementById("recordBtn").onclick = async () => {
  const statusEl = document.getElementById("status");

  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = event => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      audioChunks = [];

      statusEl.innerText = "Status: Sending to AI...";
      const formData = new FormData();
      formData.append("audio", audioBlob);

      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      document.getElementById("transcript").value = data.transcript;
      document.getElementById("feedback").innerText = data.feedback;
      statusEl.innerText = "Status: Done ✅";
    };

    mediaRecorder.start();
    statusEl.innerText = "Status: Recording...";
    document.getElementById("recordBtn").innerText = "⏹️ Stop Recording";
  } else {
    mediaRecorder.stop();
    document.getElementById("recordBtn").innerText = "🎙️ Start Recording";
  }
};
