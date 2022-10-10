
/*
//ver 1. 위아래로 움직임
window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight;

	var centerY = height * .5,
		centerX = width * .5,
		offset = height * 0.4,
		speed = 0.1,
		angle = 0;

	render();

	function render() {
		var y = centerY + Math.sin(angle) * offset;

		context.clearRect(0, 0, width, height);
		context.beginPath();
		context.arc(centerX, y, 50, 0, Math.PI * 2, false);
		context.fill();

		angle += speed;

		requestAnimationFrame(render);
	}
};
*/




/*
//ver 2. 커졌다 작아졌다
window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight;

	var centerY = height * .5,
		centerX = width * .5,
		baseRadius = 100,
		offset = 50,
		speed = 0.1,
		angle = 0;

	render();

	function render() {
		var radius = baseRadius + Math.sin(angle) * offset;

		context.fillStyle = "rgba(0, 0, 0, " + radius + ")";

		context.clearRect(0, 0, width, height);
		context.beginPath();
		context.arc(centerX, centerY, radius, 0, Math.PI * 2, false);
		context.fill();

		angle += speed;

		requestAnimationFrame(render);
	}
};
*/


//ver 3. 깜빡임
window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight;

	var centerY = height * .5,
		centerX = width * .5,
		baseAlpha = 0.5,
		offset = 0.5,
		speed = 0.1,
		angle = 0;

	render();

	function render() {
		var alpha = baseAlpha + Math.sin(angle) * offset;

		context.fillStyle = "rgba(0, 0, 0, " + alpha + ")";

		context.clearRect(0, 0, width, height);
		context.beginPath();
		context.arc(centerX, centerY, 100, 0, Math.PI * 2, false);
		context.fill();

		angle += speed;

		requestAnimationFrame(render);
	}
};
