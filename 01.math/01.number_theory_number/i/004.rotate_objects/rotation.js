window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    
    const colors = {
        triangle: "#ff0000",    // Red for triangle
        square: "#00ff00",     // Green for square
        star: "#0088ff",       // Blue for star
        grid: "#333333",       // Dark gray for grid
        axis: "#ffffff",       // White for axes
        text: "#ffffff"        // White for text
    };

    // Shape definitions (as complex numbers relative to their centers)
    const shapes = {
        triangle: [
            {x: 0, y: 0.5},            // Top
            {x: -0.433, y: -0.25},     // Bottom left
            {x: 0.433, y: -0.25}       // Bottom right
        ],
        square: [
            {x: -0.35, y: 0.35},      // Top left
            {x: 0.35, y: 0.35},       // Top right
            {x: 0.35, y: -0.35},      // Bottom right
            {x: -0.35, y: -0.35}      // Bottom left
        ],
        star: [
            {x: 0, y: 0.5},           // Top point
            {x: 0.1, y: 0.2},
            {x: 0.4, y: 0.2},         // Right top point
            {x: 0.15, y: 0},
            {x: 0.3, y: -0.3},        // Right bottom point
            {x: 0, y: -0.1},
            {x: -0.3, y: -0.3},       // Left bottom point
            {x: -0.15, y: 0},
            {x: -0.4, y: 0.2},        // Left top point
            {x: -0.1, y: 0.2}
        ]
    };

    // Position offsets for each shape
    const positions = {
        triangle: {x: -scale * 2, y: scale},
        square: {x: 0, y: scale},
        star: {x: scale * 2, y: scale}
    };
    
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

    function drawShape(points, rotator, position, color, shapeName) {
        if (points.length < 2) return;

        // Rotate and transform all points
        const transformedPoints = points.map(point => {
            const rotated = complexMultiply(point, rotator);
            return {
                x: (rotated.x * scale) + position.x,
                y: (rotated.y * scale) + position.y
            };
        });

        // Draw filled shape with transparency
        context.beginPath();
        context.moveTo(transformedPoints[0].x, transformedPoints[0].y);
        for (let i = 1; i < transformedPoints.length; i++) {
            context.lineTo(transformedPoints[i].x, transformedPoints[i].y);
        }
        context.closePath();
        context.fillStyle = color + '40'; // Add transparency
        context.fill();

        // Draw shape outline
        context.beginPath();
        context.moveTo(transformedPoints[0].x, transformedPoints[0].y);
        for (let i = 1; i < transformedPoints.length; i++) {
            context.lineTo(transformedPoints[i].x, transformedPoints[i].y);
        }
        context.closePath();
        context.strokeStyle = color;
        context.lineWidth = 2;
        context.stroke();

        // Draw rotation center
        context.beginPath();
        context.arc(position.x, position.y, 3, 0, Math.PI * 2);
        context.fillStyle = color;
        context.fill();

        // Add label
        context.save();
        context.scale(1, -1);
        context.font = "14px Arial";
        context.fillStyle = color;
        context.fillText(shapeName, position.x - 20, -position.y - scale * 0.8);
        context.restore();
    }

    function drawRotation(angle) {
        // Clear canvas
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        drawGrid();

        // Create rotation complex number
        const rotator = {
            x: Math.cos(angle),
            y: Math.sin(angle)
        };

        // Draw all shapes
        drawShape(shapes.triangle, rotator, positions.triangle, colors.triangle, "Triangle");
        drawShape(shapes.square, rotator, positions.square, colors.square, "Square");
        drawShape(shapes.star, rotator, positions.star, colors.star, "Star");

        // Add explanatory text
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = colors.text;

        // Title
        context.fillText("복소수를 이용한 도형 회전", -width/3, -height/2 + 30);
        context.fillText("(Shape Rotation using Complex Numbers)", -width/3, -height/2 + 50);
        
        // Angle and formula
        const degrees = (angle * 180 / Math.PI).toFixed(1);
        context.fillText(`Rotation Angle: ${degrees}°`, -width/3, -height/2 + 80);
        context.fillText(`z' = z · (${rotator.x.toFixed(3)} + ${rotator.y.toFixed(3)}i)`, -width/3, -height/2 + 110);

        // Explanation
        context.fillText("Each shape rotates around its center point", -width/3, height/2 - 60);
        context.fillText("z represents each vertex as a complex number", -width/3, height/2 - 30);

        // Animation state
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