function constructTower() {
    document.addEventListener("click", function (event1) {
        mouseClickX = event1.clientX -8;
        mouseClickY = event1.clientY -8;
        clickCount++;
    });
    document.addEventListener("mousemove", function (event2) {
        mouseX = event2.clientX-8;
        mouseY = event2.clientY-8;
    });
    this.ctx = gameArea.context;
    this.update = function () {
        if (gold>=upgradeCostBasic[0] && greenTowerClick == 0 && blueTowerClick == 0 && yellowTowerClick == 0 && redTowerClick == 0 && clickCount > 0 && mouseClickX >= showTowerMenu1.x + 22 && mouseClickX <= showTowerMenu1.x + 62 && mouseClickY >= showTowerMenu1.y + 42 && mouseClickY <= showTowerMenu1.y + 82 && (towerMenuDisplayed % 2)) {
            //document.getElementById("xy").innerHTML = "clicked blue tower";
            clickCount = 0;
            clickCount++;
            blueTowerClick++;
        }
        if (blueTowerClick > 0) {
            this.ctx.beginPath();
            this.ctx.arc(mouseX, mouseY,150, 0, (Math.PI)*2,true);
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
            this.ctx.fillStyle = "#76E5FC";
            this.ctx.fillRect(mouseX - 25, mouseY - 25, 50, 50);
        }
        if (towerPlacementFine(mouseClickX,mouseClickY) && clickCount > 1 && blueTowerClick > 0 && (mouseClickX < showTowerMenu1.x - 15 || mouseClickY < showTowerMenu1.y - 15 || mouseClickX > showTowerMenu1.x + showTowerMenu1.width || mouseClickY > showTowerMenu1.y + showTowerMenu1.height)) {
            towers[towerCount] = new createTower(mouseClickX - 25, mouseClickY - 25, 50, 50, "blue",10,1,"basic",10);
            towerCount++;
            //i++;
            gold-=upgradeCostBasic[0];
            clickCount = 0;
            blueTowerClick = 0;
            mouseClickX=0;
            mouseClickY=0;
        }
        if (gold>=upgradeCostBasic[0] && greenTowerClick == 0 && blueTowerClick == 0 && yellowTowerClick == 0 && redTowerClick == 0 && clickCount > 0 && mouseClickX >= showTowerMenu1.x + 82 && mouseClickX <= showTowerMenu1.x + 122 && mouseClickY >= showTowerMenu1.y + 42 && mouseClickY <= showTowerMenu1.y + 82 && (towerMenuDisplayed % 2)) {
            //document.getElementById("xy").innerHTML = "clicked green tower";
            clickCount = 0;
            clickCount++;
            greenTowerClick++;
        }
        if (greenTowerClick > 0) {
            this.ctx.beginPath();
            this.ctx.arc(mouseX, mouseY,150, 0, (Math.PI)*2,true);
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
            this.ctx.fillStyle = "#8DE969";
            this.ctx.fillRect(mouseX - 25, mouseY - 25, 50, 50);
        }
        if (towerPlacementFine(mouseClickX,mouseClickY) && clickCount > 1 && greenTowerClick > 0 && (mouseClickX < showTowerMenu1.x - 15 || mouseClickY < showTowerMenu1.y - 15 || mouseClickX > showTowerMenu1.x + showTowerMenu1.width || mouseClickY > showTowerMenu1.y + showTowerMenu1.height)) {
            towers[towerCount] = new createTower(mouseClickX - 25, mouseClickY - 25, 50, 50, "green",20,1,"slow",50);
            towerCount++;
            //i++;
            gold-=upgradeCostBasic[0];
            clickCount = 0;
            greenTowerClick = 0;
            mouseClickX=0;
            mouseClickY=0;
        }
        if (gold>=upgradeCostBasic[0] && greenTowerClick == 0 && blueTowerClick == 0 && yellowTowerClick == 0 && redTowerClick == 0 && clickCount > 0 && mouseClickX >= showTowerMenu1.x + 22 && mouseClickX <= showTowerMenu1.x + 62 && mouseClickY >= showTowerMenu1.y + 112 && mouseClickY <= showTowerMenu1.y + 152 && (towerMenuDisplayed % 2)) {
            //document.getElementById("xy").innerHTML = "clicked pink tower";
            clickCount = 0;
            clickCount++;
            redTowerClick++;
        }
        if (redTowerClick > 0) {
            this.ctx.beginPath();
            this.ctx.arc(mouseX, mouseY,150, 0, (Math.PI)*2,true);
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
            this.ctx.fillStyle = "#EEB4B3";
            this.ctx.fillRect(mouseX - 25, mouseY - 25, 50, 50);
        }
        if (towerPlacementFine(mouseClickX,mouseClickY) && clickCount > 1 && redTowerClick > 0 && (mouseClickX < showTowerMenu1.x - 15 || mouseClickY < showTowerMenu1.y - 15 || mouseClickX > showTowerMenu1.x + showTowerMenu1.width || mouseClickY > showTowerMenu1.y + showTowerMenu1.height)) {
            towers[towerCount] = new createTower(mouseClickX - 25, mouseClickY - 25, 50, 50, "red",35,1,"explosive",75);
            towerCount++;
            //i++;
            gold-=upgradeCostBasic[0];
            clickCount = 0;
            redTowerClick = 0;
            mouseClickX=0;
            mouseClickY=0;
        }
        if (gold>=upgradeCostBasic[0] && greenTowerClick == 0 && blueTowerClick == 0 && yellowTowerClick == 0 && redTowerClick == 0 && clickCount > 0 && mouseClickX >= showTowerMenu1.x + 82 && mouseClickX <= showTowerMenu1.x + 122 && mouseClickY >= showTowerMenu1.y + 112 && mouseClickY <= showTowerMenu1.y + 152 && (towerMenuDisplayed % 2)) {
            //document.getElementById("xy").innerHTML = "clicked yellow tower";
            clickCount = 0;
            clickCount++;
            yellowTowerClick++;
        }
        if (yellowTowerClick > 0) {
            this.ctx.beginPath();
            this.ctx.arc(mouseX, mouseY,150, 0, (Math.PI)*2,true);
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
            this.ctx.fillStyle = "#FAFF81";
            this.ctx.fillRect(mouseX - 25, mouseY - 25, 50, 50);
        }
        if (towerPlacementFine(mouseClickX,mouseClickY) && clickCount > 1 && yellowTowerClick > 0 && (mouseClickX < showTowerMenu1.x - 15 || mouseClickY < showTowerMenu1.y - 15 || mouseClickX > showTowerMenu1.x + showTowerMenu1.width || mouseClickY > showTowerMenu1.y + showTowerMenu1.height)) {
            towers[towerCount] = new createTower(mouseClickX - 25, mouseClickY - 25, 50, 50, "#ECA72C",100,1,"sniper",150);
            towerCount++;
            //i++;
            gold-=upgradeCostBasic[0];
            clickCount = 0;
            yellowTowerClick = 0;
            mouseClickX=0;
            mouseClickY=0;
        }
    }
}
function panak(x, y, color, width, height) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.color = color;
    this.update = function () {
        this.ctx = gameArea.context;
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(this.x, this.y, this.width, this.height);
    };
};
function kruhac(x, y, color, radius, speed,hp) {
    this.maxHitPoints = Math.floor(hp * (Math.pow(1.2, (waveCount - 1))));
    this.hitPoints = this.maxHitPoints;
    this.speed = speed;
    this.speedX = 0;
    this.speedY = 0;
    this.x = x;
    this.y = y;
    this.pix2 = (Math.PI) * 2;
    this.radius = radius;
    this.hpBarWidth = 30;
    this.hpBarHeight = 5;
    this.alive = true;
    this.ctx = gameArea.context;
    this.slowed=false;
    this.update = function () {
        this.hpPercentage = (this.hitPoints / this.maxHitPoints) * 100;
        if (this.hitPoints <= 0) this.alive = false;
        if (this.hitPoints / this.maxHitPoints > 0) {
            this.ctx.fillStyle = "red";
            this.ctx.fillRect(this.x - 15, this.y + (this.radius+5), this.hpBarWidth, this.hpBarHeight);
            if (this.hpPercentage < 100) {
                this.ctx.fillStyle = "black";
                this.ctx.fillRect(this.x - 15, this.y + (this.radius+5), (this.hpBarWidth * (100 - this.hpPercentage)) / 100, this.hpBarHeight);
            }
        }
        if(this.slowed==false){
            this.x += (this.speedX);
            this.y += (this.speedY);
        }
        if(this.slowed==true){
            this.x += (this.speedX/2);
            this.y += (this.speedY/2);
        }
        this.color = color;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, this.pix2, true);
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    };
};
function kruh(x,y,color,radius,damage){
    this.x=x;
    this.y=y;
    this.radius=radius;
    this.ctx=gameArea.context;
    this.alive=true;
    this.pix2=(Math.PI)*2;
    this.time=gameTime;
    this.damage
    this.update= function(){
        if(this.time+20<gameTime) this.alive=false;
        this.color=color;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, this.pix2, true);
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
}
function emptyCircle(x,y,color,radius){
    //this.x=x;
    //this.y=y;
    this.radius=radius;
    this.pix2 = (Math.PI) * 2;
    this.ctx=gameArea.context;
    this.update= function(){
        this.color=color;
        this.x=x;
        this.y=y;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y,this.radius, 0, this.pix2,true);
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
};
function drawPath(color) {
    this.color = color;
    this.update = function () {
        this.ctx = gameArea.context;
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(100, 50, (gameArea.canvas.width) - 150, 50);
        this.ctx.fillRect(100, 100, 50, 250);
        this.ctx.fillRect(100, 350, gameArea.canvas.width - 300, 50);
        this.ctx.fillRect(800, 350, 50, 100);
    }
}
function placeImage(imgsrc, x, y, width, height) {
    this.ctx = gameArea.context;
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    var img = new Image();
    img.src = imgsrc;
    this.update = function () {
        this.ctx.drawImage(img, this.x, this.y, this.width, this.height);
    };
}
function createTower(x, y, width, height, color, damage,towerLevel,towerType,attackSpeed) {
    this.towerLevel=towerLevel;
    this.baseDamage=damage
    this.damage=this.baseDamage;
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
    this.color = color;
    this.ctx = gameArea.context;
    this.towerType=towerType;
    this.attackSpeed=attackSpeed;
    this.upgrade= function(){
        this.towerLevel++;
        this.damage=this.towerLevel*this.baseDamage;
    }
    this.update = function () {
        this.ctx.fillStyle = this.color;
        this.ctx.fillRect(this.x, this.y, this.width, this.height);
    }
}
function towerProjectiles(radius, projectileSpeed, color, x, y, damage, xSpeed, ySpeed,towerType) {
    this.projectileSpeed = projectileSpeed;
    this.damage = damage;
    this.towerType=towerType;
    this.radius = radius;
    this.pix2 = (Math.PI) * 2;
    this.x = x;
    this.y = y;
    this.alive = true;
    this.xSpeed = xSpeed;
    this.ySpeed = ySpeed;
    this.ctx = gameArea.context;
    this.update = function () {
        this.color = color;
        this.x += this.xSpeed;
        this.y += this.ySpeed;
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.radius, 0, this.pix2, true);
        this.ctx.fillStyle = this.color;
        this.ctx.fill();
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }
}
function printText(text, x, y, font, color) {
    this.x = x;
    this.y = y;
    this.ctx = gameArea.context;
    this.font = font;
    this.color = color;
    this.update = function () {
        this.text = text;
        this.ctx.font = this.font;
        this.ctx.fillStyle = this.color;
        this.ctx.fillText(this.text, this.x, this.y);
    }
}