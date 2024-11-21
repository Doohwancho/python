window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    
    const colors = {
        regular: "#ff0000",    // Red for regular rotation
        complex: "#00ff00",    // Green for complex rotation
        grid: "#333333",       // Dark gray for grid
        axis: "#ffffff",       // White for axes
        text: "#ffffff"        // White for text
    };
    
    // Center origin
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Complex number multiplication function
    function complexMultiply(z1, z2) {
        return {
            x: z1.x * z2.x - z1.y * z2.y,
            y: z1.x * z2.y + z1.y * z2.x
        };
    }

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
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

    // Function to draw a simple arrow
    function drawArrow(x, y, angle, color, label) {
        const length = scale;
        const headLength = scale / 5;
        const headAngle = Math.PI / 6;

        context.save();
        context.strokeStyle = color;
        context.fillStyle = color;
        context.lineWidth = 2;

        // Translate to the position and rotate
        context.translate(x, y);
        context.rotate(angle);

        // Draw the main line
        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(length, 0);
        context.stroke();

        // Draw the arrowhead
        context.beginPath();
        context.moveTo(length, 0);
        context.lineTo(length - headLength * Math.cos(-headAngle), 
                      headLength * Math.sin(-headAngle));
        context.lineTo(length - headLength * Math.cos(headAngle), 
                      -headLength * Math.sin(headAngle));
        context.closePath();
        context.fill();

        // Add label
        context.scale(1, -1);
        context.font = "14px Arial";
        context.fillStyle = color;
        context.fillText(label, length/2, -10);

        context.restore();
    }

    function drawRotation(angle) {
        // Clear canvas
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        drawGrid();
        drawUnitCircle();

        // Create rotation complex number (e^(iθ) = cos(θ) + i*sin(θ))
        const rotator = {
            x: Math.cos(angle),
            y: Math.sin(angle)
        };

        // Original vector (1 + 0i)
        const original = { x: 1, y: 0 };

        // Rotate using complex multiplication
        const rotated = complexMultiply(original, rotator);

        // Draw original and rotated vectors using both methods
        drawArrow(0, 0, 0, colors.regular, "Original Vector");
        
        // Draw rotated vector using complex multiplication
        drawArrow(0, 0, angle, colors.complex, "Rotated Vector (z₁·z₂)");

        // Add explanatory text
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = colors.text;

        // Title
        context.fillText("복소평면에서의 회전 (Rotation in Complex Plane)", -width/3, -height/2 + 30);
        
        // Angle information
        const degrees = (angle * 180 / Math.PI).toFixed(1);
        context.fillText(`Rotation Angle: ${degrees}°`, -width/3, -height/2 + 60);

        // Complex number representation
        context.fillText("z₁ = 1 + 0i (original vector)", -width/3, -height/2 + 90);
        context.fillText(`z₂ = ${rotator.x.toFixed(3)} + ${rotator.y.toFixed(3)}i (rotation)`, -width/3, -height/2 + 120);
        context.fillText(`z₁·z₂ = ${rotated.x.toFixed(3)} + ${rotated.y.toFixed(3)}i (result)`, -width/3, -height/2 + 150);

        // Formula explanation
        context.fillText("Rotation Formula: z₁·z₂ = (a + bi)(cos(θ) + i·sin(θ))", -width/3, height/2 - 60);
        context.fillText("= (a·cos(θ) - b·sin(θ)) + i(a·sin(θ) + b·cos(θ))", -width/3, height/2 - 30);

        context.restore();

        // Animation state
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
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

    // Add keyboard event listener
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

    // Start animation
    animate();
};