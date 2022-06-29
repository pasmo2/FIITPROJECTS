var gameArea = {
    canvas: document.createElement("canvas"),
    start: function () {
        this.canvas.style.border = "1px solid black";
        this.canvas.width = 1000;
        this.canvas.height = 500;
        this.context = this.canvas.getContext("2d");
        document.body.insertBefore(this.canvas, document.body.childNodes[0]);
    },
    clear: function () {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height)
    }
};
var showSettings = {
    settingsAudio: document.createElement("button"),
    settingsReturnToGame: document.createElement("button"),
    start: function () {
        gameStopped = true;
        this.settingsAudio.addEventListener("click", toggleAudio);
        this.settingsAudio.style.position = "absolute";
        this.settingsAudio.style.visibility = "visible";
        this.settingsAudio.style.top = "100px";
        this.settingsAudio.style.left = "400px";
        this.settingsAudio.style.width = "200px";
        this.settingsAudio.style.height = "50px";
        this.settingsAudio.innerHTML = "TOGGLE AUDIO";
        document.body.insertBefore(this.settingsAudio, document.body.childNodes[0]);
        this.settingsReturnToGame.addEventListener("click", resumeGame);
        this.settingsReturnToGame.style.position = "absolute";
        this.settingsReturnToGame.style.visibility = "visible";
        this.settingsReturnToGame.style.top = "170px";
        this.settingsReturnToGame.style.left = "400px";
        this.settingsReturnToGame.style.width = "200px";
        this.settingsReturnToGame.style.height = "50px";
        this.settingsReturnToGame.innerHTML = "RESUME GAME";
        document.body.insertBefore(this.settingsReturnToGame, document.body.childNodes[0]);
    }
}
function showTowerMenu() {
    this.color = "lightgrey";
    this.x = 855;
    this.y = 115;
    this.width = 140;
    this.height = 270;
    this.ctx = gameArea.context;
    this.ctx.font = "10px Arial";
    this.start = function () {
        towerMenuDisplayed++;
    }
    this.update = function () {
        this.ctx.font = "10px Arial";
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(this.x, this.y, this.width, this.height);
        this.ctx.strokeText("basic tower", this.x + 20, this.y + 90);
        this.ctx.strokeText("slow tower", this.x + 80, this.y + 90);
        this.ctx.strokeText("explo tower", this.x + 20, this.y + 160);
        this.ctx.strokeText("sniper tower", this.x + 80, this.y + 160);
        this.ctx.fillStyle = "lightblue";
        this.ctx.fillRect(this.x + 20, this.y + 40, 40, 40);
        this.ctx.fillStyle = "lightgreen";
        this.ctx.fillRect(this.x + 80, this.y + 40, 40, 40);
        this.ctx.fillStyle = "pink";
        this.ctx.fillRect(this.x + 20, this.y + 110, 40, 40);
        this.ctx.fillStyle = "yellow";
        this.ctx.fillRect(this.x + 80, this.y + 110, 40, 40);
    }
}
function towerPlacementFine(x,y){
    this.x=x;
    this.y=y;
    this.width=25;
    this.height=25;
    for(i=0;i<towers.length;i++){
        if(this.x+(towers[i].width/2)>=towers[i].x && this.x-(towers[i].width/2)<=towers[i].x+towers[i].width && this.y+(towers[i].height/2)>=towers[i].y && this.y-(towers[i].height/2)<=towers[i].y+towers[i].height){
            return 0;
        }
    }
    if(
        (this.x+this.width>=100 && this.y+this.height>=50 && this.x-this.width<=((gameArea.canvas.width) - 50) && this.y-this.height<=100) || 
        (this.x+this.width>=100 && this.y+this.height>=100 && this.x-this.width<=150 && this.y-this.height<=350) ||
        (this.x+this.width>=100 && this.y+this.height>=350 && this.x-this.width<=((gameArea.canvas.width) - 200) && this.y-this.height<=400) ||
        (this.x+this.width>=800 && this.y+this.height>=350 && this.x-this.width<=850 && this.y-this.height<=450) ||
        (this.x+this.width>=showTowerMenu1.x && this.y+this.height>=showTowerMenu1.y && this.x-this.width<=showTowerMenu1.x+showTowerMenu1.width && this.y-this.height<=showTowerMenu1.y+showTowerMenu1.height)
    ){
       return 0; 
    }
    return 1;
}
function towerInfo(){
    for(towerNum=0;towerNum<towers.length;towerNum++){
        if(mouseClickX>=towers[towerNum].x && mouseClickX<=towers[towerNum].x+towers[towerNum].width && mouseClickY>=towers[towerNum].y && mouseClickY<=towers[towerNum].y+towers[towerNum].height){
            towerInfoState=true;
            towerInfoTextTowerLevel= new printText("Tower level: "+towers[towerNum].towerLevel,865,295,"14px Arial","black");
            towerInfoTextDamage= new printText("Tower damage: "+towers[towerNum].damage,865,315,"14px Arial","black");
            towerInfoTextUpgradeCost= new printText("Upgrade cost: "+upgradeCostBasic[towers[towerNum].towerLevel],865,335,"14px Arial","black");
            towerInfoTextCancel= new printText("X",967,293,"17px Arial","black");
            mouseClickX=0;
            mouseClickY=0;
            currentTower=towerNum;
        }
    }
    if(mouseClickX>=965 && mouseClickX<=980 && mouseClickY>=280 && mouseClickY<=295){
        towerInfoState=false;
        mouseClickX=0;
        mouseClickY=0;
    }
    if(mouseClickX>=895 && mouseClickX<=60+895 && mouseClickY>=350 && mouseClickY<=26+350){
        if(towers[currentTower].towerLevel<=19 && gold>=upgradeCostBasic[towers[currentTower].towerLevel]){
            towers[currentTower].upgrade();
            gold-=upgradeCostBasic[towers[currentTower].towerLevel-1];
        }
        towerInfoTextTowerLevel= new printText("Tower level: "+towers[currentTower].towerLevel,865,295,"14px Arial","black");
        towerInfoTextDamage= new printText("Tower damage: "+towers[currentTower].damage,865,315,"14px Arial","black");
        towerInfoTextUpgradeCost= new printText("Upgrade cost: "+upgradeCostBasic[towers[currentTower].towerLevel],865,335,"14px Arial","black");
        mouseClickX=0;
        mouseClickY=0;
    }
    if(towerInfoState==true && towerMenuDisplayed%2){
        gameArea.context.beginPath();
        gameArea.context.rect(860,280,130,100);
        gameArea.context.stroke();
        gameArea.context.beginPath();
        gameArea.context.rect(965,280,15,15);
        gameArea.context.stroke();
        towerInfoTextTowerLevel.update();
        towerInfoTextUpgradeCost.update();
        towerInfoTextDamage.update();
        towerInfoTextCancel.update();
        upgradeButton.update();
    }
}
function reduce(numerator, denominator) {
    var gcd = function gcd(a, b) {
        return b ? gcd(b, a % b) : a;
    };
    gcd = gcd(numerator, denominator);
    return [numerator / gcd, denominator / gcd];
}
function itComesInWaves() {
    if (enemies.length == 0) {
        waveCount++;
    }
}
function spawnEnemies() {
    if (enemyCount < ((waveCount * 10)-(Math.floor(waveCount/5)*9)) && gameTime > 0 && (gameTime % 100) == 0 && waveCount%5!=0) {
        enemies[enemies.length] = new kruhac(925, 75, "green", 25, 1,100);
        enemyCount++;
    }
    if (enemyCount < ((waveCount * 10)-(Math.floor(waveCount/5)*9)) && gameTime > 0 && (gameTime % 100) == 0 && waveCount%5==0){
        enemies[enemies.length]= new kruhac(925,75,"lightblue",35,1,1000);
        enemyCount++;
    }

}
function spawnProjectiles(index, Xspeed, Yspeed, projSpeed,damage) {
    projectiles[projectiles.length] = new towerProjectiles(5, projSpeed, towers[index].color, towers[index].x + 25, towers[index].y + 25, damage, Xspeed, Yspeed,towers[index].towerType);
    projectileCount++;
}
function manageProjectiles() {
    if (gameTime > 0) {
        for (i = 0; i < towers.length; i++) {
            enemyInRange = false;
            nearestEnemy = 1000;
            nearestEnemyX = 0;
            nearestEnemyY = 0;
            for (j = 0; j < enemies.length; j++) {
                if ((towers[i].x+(towers[i].width/2) - enemies[j].x) * (towers[i].x+(towers[i].width/2) - enemies[j].x) + (towers[i].y+(towers[i].height/2) - enemies[j].y) * (towers[i].y+(towers[i].height/2) - enemies[j].y) <= 150 * 150) {
                    enemyInRange = true;
                    if (nearestEnemy * nearestEnemy > ((towers[i].x+(towers[i].width/2) - enemies[j].x) * (towers[i].x+(towers[i].width/2) - enemies[j].x) + (towers[i].y+(towers[i].height/2) - enemies[j].y) * (towers[i].y+(towers[i].height/2) - enemies[j].y))) {
                        nearestEnemy = Math.floor(Math.pow(((towers[i].x+(towers[i].width/2) - enemies[j].x) * (towers[i].x+(towers[i].width/2) - enemies[j].x) + (towers[i].y+(towers[i].height/2) - enemies[j].y) * (towers[i].y+(towers[i].height/2) - enemies[j].y)), 0.5));
                        this.multiplier=1;
                        nearestEnemyX = enemies[j].x;
                        nearestEnemyY = enemies[j].y;
                        this.distanceTime=(nearestEnemy/skapemZ);
                        nearestEnemyFuture = Math.floor(Math.pow(((towers[i].x - (enemies[j].x+this.distanceTime*enemies[j].speedX)) * (towers[i].x - (enemies[j].x+this.distanceTime*enemies[j].speedX)) + (towers[i].y - (enemies[j].y+this.distanceTime*enemies[j].speedY)) * (towers[i].y - (enemies[j].y+this.distanceTime*enemies[j].speedY))), 0.5));
                        if(nearestEnemyFuture>nearestEnemy) this.multiplier=2;
                        //enemyDistanceX = nearestEnemyX - (towers[i].x+(towers[i].width/2));
                        //enemyDistanceY = nearestEnemyY - (towers[i].y+(towers[i].height/2));
                        enemyDistanceX=(nearestEnemyX+(this.multiplier*(this.distanceTime)*enemies[j].speedX)) - (towers[i].x+(towers[i].width/2));
                        enemyDistanceY=(nearestEnemyY+(this.multiplier*(this.distanceTime)*enemies[j].speedY)) - (towers[i].y+(towers[i].height/2));
                    }
                }
            }
            //document.getElementById("xy").innerHTML = "nearest enemy=> X:" + nearestEnemyX + "Y:" + nearestEnemyY + "distance:" + nearestEnemy;
            if (enemyInRange == true && gameTime % (towers[i].attackSpeed) == 0) {                   
                skapemArray = reduce(enemyDistanceX, enemyDistanceY);
                skapemA = Math.abs(skapemArray[0]);
                skapemB = Math.abs(skapemArray[1]);
                skapemZ = 5;
                skapemX = (skapemZ * skapemA) / (Math.sqrt((skapemA * skapemA) + (skapemB * skapemB)));
                skapemY = (skapemZ * skapemB) / (Math.sqrt((skapemA * skapemA) + (skapemB * skapemB)));
                if (enemyDistanceX < 0) skapemX = -skapemX;
                if (enemyDistanceY < 0) skapemY = -skapemY;
                spawnProjectiles(i, skapemX, skapemY, skapemZ,towers[i].damage);
            }
        }
    }
}
function resumeEnemyMovement(index){
    enemies[index].slowed=false;
}
function handleExplosions(){
    for(fr=0;fr<explosions.length;fr++){
        if(explosions[fr].alive==false && explosions.length>0){
            explosions.splice(fr,1);
            continue;
        }
        explosions[fr].update();
    }
}
function collision() {
    if (enemies.length > 0) {
        for (fx = 0; fx < enemies.length; fx++) {
            for (fs = 0; fs < projectiles.length; fs++) {
                dx = enemies[fx].x - projectiles[fs].x;
                dy = enemies[fx].y - projectiles[fs].y;
                distance = Math.sqrt(dx * dx + dy * dy);
                if ((distance < enemies[fx].radius + projectiles[fs].radius) && enemies[fx].alive && projectiles[fs].alive) {
                    if(projectiles[fs].towerType=="basic" || projectiles[fs].towerType=="sniper"){
                       enemies[fx].hitPoints -= projectiles[fs].damage;
                    }
                    if(projectiles[fs].towerType=="slow"){
                        if(enemies[fx].slowed==false){
                            enemies[fx].slowed=true;
                            setTimeout(resumeEnemyMovement,200,fx);
                        }
                    }
                    if(projectiles[fs].towerType=="explosive"){
                        explosions[explosions.length]= new kruh(enemies[fx].x,enemies[fx].y,"#eebbc3",150);
                        for(i=0;i<explosions.length;i++){
                            for(j=0;j<enemies.length;j++){
                                rx= enemies[j].x-explosions[i].x;
                                ry=enemies[j].y-explosions[i].y;
                                distance2 = Math.sqrt(rx * rx + ry * ry);
                                if((distance2<enemies[j].radius + explosions[i].radius) && enemies[j].alive && explosions[i].alive){
                                    enemies[j].hitPoints-=projectiles[fs].damage;
                                }
                            }
                        }
                    }
                    projectiles[fs].alive = false;
                }
            }
        }
    }
};
function enemyMovementTurn() {
    for (fy = 0; fy < enemies.length; fy++) {
        if (enemies[fy].x == 925 && enemies[fy].y == 75) enemies[fy].speedX = -enemies[fy].speed;
        if (enemies[fy].x == 125 && enemies[fy].y == 75) {
            enemies[fy].speedX = 0;
            enemies[fy].speedY = enemies[fy].speed;
        }
        if (enemies[fy].x == 125 && enemies[fy].y == 375) {
            enemies[fy].speedX = enemies[fy].speed;
            enemies[fy].speedY = 0;
        }
        if (enemies[fy].x == 825 && enemies[fy].y == 375) {
            enemies[fy].speedX = 0;
            enemies[fy].speedY = enemies[fy].speed;
        }
        if (enemies[fy].x == 825 && enemies[fy].y == 425) {
            enemies[fy].speedX = 0;
            enemies[fy].speedY = 0;
            enemies[fy].alive = false;
            if (gameAudio == "true") {
                audioOof.load();
                audioOof.play();
            }

            playerLife--;
        }
    }
}
function enemyMovement() {
    for (ff = 0; ff < towers.length; ff++) {
        towers[ff].update();
    }
    for (fx = 0; fx < enemies.length; fx++) {
        if (enemies[fx].hitPoints <= 0) {
            if (gameAudio == "true") {
                audioDeath.load();
                audioDeath.play();
            }
        }
        if (enemies[fx].alive == false && enemies.length > 0) {
            gold+=Math.floor(Math.pow(1.2,(waveCount)-1)*10);
            enemies.splice(fx, 1);
        }
        if (enemies[fx].alive == true && enemies.length > 0) enemies[fx].update();

    }
    for (fs = 0; fs < projectiles.length; fs++) {
        if (projectiles[fs].alive) projectiles[fs].update();
        if (projectiles[fs].alive && (projectiles[fs].x < 0 || projectiles[fs].y < 0 || projectiles[fs].x > gameArea.canvas.width || projectiles[fs].y > gameArea.canvas.height)) projectiles[fs].alive = false;
        if (projectiles[fs].alive == false) {
            projectiles.splice(fs, 1);
        }
    }
}
function playerLifeCheck() {
    if (playerLife == 0) {
        gameState = "gameOver";
        resetVariables();
        enemies = [];
        projectiles = [];
        towers = [];
        projectileIntervals = [];
    }
}
function buttonVisibility(buttonState) {
    document.getElementById("settingsButton").style.visibility = buttonState;
    document.getElementById("towerButton").style.visibility = buttonState;
    document.getElementById("audioButton").style.visibility = buttonState;
}