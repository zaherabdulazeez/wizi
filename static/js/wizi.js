/**
 *wizi
 *On browser rendering of visualizations by image delivery
 *Handle Mouse Interaction Events & send them to the server over a websocket connection
*/
// Handle Mouse Interaction Events & send them to the server over a websocket connection

var wizi = {} || wizi; 

wizi.interact = function(container,websocket){
	var mouse = {x:0,y:0};
	var triggerStartPosition = {x:0, y:0};
	var delta = {x:0,y:0};
	var distanceMoved = {x:0, y:0};
	var startPosition = {x:0, y:0};
	var mouseEntered;
	var Wwidth =container.offsetWidth; 
	var Wheight = container.offsetHeight;
	var angleFactor = {x:90/Wwidth, y:90/Wheight} //one unit delta.x results in angleFactor.x unit degree of azimuth change
	var azimuth,elevation;
	var data;

	function init(){
		console.log(Wwidth, Wheight)
		container.addEventListener('mouseover', function(){ mouseEntered = true;}, false);
		container.addEventListener('mouseout', function(){ mouseEntered = false;}, false);
		container.addEventListener('mousedown', onMouseDown, false);
		container.addEventListener('wheel',onMouseWheel, false);
		document.addEventListener('keydown', onKeyDown,false);
		window.addEventListener('resize', onWindowResize, false);
	};


	function onMouseDown(event){
		event.preventDefault();
		container.addEventListener('mousemove', onMouseMove, false);
		container.addEventListener('mouseup',onMouseUp,false);
		container.addEventListener('mouseout',onMouseOut,false);

		triggerStartPosition.x = event.clientX;
		triggerStartPosition.y = event.clientY;

		startPosition.x = triggerStartPosition.x;
		startPosition.y = triggerStartPosition.y;

		container.style.cursor = 'move';
		console.log("start");
	};

	function onMouseMove(event){
		// console.log("diff:"+startPosition.x +"|"+triggerStartPosition.x)
		mouse.x = event.clientX;
		mouse.y = event.clientY;

		delta.x = mouse.x - startPosition.x;
		delta.y = startPosition.y - mouse.y;

		// distanceMoved.x = Math.abs(delta.x);
		// distanceMoved.y = Math.abs(delta.y);

		//one unit delta.x results in angleFactor.x unit degree of azimuth change

		azimuth = delta.x * angleFactor.x;
		elevation = delta.y *angleFactor.y;

		if(Math.abs(azimuth)>5 || Math.abs(elevation)>5){
			console.log("sending...");
			data = JSON.stringify({azimuth:azimuth, elevation:elevation});
			websocket.send(data);
			startPosition.x = mouse.x;
			startPosition.y = mouse.y;
		}

			
		// console.log("X distance moved:"+distanceMoved.x);
		// console.log("Y distance moved:"+distanceMoved.y);
		// console.log("angle factor:"+angleFactor.x);
		// console.log("azimuth"+azimuth);
		// console.log("elevation"+elevation);

		// if(distanceMoved.x >5 && distanceMoved.y >5){
		// 	azimuth = delta.x*angleFactor.x;
		// 	elevation = delta.y*angleFactor.y;
		// 	data = JSON.stringify({azimuth:azimuth, elevation:elevation})
		// 	websocket.send(data)
		// 	startPosition.x = mouse.x;
		// 	startPosition.y = mouse.y;
		// }

		// if(distanceMoved.x > 2 && distanceMoved.y > 2){

		// 	if( distanceMoved.x > distanceMoved.y && delta.x > 0){
		// 		console.log("x:"+distanceMoved.x + "|" + delta.x);
		// 		websocket.send("right");
		// 	} else if ( distanceMoved.x > distanceMoved.y && delta.x < 0){
		// 		console.log("x:"+distanceMoved.x + "|" + delta.x);
		// 		websocket.send("left");
		// 	} else if ( distanceMoved.y > distanceMoved.x && delta.y > 0) {
		// 		console.log("y:"+distanceMoved.y + "|" + delta.y);
		// 		websocket.send("down");
		// 	} else if ( distanceMoved.y > distanceMoved.x && delta.y < 0){
		// 		console.log("y:"+distanceMoved.y + "|" + delta.y);
		// 		websocket.send("up");
		// 	}
		// 	startPosition.x = mouse.x;
		// 	startPosition.y = mouse.y;
	 //    }
	};

	function onMouseUp(event){
		console.log("mouseup");
		// if(Math.abs(azimuth)>5 || Math.abs(elevation)>5){
		// 	console.log("sending...");
		// 	data = JSON.stringify({azimuth:azimuth, elevation:elevation});
		// 	websocket.send(data);
		// 	startPosition.x = mouse.x;
		// 	startPosition.y = mouse.y;
		// }
		container.removeEventListener('mousemove', onMouseMove, false);
		container.removeEventListener('mouseup',onMouseUp, false);
		container.removeEventListener('mouseout', onMouseOut, false);
		container.style.cursor = 'auto';
	};

	function onMouseOut(event){

		container.removeEventListener('mousemove', onMouseMove, false);
		container.removeEventListener('mouseup',onMouseUp, false);
		container.removeEventListener('mouseout', onMouseOut, false);
		container.style.cursor = 'auto';
	};

	function onMouseWheel(event){
		// to be developed
	};

	function onKeyDown(event){
		// to be developed
	};

	function onWindowResize(event){
		// to be developed
	};
	
	this.start = init;
	return this;
}

