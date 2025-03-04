
window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight;

	var p0 = {
			x: 100,
			y: 100
		},
		p1 = {
			x: 500,
			y: 500
		},
		p2 = {
			x: 600,
			y: 50
		},
		p3 = {
			x: 80,
			y: 600
		},
		clickPoint;

	document.body.addEventListener("mousedown", onMouseDown);

	function onMouseDown(event) {
		clickPoint = getClickPoint(event.clientX, event.clientY);
		if(clickPoint) {
			document.body.addEventListener("mousemove", onMouseMove);
			document.body.addEventListener("mouseup", onMouseUp);
		}
	}

	function onMouseMove(event) {
		clickPoint.x = event.clientX;
		clickPoint.y = event.clientY;
		render();
	}

	function onMouseUp(event) {
		document.body.removeEventListener("mousemove", onMouseMove);
		document.body.removeEventListener("mouseup", onMouseUp);
	}

	function getClickPoint(x, y) {
		var points = [p0, p1, p2, p3];
		for(var i = 0; i < points.length; i++) {
			var p = points[i],
				dx = p.x - x,
				dy = p.y - y,
				dist = Math.sqrt(dx * dx + dy * dy);
			if(dist < 10) {
				return p;
			}

		}
	}


	render();

	function render() {
		context.clearRect(0, 0, width, height);

		drawPoint(p0);
		drawPoint(p1);
		drawPoint(p2);
		drawPoint(p3);

		context.beginPath();
		context.moveTo(p0.x, p0.y);
		context.lineTo(p1.x, p1.y);
		context.moveTo(p2.x, p2.y);
		context.lineTo(p3.x, p3.y);
		context.stroke();

		var intersect = lineIntersect(p0, p1, p2, p3);

		context.beginPath();
		context.arc(intersect.x, intersect.y, 20, 0, Math.PI * 2, false);
		context.stroke();
	}

	function drawPoint(p) {
		context.beginPath();
		context.arc(p.x, p.y, 10, 0, Math.PI * 2, false);
		context.fill();
	}


	//두 line의 intersection point를 구하는 함수는 아래에 자세히 설명되어있음 
	//https://youtu.be/4bIsntTiKfM?t=540
	function lineIntersect(p0, p1, p2, p3) {
		var A1 = p1.y - p0.y,
			B1 = p0.x - p1.x,
			C1 = A1 * p0.x + B1 * p0.y,

			A2 = p3.y - p2.y,
			B2 = p2.x - p3.x,
			C2 = A2 * p2.x + B2 * p2.y,

			denominator = A1 * B2 - A2 * B1;

		return {
			x: (B2 * C1 - B1 * C2) / denominator,
			y: (A1 * C2 - A2 * C1) / denominator
		}
	}

};