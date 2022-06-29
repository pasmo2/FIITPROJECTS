function mainMenuButtons() {
    if (gameState == "mainMenu" && mouseClickX >= mainMenuButtonStartGame.x  && mouseClickX <= mainMenuButtonStartGame.x + mainMenuButtonStartGame.width  && mouseClickY >= mainMenuButtonStartGame.y  && mouseClickY <= mainMenuButtonStartGame.y + mainMenuButtonStartGame.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
        gameState = "instructions";
    }
    if (gameState == "mainMenu" && mouseClickX >= mainMenuButtonSettings.x  && mouseClickX <= mainMenuButtonSettings.x + mainMenuButtonSettings.width  && mouseClickY >= mainMenuButtonSettings.y  && mouseClickY <= mainMenuButtonSettings.y + mainMenuButtonSettings.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
    }
    if (gameState == "mainMenu" && mouseClickX >= mainMenuButtonExit.x  && mouseClickX <= mainMenuButtonExit.x + mainMenuButtonExit.width  && mouseClickY >= mainMenuButtonExit.y  && mouseClickY <= mainMenuButtonExit.y + mainMenuButtonExit.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
    }
}
function instructionsButtons() {
    if (gameState == "instructions" && mouseClickX >= instructionsButtonUnderstood.x  && mouseClickX <= instructionsButtonUnderstood.x + instructionsButtonUnderstood.width  && mouseClickY >= instructionsButtonUnderstood.y  && mouseClickY <= instructionsButtonUnderstood.y + instructionsButtonUnderstood.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
        gameState = "inGame";
        startGame();
    }
}
function inGameButtons() {
    if (gameState == "inGame" && mouseClickX >= waveButton.x  && mouseClickX <= waveButton.x + waveButton.width  && mouseClickY >= waveButton.y  && mouseClickY <= waveButton.y + waveButton.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
        itComesInWaves();
        //document.getElementById("xy").innerHTML = Math.floor(100 * (Math.pow(1.2, (waveCount - 1))));
    }
}
function gameOverButtons() {
    if (gameState == "gameOver" && mouseClickX >= gameOverButtonTryAgain.x  && mouseClickY >= gameOverButtonTryAgain.y  && mouseClickX <= gameOverButtonTryAgain.x + gameOverButtonTryAgain.width  && mouseClickY <= gameOverButtonTryAgain.y + gameOverButtonTryAgain.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
        startGame();
        gameState = "inGame";
    }
    if (gameState == "gameOver" && mouseClickX >= gameOverButtonExitGame.x  && mouseClickY >= gameOverButtonExitGame.y  && mouseClickX <= gameOverButtonExitGame.x + gameOverButtonExitGame.width  && mouseClickY <= gameOverButtonExitGame.y + gameOverButtonExitGame.height ) {
        mouseClickX = 0;
        mouseClickY = 0;
        gameState = "mainMenu";
    }
}