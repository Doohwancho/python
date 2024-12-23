/*
Q. what is easing?

Easing refers to the gradual acceleration or deceleration of motion in animations, 
making transitions feel more natural. 
Instead of linear progression, easing functions like 
"ease-in," "ease-out," and "ease-in-out" adjust speed dynamically.

*/

window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight,

		target = {
			x: width,
			y: Math.random() * height
		},

		position = {
			x: 0,
			y: Math.random() * height
		},

		// ease = 0.1;
		ease = 0.05;

	update();

	document.body.addEventListener("mousemove", function(event) {
		target.x = event.clientX;
		target.y = event.clientY;
	});

	function update() {
		context.clearRect(0, 0, width, height);

		context.beginPath();
		context.arc(position.x, position.y, 10, 0, Math.PI * 2, false);
		context.fill();


		var dx = target.x - position.x, //얼만큼 x만 큼 드래그 됬는지, change in x를 측정. 
										//근데 공이 접근할 수록 마우스 위치랑 고정점 사이의 거리가 줄어들어서 0에 가까워진다.
										//따라서 속도도 역시 줄어들게 된다.
			dy = target.y - position.y,
			vx = dx * ease, //속도의 증감은 ease로 조절한다. 1이면 바로 따라오는데, 0.1이면 천천히 따라온다.
			vy = dy * ease; 

		position.x += vx; //dx에 ease로 속도 조절한걸 더해준다. 
		position.y += vy;


		requestAnimationFrame(update);
	}

};