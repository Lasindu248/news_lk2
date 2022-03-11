// See https://developer.mozilla.org/en-US/docs/Web/API/SpeechSynthesisUtterance/voice
function tts(id, text) {
  const synth = window.speechSynthesis;
  synth.cancel();

  const buttons = document.getElementsByTagName("button");
  for (button of buttons) {
    if (button.id === id) {
      if (button.innerHTML === "⏯︎") {
        button.innerHTML = "⏸︎";
        let utterThis = new SpeechSynthesisUtterance(text);
        utterThis.lang = "en-GB";
        utterThis.rate = 1.25;
        synth.speak(utterThis);
      } else {
        button.innerHTML = "⏯︎";
      }
    } else {
      button.innerHTML = "⏯︎";
    }
  }
}
