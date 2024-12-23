/*
---
원리

1. 공간에 bitmap grid를 그린다.
2. 그 격자에서 내가 칠한 곳은 1, 안칠한 곳은 0으로 값을 둔다.
3. 만약 물체가 이동하다가, 저 bitmap grid에 1인 값을 detect하면, 충돌한 것이라 판단한다.

*/


window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		targetCanvas = document.getElementById("target"),
		targetContext = targetCanvas.getContext("2d"),
		width = canvas.width = targetCanvas.width = window.innerWidth,
		height = canvas.height = targetCanvas.height = window.innerHeight,
		p = particle.create(0, height / 2, 10, 0);

	targetContext.beginPath();
	targetContext.arc(width / 2, height / 2, 200, 0, Math.PI * 2, false);
	targetContext.fill();	

	update();

	function update() {
		context.clearRect(0, 0, width, height);

		p.update();
		context.beginPath();
		context.arc(p.x, p.y, 4, 0, Math.PI * 2, false);
		context.fill();

		var imageData = targetContext.getImageData(p.x, p.y, 1, 1);
		if(imageData.data[3] > 0) {
			targetContext.globalCompositeOperation = "destination-out";
			targetContext.beginPath();
			targetContext.arc(p.x, p.y, 20, 0, Math.PI * 2, false);
			targetContext.fill();

			resetParticle();
		}
		else if(p.x > width) {
			resetParticle();
		}
		requestAnimationFrame(update);
	}

	function resetParticle() {
		p.x = 0;
		p.y = height / 2;
		p.setHeading(utils.randomRange(-0.1, 0.1));
	}
};