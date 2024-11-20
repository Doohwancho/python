window.onload = function() {
    // Canvas 1: Vertical movement
    const canvas1 = document.getElementById("canvas1"),
          context1 = canvas1.getContext("2d"),
          width1 = canvas1.width = window.innerWidth / 3,
          height1 = canvas1.height = window.innerHeight;
    let angle1 = 0, speed1 = 0.1;
    const centerY1 = height1 * 0.5,
          centerX1 = width1 * 0.5,
          offset1 = height1 * 0.4;

    function render1() {
        const y = centerY1 + Math.sin(angle1) * offset1; //sin()으로 공 위 아래로 움직이기 
        context1.clearRect(0, 0, width1, height1);
        context1.beginPath();
        context1.arc(centerX1, y, 50, 0, Math.PI * 2);
        context1.fill();
        angle1 += speed1;
        requestAnimationFrame(render1);
    }

    // Canvas 2: Size change
    const canvas2 = document.getElementById("canvas2"),
          context2 = canvas2.getContext("2d"),
          width2 = canvas2.width = window.innerWidth / 3,
          height2 = canvas2.height = window.innerHeight;
    let angle2 = 0, speed2 = 0.1;
    const centerY2 = height2 * 0.5,
          centerX2 = width2 * 0.5,
          baseRadius = 100,
          offset2 = 50;

    function render2() {
        const radius = baseRadius + Math.sin(angle2) * offset2; //radius가 커졌다 작아졌다 비율이 sin() 
        context2.clearRect(0, 0, width2, height2);
        context2.beginPath();
        context2.arc(centerX2, centerY2, radius, 0, Math.PI * 2);
        context2.fill();
        angle2 += speed2;
        requestAnimationFrame(render2);
    }

    // Canvas 3: Blinking effect
    const canvas3 = document.getElementById("canvas3"),
          context3 = canvas3.getContext("2d"),
          width3 = canvas3.width = window.innerWidth / 3,
          height3 = canvas3.height = window.innerHeight;
    let angle3 = 0, speed3 = 0.1;
    const centerY3 = height3 * 0.5,
          centerX3 = width3 * 0.5,
          baseAlpha = 0.5,
          offset3 = 0.5;

    function render3() {
        const alpha = baseAlpha + Math.sin(angle3) * offset3; //blinking effect 되는 정도가 sin()
        context3.fillStyle = `rgba(0, 0, 0, ${alpha})`;
        context3.clearRect(0, 0, width3, height3);
        context3.beginPath();
        context3.arc(centerX3, centerY3, 100, 0, Math.PI * 2);
        context3.fill();
        angle3 += speed3;
        requestAnimationFrame(render3);
    }

    // Start rendering all three animations
    render1();
    render2();
    render3();
};
