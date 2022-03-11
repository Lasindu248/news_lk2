function tts(text) {
    let synth = window.speechSynthesis;
    synth.cancel();
    let utterThis = new SpeechSynthesisUtterance(text);
    synth.speak(utterThis);
}
