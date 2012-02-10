
var addGhostHead = (function() {

    var coords = [
        0,6,
        1,3,
        2,2,
        3,1,
        4,1,
        5,0,
        8,0,
        9,1,
        10,1,
        11,2,
        12,3,
        13,6,
    ];

    return function(ctx) {
        var i;
        ctx.moveTo(coords[0],coords[1]);
        for (i=2; i<coords.length; i+=2)
            ctx.lineTo(coords[i],coords[i+1]);
    };
})();

var addGhostFeet1 = (function(){
    var coords = [
        13,13,
        11,11,
        9,13,
        8,13,
        8,11,
        5,11,
        5,13,
        4,13,
        2,11,
        0,13,
    ];

    return function(ctx) {
        var i;
        for (i=0; i<coords.length; i+=2)
            ctx.lineTo(coords[i],coords[i+1]);
    };

})();

var addGhostFeet2 = (function(){
    var coords = [
        13,12,
        12,13,
        11,13,
        9,11,
        7,13,
        6,13,
        4,11,
        2,13,
        1,13,
        0,12,
    ];

    return function(ctx) {
        var i;
        for (i=0; i<coords.length; i+=2)
            ctx.lineTo(coords[i],coords[i+1]);
    };

})();

var addGhostEyes = function(ctx,dirEnum){
    var i;

    ctx.save();
    ctx.translate(2,3);

    if (dirEnum == DIR_LEFT) ctx.translate(-1,0);
    else if (dirEnum == DIR_RIGHT) ctx.translate(1,0);
    else if (dirEnum == DIR_UP) ctx.translate(0,-1);
    else if (dirEnum == DIR_DOWN) ctx.translate(0,1);

    ctx.fillStyle = "#FFF";
    ctx.fillRect(1,0,2,5);
    ctx.fillRect(0,1,4,3);
    ctx.translate(6,0);
    ctx.fillRect(1,0,2,5);
    ctx.fillRect(0,1,4,3);

    if (dirEnum == DIR_LEFT) ctx.translate(0,2);
    else if (dirEnum == DIR_RIGHT) ctx.translate(2,2);
    else if (dirEnum == DIR_UP) ctx.translate(1,0);
    else if (dirEnum == DIR_DOWN) ctx.translate(1,3);

    ctx.fillStyle = "#00F";
    ctx.fillRect(0,0,2,2);
    ctx.translate(-6,0);
    ctx.fillRect(0,0,2,2);

    ctx.restore();
};

var addScaredGhostFace = function(ctx,flash){
    ctx.fillStyle = flash ? "#F00" : "#FF0";
    ctx.fillRect(4,5,2,2);
    ctx.fillRect(8,5,2,2);

    ctx.fillRect(1,10,1,1);
    ctx.fillRect(12,10,1,1);
    ctx.fillRect(2,9,2,1);
    ctx.fillRect(6,9,2,1);
    ctx.fillRect(10,9,2,1);
    ctx.fillRect(4,10,2,1);
    ctx.fillRect(8,10,2,1);
};

var addPacmanBody = function(ctx,dirEnum,angle,mouthShift,scale,centerShift) {
    if (mouthShift == undefined) mouthShift = 0;
    if (centerShift == undefined) centerShift = 0;
    if (scale == undefined) scale = 1;

    ctx.save();

    var d90 = Math.PI/2;
    if (dirEnum == DIR_UP) ctx.rotate(3*d90);
    else if (dirEnum == DIR_RIGHT) ctx.rotate(0);
    else if (dirEnum == DIR_DOWN) ctx.rotate(d90);
    else if (dirEnum == DIR_LEFT) ctx.rotate(2*d90);

    ctx.moveTo(-3+mouthShift,0);
    ctx.arc(centerShift,0,6*scale,angle,2*Math.PI-angle);

    ctx.restore();
};
