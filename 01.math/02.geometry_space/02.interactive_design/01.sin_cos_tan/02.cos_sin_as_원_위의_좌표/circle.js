window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight,

		centerX = width / 2,
		centerY = height / 2,
		radius = 200,
		angle = 0,
		numObjects = 20,
		slice = Math.PI * 2 / numObjects, //원의 갯수만큼 360도에서 부터 쪼갬 
		x, y;

	for(var i = 0; i < numObjects; i += 1) {
		angle = i * slice;
		x = centerX + Math.cos(angle) * radius; //cos,sin으로 좌표 x,y 정함. radius를 곱하는건 원점에서 떨어진 정도. 
		y = centerY + Math.sin(angle) * radius; //sin은 y축 좌표 
		context.beginPath();
		context.arc(x, y, 10, 0, Math.PI * 2, false);
		context.fill();
	}
};