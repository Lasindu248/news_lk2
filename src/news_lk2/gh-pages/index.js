// See https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/voice
function tts(id, title, body) {
  const synth = window.speechSynthesis;
  synth.cancel();

  const buttons = document.getElementsByTagName("button");
  for (button of buttons) {
    if (button.id === id) {
      if (button.innerHTML === "⏯︎") {
        button.innerHTML = "⏸︎";

        let utterTitle = new SpeechSynthesisUtterance(title);
        utterTitle.lang = "en-GB";
        utterTitle.rate = 1;
        utterTitle.pitch = 1;
        synth.speak(utterTitle);

        let utterBody = new SpeechSynthesisUtterance(body);
        utterBody.lang = "en-GB";
        utterBody.rate = 1.2;
        utterBody.pitch = 1.2;
        synth.speak(utterBody);
      } else {
        button.innerHTML = "⏯︎";
      }
    } else {
      button.innerHTML = "⏯︎";
    }
  }
}
