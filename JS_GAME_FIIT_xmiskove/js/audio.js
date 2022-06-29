function toggleAudio() {
    if (gameAudio == "true") {
        audioMain.pause();
        gameAudio = "false";
        return;
    }

    if (gameAudio == "false") {
        audioMain.play();
        gameAudio = "true";
    }
    return;
}