wizi.websocket = function(){

	var host = 'ws://localhost:8000/ws';
	var	websocket = new WebSocket(host);
	console.log('WebSocket OK')
	return websocket;
}

wizi.wsCommunication = function(websocket,canvas){

	function init(){
		websocket.onopen = function(){
			wizi.draw_image_mode_ON(canvas);
			// websocket.send('{"open_msg":"connection open"}');
		};
		websocket.onmessage = function(msg){
			wizi.handleIncomingMessage(msg);
		};
		websocket.onclose = function(){};
		console.log('comm Start OK')
	};
	this.start = init;
	return this;
}

wizi.handleIncomingMessage = function(msg){
	base64data = msg.data;
	ImageObj.src = base64data;
	console.log(msg.data)
	return;
}

var ImageObj = new Image()

wizi.draw_image_mode_ON = function(container){
	var context = container.getContext("2d");
	container.width = container.offsetWidth
	container.height = container.offsetHeight
	//Thanks to http://stackoverflow.com/questions/23104582/scaling-an-image-to-fit-on-canvas
	ImageObj.onload = function(){
		Cwidth = container.width;
		Cheight = container.height;
		Iwidth = ImageObj.width;
		Iheight = ImageObj.height;
		var hRatio = Cwidth/Iwidth;
		var vRatio = Cheight/Iheight;
		var ratio = Math.min(hRatio,vRatio);
		var centerShift_x = (Cwidth - Iwidth*hRatio)/2;
		var centerShift_y = (Cheight - Iheight*vRatio)/2;
		context.clearRect(0,0, Cwidth, Cheight);
		// context.drawImage(ImageObj, 0, 0);
		context.drawImage(ImageObj, 0, 0, Iwidth, Iheight, centerShift_x, centerShift_y, Iwidth*hRatio, Iheight*vRatio);
		// context.drawImage(ImageObj, 0, 0, Iwidth, Iheight, centerShift_x, centerShift_y, Iwidth*ratio, Iheight*ratio);
		// context.drawImage(ImageObj, 0, 0, Iwidth, Iheight,0,0, Cwidth, Cheight);
		console.log('image loaded') 
	};
	console.log('draw image mode on OK')
}

wizi.drawCanvas = function(canvasDiv){
	
	var div = document.getElementById(canvasDiv);
	div.style.background = 'skyblue';
	div.style.width = '100%';
	div.style.height = '100%';
	var canvasElement = document.createElement('canvas');
	canvasElement.id = 'canvasId';
	div.appendChild(canvasElement);
	canvasElement.style.width = '100%';
	canvasElement.style.height = '100%';
	canvasElement.style.background = 'gray';
	console.log('canvas drawn OK')
	return canvasElement;
}

// plug in all the objects created above & make wizi run
var canvas = new wizi.drawCanvas('canva')
var ws = new wizi.websocket()
var comm = new wizi.wsCommunication(ws,canvas)
var iren = new wizi.interact(canvas,ws)
comm.start()
iren.start()
