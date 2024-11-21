window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    
    const colors = {
        vector1: "#ff0000",    // Red for first vector
        vector2: "#00ff00",    // Green for second vector
        vector3: "#0088ff",    // Blue for third vector
        real: "#ff8800",       // Orange for real components
        imaginary: "#ff00ff",  // Magenta for imaginary components
        grid: "#333333",       // Dark gray for grid
        axis: "#ffffff",       // White for axes
        text: "#ffffff"        // White for text
    };
    
    // Initial vectors
    const vectors = [
        { x: 1, y: 0, color: colors.vector1, label: "z₁" },
        { x: 0.7, y: 0.7, color: colors.vector2, label: "z₂" },
        { x: 0.5, y: -0.5, color: colors.vector3, label: "z₃" }
    ];
    
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    function complexMultiply(z1, z2) {
        return {
            x: z1.x * z2.x - z1.y * z2.y,
            y: z1.x * z2.y + z1.y * z2.x
        };
    }

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        for(let i = -width/2; i < width/2; i += scale) {
            context.beginPath();
            context.strokeStyle = i === 0 ? colors.axis : colors.grid;
            context.moveTo(i, -height/2);
            context.lineTo(i, height/2);
            context.stroke();
        }
        
        for(let i = -height/2; i < height/2; i += scale) {
            context.beginPath();
            context.strokeStyle = i === 0 ? colors.axis : colors.grid;
            context.moveTo(-width/2, i);
            context.lineTo(width/2, i);
            context.stroke();
        }
    }

    function drawUnitCircle() {
        context.strokeStyle = "rgba(255,255,255,0.3)";
        context.lineWidth = 1;
        context.beginPath();
        context.arc(0, 0, scale, 0, Math.PI * 2);
        context.stroke();
    }

    function drawVector(vector, rotator, color, label) {
        const rotated = complexMultiply(vector, rotator);
        const x = rotated.x * scale;
        const y = rotated.y * scale;

        // Draw real component (dashed)
        context.beginPath();
        context.strokeStyle = colors.real;
        context.setLineDash([5, 5]);
        context.moveTo(0, 0);
        context.lineTo(x, 0);
        context.stroke();
        context.setLineDash([]);

        // Draw imaginary component (dashed)
        context.beginPath();
        context.strokeStyle = colors.imaginary;
        context.setLineDash([5, 5]);
        context.moveTo(x, 0);
        context.lineTo(x, y);
        context.stroke();
        context.setLineDash([]);

        // Draw main vector
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;
        context.moveTo(0, 0);
        context.lineTo(x, y);
        
        // Arrow head
        const headLength = scale / 15;
        const angle = Math.atan2(y, x);
        context.lineTo(x - headLength * Math.cos(angle - Math.PI / 6),
                      y - headLength * Math.sin(angle - Math.PI / 6));
        context.moveTo(x, y);
        context.lineTo(x - headLength * Math.cos(angle + Math.PI / 6),
                      y - headLength * Math.sin(angle + Math.PI / 6));
        context.stroke();

        // Labels
        context.save();
        context.scale(1, -1);
        context.font = "14px Arial";
        context.fillStyle = color;
        const labelX = x * 1.1;
        const labelY = -y * 1.1;
        context.fillText(`${label} = ${rotated.x.toFixed(2)} + ${rotated.y.toFixed(2)}i`, labelX, labelY);
        
        // Component labels
        if (Math.abs(rotated.x) > 0.1) {
            context.fillStyle = colors.real;
            context.fillText(`Re(${label})`, x/2, 15);
        }
        if (Math.abs(rotated.y) > 0.1) {
            context.fillStyle = colors.imaginary;
            context.fillText(`Im(${label})`, x + 5, -y/2);
        }
        context.restore();

        return rotated;
    }

    function drawRotation(angle) {
        // Clear canvas
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        drawGrid();
        drawUnitCircle();

        // Create rotation complex number
        const rotator = {
            x: Math.cos(angle),
            y: Math.sin(angle)
        };

        // Draw all vectors with their components
        const rotatedVectors = vectors.map(v => 
            drawVector(v, rotator, v.color, v.label));

        // Add explanatory text
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = colors.text;

        // Title and angle
        context.fillText("복소평면에서의 다중 벡터 회전", -width/3, -height/2 + 30);
        context.fillText("(Multiple Vector Rotation in Complex Plane)", -width/3, -height/2 + 50);
        
        const degrees = (angle * 180 / Math.PI).toFixed(1);
        context.fillText(`Rotation Angle: ${degrees}°`, -width/3, -height/2 + 80);

        // Complex rotation formula
        context.fillText("Rotation: z' = z · (cos θ + i·sin θ)", -width/3, -height/2 + 110);
        context.fillText(`cos θ + i·sin θ = ${rotator.x.toFixed(3)} + ${rotator.y.toFixed(3)}i`, -width/3, -height/2 + 130);

        // Component explanation
        context.fillText("Components:", -width/3, -height/2 + 160);
        context.fillStyle = colors.real;
        context.fillText("Real part (Re)", -width/3 + 100, -height/2 + 160);
        context.fillStyle = colors.imaginary;
        context.fillText("Imaginary part (Im)", -width/3 + 220, -height/2 + 160);

        // Animation state
        context.fillStyle = colors.text;
        context.fillText(
            isAnimating ? "Press SPACE to pause" : "Press SPACE to resume", 
            -width/2 + 20, 
            -height/2 + 30
        );

        context.restore();
    }

    let angle = 0;

    function animate() {
        if (isAnimating) {
            angle += 0.01;
            if(angle > Math.PI * 2) angle = 0;
            
            drawRotation(angle);
            animationId = requestAnimationFrame(animate);
        }
    }

    document.addEventListener('keydown', function(event) {
        if (event.code === 'Space') {
            event.preventDefault();
            isAnimating = !isAnimating;
            
            if (isAnimating) {
                animate();
            } else {
                cancelAnimationFrame(animationId);
            }
        }
    });

    animate();
};