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
		//angle이 늘어나면서, alpha가 커지고 작아진다.
		var alpha = baseAlpha + Math.sin(angle) * offset;

		context.fillStyle = "rgba(0, 0, 0, " + alpha + ")";

		//원을 그리는 코드
		context.clearRect(0, 0, width, height);
		context.beginPath();
		context.arc(centerX, centerY, 100, 0, Math.PI * 2, false);
		context.fill();

		//angle이 커지는 속도를 여기서 정한다. 
		angle += speed;

		requestAnimationFrame(render);
	}
};