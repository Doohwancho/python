
window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight;

	var points = [],
		bounce = 0.9,
		gravity = 0.5,
		friction = 0.999;

	points.push({
		x: 100,
		y: 100,
		oldx: 95,
		oldy: 95
	});



	update();

	function update() {
		updatePoints();
		renderPoints();
		requestAnimationFrame(update);
	}

	function updatePoints() {
		for(var i = 0; i < points.length; i++) {
			var p = points[i],
				vx = (p.x - p.oldx) * friction,
				//벡터로 한게 아니라, 위아래 개념이라, 하강은 y값을 뺴주는거고, bounce는 y값을 더해주는 식으로 구현되었음.
				vy = (p.y - p.oldy) * friction;

			p.oldx = p.x;
			p.oldy = p.y;
			p.x += vx;
			p.y += vy;
			p.y += gravity;

			if(p.x > width) {
				p.x = width;
				p.oldx = p.x + vx * bounce;
			}
			else if(p.x < 0) {
				p.x = 0;
				p.oldx = p.x + vx * bounce;
			}
			if(p.y > height) {
				p.y = height;
				//벡터로 한게 아니라, 위아래 개념이라, 하강은 y값을 뺴주는거고, bounce는 y값을 더해주는 식으로 구현되었음.
				p.oldy = p.y + vy * bounce;
			}
			else if(p.y < 0) {
				p.y = 0;
				//벡터로 한게 아니라, 위아래 개념이라, 하강은 y값을 뺴주는거고, bounce는 y값을 더해주는 식으로 구현되었음.
				p.oldy = p.y + vy * bounce;
			}
		}
	}

	function renderPoints() {
		context.clearRect(0, 0, width, height);
		for(var i = 0; i < points.length; i++) {
			var p = points[i];
			context.beginPath();
			context.arc(p.x, p.y, 5, 0, Math.PI * 2);
			context.fill();
		}
	}
};