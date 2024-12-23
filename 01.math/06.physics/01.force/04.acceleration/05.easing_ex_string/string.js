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
		numPoints = 50, //이게 라인안에 끊어진 점의 갯수인데, 이게 커질수록 더 촘촘해서 부드럽게 보인다.
		ease = 0.25;

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

		//이어진 라인을 그리기 시작하는데,
		context.beginPath();
		//첫 시작점부터 시작해서 
		context.moveTo(leader.x, leader.y);

		for(var i = 0; i < numPoints; i++) {
			var point = points[i];
			//그 다음 에 이어지는 점들의 위치를 구할 때, 그 차이에 ease를 곱한만큼 dx만큰 x,y를 정한다. 
			point.x += (leader.x - point.x) * ease;
			point.y += (leader.y - point.y) * ease;

			//라인을 이어준다.
			context.lineTo(point.x, point.y);

			//그 다음 점을 다음 점의 시작점으로 설정한다음
			leader.x = point.x;
			leader.y = point.y;
		}

		context.stroke();

		requestAnimationFrame(update);
	}

};