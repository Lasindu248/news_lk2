function tts(text) {
    let synth = window.speechSynthesis;
    synth.cancel();

    let utterThis = new SpeechSynthesisUtterance(text);
    utterThis.lang = 'en-GB';
    utterThis.rate = 1.25;

    synth.speak(utterThis);
}
