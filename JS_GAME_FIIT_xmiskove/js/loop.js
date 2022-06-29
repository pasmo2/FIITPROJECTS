function mainMenu() {
    gameState = "mainMenu";
    startInterval();
    gameArea.start();
    //skuskaProj= new panak(500,250,"black",20,20);
    uwaga1 = new placeImage("obrazky/uwagaedit.png", 800, 400, 50, 50);
    path1 = new drawPath("khaki");
    heart1 = new placeImage("obrazky/heart.png", 10, 430, 50, 50);
    waveButton = new placeImage("obrazky/playButton.png", 487, 12, 25, 25);
    upgradeButton = new placeImage("obrazky/Upgrade.png",895,350,60,26);
    mainMenu1 = new placeImage("obrazky/mainMenu.png", 0, 0, 1000, 500);
    mainMenuButtonStartGame = new placeImage("obrazky/mainMenuStartGameButton.png", 350, 200, 300, 50);
    mainMenuButtonSettings = new placeImage("obrazky/mainMenuSettingsButton.png", 400, 270, 200, 50);
    mainMenuButtonExit = new placeImage("obrazky/mainMenuExitButton.png", 425, 340, 150, 50);
    instructions1 = new placeImage("obrazky/instructions.png", 0, 0, 1000, 500);
    instructionsButtonUnderstood = new placeImage("obrazky/instructionsUnderstoodButton.png", 350, 400, 300, 50);
    gameOver1 = new placeImage("obrazky/gameOver.png", 0, 0, 1000, 500);
    gameOverButtonTryAgain = new placeImage("obrazky/gameOverTryAgainButton.png", 350, 340, 300, 50);
    gameOverButtonExitGame = new placeImage("obrazky/gameOverExitGameButton.png", 350, 410, 300, 50);
    //    printTextLife = new printText(playerLife, 70, 470, "50px Arial", "black");
    //    printTextWaveCount = new printText("Wave:"+waveCount,150,35,"30px Arial","black");
    constructTower1 = new constructTower();
    showTowerMenu1 = new showTowerMenu();

}
function startGame() {
    playerLife = 2;
    if (gameAudio == "true") audioMain.play();
};
function resumeGame() {
    var f = updateGame;
    gameStopped = false;
    showSettings.settingsAudio.style.visibility = "hidden";
    showSettings.settingsReturnToGame.style.visibility = "hidden";
    interval = setInterval(f, 20);
}
function startInterval() {
    var f = updateGame;
    interval = setInterval(f, 20);
}
function updateGame() {
    if (gameState == "mainMenu") {
        buttonVisibility("hidden");
        mainMenu1.update();
        mainMenuButtonStartGame.update();
        mainMenuButtonSettings.update();
        mainMenuButtonExit.update();
        mainMenuButtons();
        //document.getElementById("xyskusacky").innerHTML = "X:" + mouseX + " Y:" + mouseY;
    }
    if (gameState == "instructions") {
        buttonVisibility("hidden");
        instructionsButtons();
        instructions1.update();
        instructionsButtonUnderstood.update();
       //document.getElementById("xyskusacky").innerHTML = "X:" + mouseX + " Y:" + mouseY;
    }
    if (gameState == "inGame") {
        gameTime++;
        buttonVisibility("visible");
        spawnEnemies();
        manageProjectiles();
        gameArea.clear();
        path1.update();
        uwaga1.update();
        waveButton.update();
        inGameButtons();
        playerLifeCheck();
        heart1.update();
        printTextLife = new printText(playerLife, 70, 470, "50px Arial", "black");
        if (waveCount != 0) printTextWaveCount = new printText("Wave:" + waveCount, 350, 35, "30px Arial", "black");
        printTextLife.update();
        if (waveCount != 0) printTextWaveCount.update();
        printTextGold= new printText("Gold: "+gold,550,35,"30px Arial","black");
        printTextGold.update();
        //document.getElementById("xyskusacky").innerHTML = "X:" + mouseX + " Y:" + mouseY;
        if (towerMenuDisplayed % 2) showTowerMenu1.update();
        if (gameStopped == true) clearInterval(interval);
        constructTower1.update();
        collision();
        handleExplosions();
        if(towers.length>0)towerInfo();
        enemyMovement();
        enemyMovementTurn();
    }
    if (gameState == "gameOver") {
        buttonVisibility("hidden");
        gameOver1.update();
        gameOverButtonTryAgain.update();
        gameOverButtonExitGame.update();
        gameOverButtons();
        //document.getElementById("xyskusacky").innerHTML = "X:" + mouseX + " Y:" + mouseY;
    }
};