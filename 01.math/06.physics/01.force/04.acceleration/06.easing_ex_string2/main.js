window.onload = function() {
	var canvas = document.getElementById("canvas"),
		context = canvas.getContext("2d"),
		width = canvas.width = window.innerWidth,
		height = canvas.height = window.innerHeight,

		target = {
			x: width,
			y: Math.random() * height
		},

		points = [],
		numPoints = 100,
		ease = 0.5;

	for(var i = 0; i < numPoints; i++) {
		points.push({
			x: 0,
			y: 0
		});
	}

	update();

	document.body.addEventListener("mousemove", function(event) {
		target.x = event.clientX;
		target.y = event.clientY;
	});

	function update() {
		context.clearRect(0, 0, width, height);

		var leader = {
			x: target.x,
			y: target.y
		};

		for(var i = 0; i < numPoints; i++) {
			var point = points[i];
			point.x += (leader.x - point.x) * ease;
			point.y += (leader.y - point.y) * ease;

			context.beginPath();
			//이게 string1과 다른점은, 라인으로 그린게 아니라, 각 점을 원으로 표현한 것 
			context.arc(point.x, point.y, 10, 0, Math.PI * 2, false);
			context.fill();

			leader.x = point.x;
			leader.y = point.y;
		}


		requestAnimationFrame(update);
	}

};