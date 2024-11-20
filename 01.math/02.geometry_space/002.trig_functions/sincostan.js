window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const margin = {
        left: 50,
        right: 50,
        top: 50,
        bottom: 50,
    };

    const plotWidth = width - margin.left - margin.right;
    const plotHeight = height - margin.top - margin.bottom;
    const scale = 200; // Scale factor for the unit circle and graphs

    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    function drawUnitCircle() {
        context.save();
        
        // Draw the circle
        context.beginPath();
        context.strokeStyle = "#666";
        context.lineWidth = 2;
        context.arc(0, 0, scale, 0, Math.PI * 2);
        context.stroke();

        // Draw radial lines for common angles
        const angles = [0, Math.PI/6, Math.PI/4, Math.PI/3, Math.PI/2, 
                       2*Math.PI/3, 3*Math.PI/4, 5*Math.PI/6, Math.PI];
        
        context.strokeStyle = "#999";
        context.lineWidth = 1;
        angles.forEach(angle => {
            context.beginPath();
            context.moveTo(0, 0);
            context.lineTo(Math.cos(angle) * scale, Math.sin(angle) * scale);
            context.stroke();

            // Add angle labels
            context.save();
            context.scale(1, -1);
            context.font = "12px Arial";
            context.fillStyle = "#666";
            const labelRadius = scale + 20;
            const labelX = Math.cos(angle) * labelRadius;
            const labelY = -Math.sin(angle) * labelRadius;
            context.fillText(`${(angle/Math.PI).toFixed(2)}π`, labelX, labelY);
            context.restore();
        });

        context.restore();
    }

    function drawInverseTrigFunctions() {
        context.save();

        // Draw arcsin
        context.strokeStyle = "rgba(0,0,0,0.5)";
        context.beginPath();
        for(let x = -1; x <= 1; x += 0.01) {
            const y = Math.asin(x);
            context.lineTo(x * scale, y * scale);
        }
        context.stroke();

        // Draw arccos
        context.strokeStyle = "rgba(255,0,0,0.5)";
        context.beginPath();
        for(let x = -1; x <= 1; x += 0.01) {
            const y = Math.acos(x);
            context.lineTo(x * scale, y * scale);
        }
        context.stroke();

        // Draw arctan
        context.strokeStyle = "rgba(0,0,255,0.5)";
        context.beginPath();
        for(let x = -5; x <= 5; x += 0.01) {
            const y = Math.atan(x);
            if(Math.abs(y * scale) < plotHeight/2) {
                context.lineTo(x * scale, y * scale);
            }
        }
        context.stroke();

        context.restore();
    }

    function drawAxes() {
        context.save();
        context.scale(1, -1);

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
        for (let x = -2 * Math.PI; x <= 2 * Math.PI; x += Math.PI/2) {
            const xPos = x * scale;
            context.beginPath();
            context.moveTo(xPos, -5);
            context.lineTo(xPos, 5);
            context.stroke();

            const value = (x/Math.PI).toFixed(1);
            context.fillText(value === "0.0" ? "0" : value + "π", xPos, 20);
        }

        // Draw Y axis
        context.beginPath();
        context.moveTo(0, -plotHeight / 2);
        context.lineTo(0, plotHeight / 2);
        context.stroke();

        // Draw Y axis ticks and labels
        for (let y = -Math.PI; y <= Math.PI; y += Math.PI/2) {
            const yPos = -y * scale;
            context.beginPath();
            context.moveTo(-5, yPos);
            context.lineTo(5, yPos);
            context.stroke();

            if(y !== 0) {
                const value = (y/Math.PI).toFixed(1);
                context.fillText(value + "π", -25, yPos);
            }
        }

        // Legend
        const legendX = plotWidth / 3;
        const legendY = -plotHeight / 3;

        // Original functions
        context.fillStyle = "black";
        context.fillRect(legendX, legendY, 20, 10);
        context.fillText("sin(x)", legendX + 60, legendY + 5);

        context.fillStyle = "red";
        context.fillRect(legendX, legendY + 20, 20, 10);
        context.fillText("cos(x)", legendX + 60, legendY + 25);

        context.fillStyle = "blue";
        context.fillRect(legendX, legendY + 40, 20, 10);
        context.fillText("tan(x)", legendX + 60, legendY + 45);

        // Reciprocal functions
        context.fillStyle = "green";
        context.fillRect(legendX, legendY + 60, 20, 10);
        context.fillText("sec(x)", legendX + 60, legendY + 65);

        context.fillStyle = "orange";
        context.fillRect(legendX, legendY + 80, 20, 10);
        context.fillText("csc(x)", legendX + 60, legendY + 85);

        context.fillStyle = "purple";
        context.fillRect(legendX, legendY + 100, 20, 10);
        context.fillText("cot(x)", legendX + 60, legendY + 105);


        // Inverse functions
        // context.fillStyle = "rgba(0,0,0,0.5)";
        // context.fillRect(legendX, legendY + 60, 20, 10);
        // context.fillText("arcsin(x)", legendX + 60, legendY + 65);

        // context.fillStyle = "rgba(255,0,0,0.5)";
        // context.fillRect(legendX, legendY + 80, 20, 10);
        // context.fillText("arccos(x)", legendX + 60, legendY + 85);

        // context.fillStyle = "rgba(0,0,255,0.5)";
        // context.fillRect(legendX, legendY + 100, 20, 10);
        // context.fillText("arctan(x)", legendX + 60, legendY + 105);

        context.restore();
    }

    // function drawTrigFunctions() {
    //     for (let angle = -Math.PI * 2; angle < Math.PI * 2; angle += 0.01) {
    //         const x = angle * scale;

    //         // Plot sine
    //         let y = Math.sin(angle) * scale;
    //         context.fillStyle = "black";
    //         context.fillRect(x, y, 2, 2);

    //         // Plot cosine
    //         y = Math.cos(angle) * scale;
    //         context.fillStyle = "red";
    //         context.fillRect(x, y, 2, 2);

    //         // Plot tangent
    //         if (Math.abs(Math.cos(angle)) > 0.01) {
    //             y = Math.tan(angle) * scale;
    //             if (Math.abs(y) < plotHeight / 2) {
    //                 context.fillStyle = "blue";
    //                 context.fillRect(x, y, 2, 2);
    //             }
    //         }
    //     }
    // }

    function drawTrigFunctions() {
        for (let angle = -Math.PI * 2; angle < Math.PI * 2; angle += 0.01) {
            const x = angle * scale;
    
            // Original functions
            // Plot sine
            let y = Math.sin(angle) * scale;
            context.fillStyle = "black";
            context.fillRect(x, y, 2, 2);
    
            // Plot cosine
            y = Math.cos(angle) * scale;
            context.fillStyle = "red";
            context.fillRect(x, y, 2, 2);
    
            // Plot tangent
            if (Math.abs(Math.cos(angle)) > 0.01) {
                y = Math.tan(angle) * scale;
                if (Math.abs(y) < plotHeight / 2) {
                    context.fillStyle = "blue";
                    context.fillRect(x, y, 2, 2);
                }
            }
    
            // Reciprocal functions
            // Plot cotangent (1/tan = cos/sin)
            if (Math.abs(Math.sin(angle)) > 0.01) {
                y = (Math.cos(angle) / Math.sin(angle)) * scale;
                if (Math.abs(y) < plotHeight / 2) {
                    context.fillStyle = "purple";
                    context.fillRect(x, y, 2, 2);
                }
            }
    
            // Plot secant (1/cos)
            if (Math.abs(Math.cos(angle)) > 0.01) {
                y = (1 / Math.cos(angle)) * scale;
                if (Math.abs(y) < plotHeight / 2) {
                    context.fillStyle = "green";
                    context.fillRect(x, y, 2, 2);
                }
            }
    
            // Plot cosecant (1/sin)
            if (Math.abs(Math.sin(angle)) > 0.01) {
                y = (1 / Math.sin(angle)) * scale;
                if (Math.abs(y) < plotHeight / 2) {
                    context.fillStyle = "orange";
                    context.fillRect(x, y, 2, 2);
                }
            }
        }
    }

    // Draw everything
    drawAxes();
    drawUnitCircle();
    drawTrigFunctions();
    // drawInverseTrigFunctions();
};