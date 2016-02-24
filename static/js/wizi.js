/**
 *wizi
 *On browser rendering of visualizations by image delivery
 *Handle Mouse Interaction Events & send them to the server over a websocket connection
*/
var wizi = {}; 

wizi.render = function(container){

	var mouse = {x:0,y:0};
	var triggerStartPosition = {x:0, y:0};
	var delta = {x:0,y:0};
	var distanceMoved = {x:0, y:0};
	var startPosition = {x:0, y:0};
	var websocket;
	var mouseEntered;

	function init(){
		container.style.color = '#999';
		width = container.offsetWidth; 
		height = container.offsetHeight;

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
		delta.y = mouse.y - startPosition.y;

		distanceMoved.x = Math.abs(delta.x);
		distanceMoved.y = Math.abs(delta.y);
		// console.log(mouse.x + "|" + mouse.y);
		// console.log("x:"+distanceMoved.x + "|" + delta.x)
		// console.log("y:"+distanceMoved.y + "|" + delta.y)

		if( distanceMoved.x > distanceMoved.y && delta.x > 0){
			websocketSend("right");
		} else if ( distanceMoved.x > distanceMoved.y && delta.x < 0){
			websocketSend("left");
		} else if ( distanceMoved.y > distanceMoved.x && delta.y > 0) {
			websocketSend("down");
		} else if ( distanceMoved.y > distanceMoved.x && delta.y < 0){
			websocketSend("up");
		}
		startPosition.x = mouse.x;
		startPosition.y = mouse.y;
	};

	function onMouseUp(event){
		console.log("stop")
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
	
	function OpenWebSocket(){

		var host = 'ws://localhost:8000/ws';
		websocket = new WebSocket(host);
		websocket.onopen = function(evt){
			websocket.send("connection open");
			init();
		};
		websocket.onmessage = function(evt){};
		websocket.onclose = function(evt){};
	};

	function websocketSend(message){
		websocket.send(message);
	};
	
	function start(){
		OpenWebSocket();
	};
	
	this.start = start;
	return this;
}

canvas = document.getElementById('canva');

var renderer = new wizi.render(canvas);
// wizi.render(canvas);
renderer.start();