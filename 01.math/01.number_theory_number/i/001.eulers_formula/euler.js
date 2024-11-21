window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 4;
    let isAnimating = true;
    let animationId = null;
    
    const colors = {
        real: "#ff0000",      // Red for real part (cos)
        imaginary: "#00ff00", // Green for imaginary part (sin)
        complex: "#ffffff",   // White for complex number
        grid: "#333333",      // Dark gray for grid
        axis: "#ffffff",      // White for axes
        unitMarker: "#888888" // Gray for unit markers
    };
    
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -width/2; i < width/2; i += scale/4) {
            context.beginPath();
            context.strokeStyle = i % scale === 0 ? "rgba(255,255,255,0.2)" : colors.grid;
            context.moveTo(i, -height/2);
            context.lineTo(i, height/2);
            context.stroke();
        }
        
        for(let i = -height/2; i < height/2; i += scale/4) {
            context.beginPath();
            context.strokeStyle = i % scale === 0 ? "rgba(255,255,255,0.2)" : colors.grid;
            context.moveTo(-width/2, i);
            context.lineTo(width/2, i);
            context.stroke();
        }
    }

    function drawUnitMarkers() {
        context.save();
        context.scale(1, -1);
        context.font = "14px Arial";
        context.textAlign = "center";
        context.fillStyle = colors.unitMarker;

        // X-axis unit markers
        context.fillText("1", scale + 15, 20);
        context.fillText("-1", -scale - 15, 20);
        
        // Y-axis unit markers
        context.fillText("i", 20, -scale - 5);
        context.fillText("-i", 20, scale + 15);

        // Draw tick marks
        context.strokeStyle = colors.unitMarker;
        context.lineWidth = 2;
        
        // X-axis ticks
        [-1, -0.5, 0.5, 1].forEach(x => {
            const xPos = x * scale;
            context.beginPath();
            context.moveTo(xPos, -5);
            context.lineTo(xPos, 5);
            context.stroke();
        });
        
        // Y-axis ticks
        [-1, -0.5, 0.5, 1].forEach(y => {
            const yPos = y * scale;
            context.beginPath();
            context.moveTo(-5, yPos);
            context.lineTo(5, yPos);
            context.stroke();
        });

        context.restore();
    }

    function drawAxes() {
        context.lineWidth = 2;
        
        // Real axis
        context.beginPath();
        context.strokeStyle = colors.axis;
        context.moveTo(-width/2, 0);
        context.lineTo(width/2, 0);
        context.stroke();
        
        // Imaginary axis
        context.beginPath();
        context.strokeStyle = colors.axis;
        context.moveTo(0, -height/2);
        context.lineTo(0, height/2);
        context.stroke();
        
        // Labels
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = colors.axis;
        context.fillText("Real", width/2 - 50, 20);
        context.fillText("Imaginary", 10, -height/2 + 20);
        
        // Add "복소평면" label
        context.font = "bold 20px Arial";
        context.fillText("복소평면 (Complex Plane)", -70, -height/2 + 50);
        context.restore();
    }

    function drawUnitCircle() {
        context.strokeStyle = "rgba(255,255,255,0.3)";
        context.lineWidth = 2;
        context.beginPath();
        context.arc(0, 0, scale, 0, Math.PI * 2);
        context.stroke();
    }

    function drawEulerFormula(angle) {
        // Clear canvas
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        drawGrid();
        drawAxes();
        drawUnitCircle();
        drawUnitMarkers();
        
        // Calculate point on unit circle
        const x = Math.cos(angle) * scale;  // Real part
        const y = Math.sin(angle) * scale;  // Imaginary part
        
        // Draw radius vector (e^(iθ))
        context.beginPath();
        context.strokeStyle = colors.complex;
        context.lineWidth = 2;
        context.moveTo(0, 0);
        context.lineTo(x, y);
        context.stroke();
        
        // Draw cos(θ) component
        context.beginPath();
        context.strokeStyle = colors.real;
        context.setLineDash([5, 5]);
        context.moveTo(0, 0);
        context.lineTo(x, 0);
        context.stroke();
        context.setLineDash([]);
        
        // Draw i*sin(θ) component
        context.beginPath();
        context.strokeStyle = colors.imaginary;
        context.setLineDash([5, 5]);
        context.moveTo(x, 0);
        context.lineTo(x, y);
        context.stroke();
        context.setLineDash([]);
        
        // Draw angle arc
        context.beginPath();
        context.strokeStyle = colors.complex;
        context.arc(0, 0, scale/4, 0, angle);
        context.stroke();
        
        // Labels and formula
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        
        // Angle label
        context.fillStyle = colors.complex;
        context.fillText(`θ = ${(angle * 180 / Math.PI).toFixed(1)}°`, scale/8, scale/8);
        
        // Euler's formula - moving with point
        const cosValue = Math.cos(angle).toFixed(3);
        const sinValue = Math.sin(angle).toFixed(3);
        const formulaX = x + 20;
        const formulaY = -(y + 20);
        
        // Background for formula
        context.fillStyle = "rgba(0, 0, 0, 0.7)";
        context.fillRect(formulaX - 10, formulaY - 20, 250, 30);
        
        // Formula text
        context.fillStyle = "#ffffff";
        context.fillText(`e^(iθ) = `, formulaX, formulaY);
        context.fillStyle = colors.real;
        context.fillText(`${cosValue}`, formulaX + 80, formulaY);
        context.fillStyle = "#ffffff";
        context.fillText(` + `, formulaX + 140, formulaY);
        context.fillStyle = colors.imaginary;
        context.fillText(`${sinValue}i`, formulaX + 160, formulaY);
        
        // Component labels
        context.fillStyle = colors.real;
        context.fillText("cos(θ)", x/2 - 30, 20);
        context.fillStyle = colors.imaginary;
        context.fillText("i·sin(θ)", x + 10, -y/2);
        
        context.restore();
        
        // Animation state
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = "#ffffff";
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
            
            drawEulerFormula(angle);
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