window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    // Define margins
    const margin = {
        left: 50,
        right: 50,
        top: 50,
        bottom: 50,
    };

    // Calculate plotting area
    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;

    // Move origin to center of plotting area
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Draw axes
    drawAxes();

    // Plot sine, cosine, and tangent
    for (let angle = -Math.PI * 2; angle < Math.PI * 2; angle += 0.01) {
        const x = angle * 200;

        // Plot sine
        let y = Math.sin(angle) * 200;
        context.fillStyle = "black";
        context.fillRect(x, y, 5, 5);

        // Plot cosine
        y = Math.cos(angle) * 200;
        context.fillStyle = "red";
        context.fillRect(x, y, 5, 5);

        // Plot tangent, handle vertical asymptotes
        if (Math.abs(Math.cos(angle)) > 0.01) {
            y = Math.tan(angle) * 200;
            if (Math.abs(y) < plotHeight / 2) {
                context.fillStyle = "blue";
                context.fillRect(x, y, 5, 5);
            }
        }
    }

    function drawAxes() {
        context.save();
        context.scale(1, -1); // Flip back for text

        // Set axis style
        context.strokeStyle = "#000";
        context.lineWidth = 2;
        context.font = "14px Arial";
        context.textAlign = "center";

        // Draw X axis
        context.beginPath();
        context.moveTo(-plotWidth / 2, 0);
        context.lineTo(plotWidth / 2, 0);
        context.stroke();

        // Draw X axis ticks and labels
        // for (let x = -Math.PI * 2 * 200; x <= Math.PI * 2 * 200; x += 200) {
        //     context.beginPath();
        //     context.moveTo(x, -5);
        //     context.lineTo(x, 5);
        //     context.stroke();
        //     context.fillText((x / 200).toFixed(1) + "π", x, 20);
        // }
        for (let x = -Math.PI * 2 * 200; x <= Math.PI * 2 * 200; x += Math.PI * 200) {
            const value = (x / (Math.PI * 200)).toFixed(0); // Calculate multiples of π
            context.fillText((value === "0" ? "" : value) + "π", x, 20);
        }

        // Draw Y axis
        context.beginPath();
        context.moveTo(0, -plotHeight / 2);
        context.lineTo(0, plotHeight / 2);
        context.stroke();

        // Draw Y axis ticks and labels
        for (let y = -200; y <= 200; y += 100) {
            context.beginPath();
            context.moveTo(-5, -y);
            context.lineTo(5, -y);
            context.stroke();
            if (y !== 0) {
                context.fillText(y / 200, -25, -y);
            }
        }

        // Axis labels
        context.fillStyle = "black";
        context.font = "16px Arial";
        context.fillText("x (radians in π)", plotWidth / 3, 40);
        context.save();
        context.translate(-40, 0);
        context.rotate(-Math.PI / 2);
        // context.fillText("sin(x) / cos(x) / tan(x)", 0, 0);
        context.restore();

        // Legend - moved to upper right quadrant
        const legendX = plotWidth / 3;
        const legendY = -plotHeight / 3;

        context.fillStyle = "black";
        context.fillRect(legendX, legendY, 20, 10);
        context.fillText("sin(x)", legendX + 60, legendY + 5);

        context.fillStyle = "red";
        context.fillRect(legendX, legendY + 20, 20, 10);
        context.fillText("cos(x)", legendX + 60, legendY + 25);

        context.fillStyle = "blue";
        context.fillRect(legendX, legendY + 40, 20, 10);
        context.fillText("tan(x)", legendX + 60, legendY + 45);

        context.restore();
    }
};