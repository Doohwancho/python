window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 4;
    let isAnimating = true;
    let animationId = null;
    
    const colors = {
        sin: "#00ff00",      // Green for sin
        cos: "#ff0000",      // Red for cos
        tan: "#ffff00",      // Yellow for tan
        sec: "#ff00ff",      // Magenta for sec
        csc: "#00ffff",      // Cyan for csc
        cot: "#ff8800",      // Orange for cot
        grid: "#333333",     // Dark gray for background grid
        axis: "#ffffff"      // White for main axes
    };
    
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Vertical grid lines
        for(let i = -width/2; i < width/2; i += scale/4) {
            context.beginPath();
             // Only color the unit marks, not the whole line
            context.strokeStyle = i % scale === 0 ? "rgba(255,0,0,0.3)" : colors.grid;
            context.moveTo(i, -height/2);
            context.lineTo(i, height/2);
            context.stroke();
        }
        
        // Horizontal grid lines
        for(let i = -height/2; i < height/2; i += scale/4) {
            context.beginPath();
            // Only color the unit marks, not the whole line
            context.strokeStyle = i % scale === 0 ? "rgba(0,255,0,0.3)" : colors.grid;
            context.moveTo(-width/2, i);
            context.lineTo(width/2, i);
            context.stroke();
        }

        // Add grid values
        context.save();
        context.scale(1, -1);
        context.font = "12px Arial";
        context.textAlign = "right";

        // X-axis values
        for(let i = -width/2; i <= width/2; i += scale/2) {
            if(i !== 0) {
                context.fillStyle = colors.axis; // Changed to white
                context.fillText((i/scale).toFixed(1), i - 5, 20);
            }
        }

        // Y-axis values
        for(let i = -height/2; i <= height/2; i += scale/2) {
            if(i !== 0) {
                context.fillStyle = colors.axis; // Changed to white
                context.fillText((i/scale).toFixed(1), -5, -i + 5);
            }
        }
        context.restore();
    }

    function drawAngleMarkers(angle) {
        context.save();
        context.scale(1, -1); // Flip text right side up
        context.font = "14px Arial";
        context.textAlign = "center";
        
        // Draw degree markers around circle
        for(let deg = 0; deg < 360; deg += 30) {
            const rad = (deg * Math.PI) / 180;
            const markerDist = scale + 25;
            const x = Math.cos(rad) * markerDist;
            const y = Math.sin(rad) * markerDist;
            
            context.fillStyle = "#888888";
            context.fillText(`${deg}°`, x, -y);
        }
        
        // Draw π radian markers
        for(let rad = 0; rad < Math.PI * 2; rad += Math.PI/4) {
            const markerDist = scale + 45;
            const x = Math.cos(rad) * markerDist;
            const y = Math.sin(rad) * markerDist;
            
            context.fillStyle = "#666666";
            const piLabel = (rad/Math.PI).toFixed(2) + "π";
            context.fillText(piLabel, x, -y);
        }

        // Show current angle in degrees and radians
        context.fillStyle = "#ffffff";
        const degrees = (angle * 180 / Math.PI).toFixed(1);
        const radians = (angle / Math.PI).toFixed(2);
        context.fillText(`Angle: ${degrees}° = ${radians}π`, 0, -scale - 60);

        // Show unit measurements
        const x = Math.cos(angle);
        const y = Math.sin(angle);
        context.fillText(`sin(θ) = ${y.toFixed(3)}`, -scale/2, -scale - 80);
        context.fillText(`cos(θ) = ${x.toFixed(3)}`, scale/2, -scale - 80);
        if(Math.abs(Math.cos(angle)) > 0.01) {
            context.fillText(`tan(θ) = ${Math.tan(angle).toFixed(3)}`, 0, -scale - 100);
        }

        context.restore();
    }

    function drawUnitMarkers() {
        context.save();
        context.scale(1, -1);
        context.font = "12px Arial";
        context.fillStyle = "#666666";
        
        // Mark unit circle values
        context.fillText("1", scale + 5, -5);
        context.fillText("1", 5, -scale - 5);
        context.fillText("-1", -scale - 15, -5);
        context.fillText("-1", 5, scale + 15);
        
        // Draw small ticks at unit intervals
        context.strokeStyle = "#444444";
        context.lineWidth = 1;
        
        // X-axis ticks
        for(let i = -1; i <= 1; i += 0.5) {
            const x = i * scale;
            context.beginPath();
            context.moveTo(x, -5);
            context.lineTo(x, 5);
            context.stroke();
        }
        
        // Y-axis ticks
        for(let i = -1; i <= 1; i += 0.5) {
            const y = i * scale;
            context.beginPath();
            context.moveTo(-5, -y);
            context.lineTo(5, -y);
            context.stroke();
        }
        
        context.restore();
    }


    function drawTrigFunctions(angle) {
        // Clear and draw background
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        // Always draw these regardless of angle
        drawGrid();
        drawAxes();
        drawUnitCircle();
        drawUnitMarkers();
        drawAngleMarkers(angle);

        const x = Math.cos(angle) * scale;
        const y = Math.sin(angle) * scale;

        // Draw angle arc
        context.beginPath();
        context.strokeStyle = "#ffffff";
        context.lineWidth = 2;
        context.arc(0, 0, scale/4, 0, angle);
        context.stroke();

        // Draw radius line
        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(x, y);
        context.stroke();

        // Draw sin line
        context.strokeStyle = colors.sin;
        context.lineWidth = 3;
        context.beginPath();
        context.moveTo(x, 0);
        context.lineTo(x, y);
        context.stroke();

        // Draw cos line
        context.strokeStyle = colors.cos;
        context.beginPath();
        context.moveTo(0, 0);
        context.lineTo(x, 0);
        context.stroke();

        // Animation state indicator
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = "#ffffff";
        context.fillText(isAnimating ? "Press SPACE to pause" : "Press SPACE to resume", -width/2 + 20, -height/2 + 30);
        context.restore();

        let tanLength = 0, secX = 0, cscY = 0, cotHeight = 0;

        // Calculate and draw other trig functions
        if(Math.abs(Math.cos(angle)) > 0.01) {
            tanLength = Math.tan(angle) * scale;
            secX = scale / Math.cos(angle);
            
            if(Math.abs(tanLength) < height) {
                context.strokeStyle = colors.tan;
                context.beginPath();
                context.moveTo(scale, 0);
                context.lineTo(scale, tanLength);
                context.stroke();
            }

            if(Math.abs(secX) < width) {
                context.strokeStyle = colors.sec;
                context.beginPath();
                context.moveTo(0, 0);
                context.lineTo(secX, 0);
                context.stroke();
            }
        }

        if(Math.abs(Math.sin(angle)) > 0.01) {
            cscY = scale / Math.sin(angle);
            cotHeight = (Math.cos(angle) / Math.sin(angle)) * scale;

            if(Math.abs(cscY) < height) {
                context.strokeStyle = colors.csc;
                context.beginPath();
                context.moveTo(0, 0);
                context.lineTo(0, cscY);
                context.stroke();
            }

            if(Math.abs(cotHeight) < height) {
                context.strokeStyle = colors.cot;
                context.beginPath();
                context.moveTo(0, scale);
                context.lineTo(0, cotHeight);
                context.stroke();
            }
        }

        // Labels
        context.save();
        context.scale(1, -1);
        context.font = "bold 16px Arial";
        
        // Always show angle label
        context.fillStyle = "#ffffff";
        context.fillText(`θ`, scale/8, scale/8);
        
        // Always show basic trig function labels
        context.fillStyle = colors.cos;
        context.fillText("cos θ", x/2, -10);
        
        context.fillStyle = colors.sin;
        context.fillText("sin θ", x + 10, -y/2);
        
        // Show other labels only when the functions are defined and within bounds
        if(Math.abs(Math.cos(angle)) > 0.01 && Math.abs(tanLength) < height) {
            context.fillStyle = colors.tan;
            context.fillText("tan θ", scale + 10, -tanLength/2);
            
            if(Math.abs(secX) < width) {
                context.fillStyle = colors.sec;
                context.fillText("sec θ", secX/2, 20);
            }
        }
        
        if(Math.abs(Math.sin(angle)) > 0.01) {
            if(Math.abs(cscY) < height) {
                context.fillStyle = colors.csc;
                context.fillText("csc θ", -30, -cscY);
            }
            
            if(Math.abs(cotHeight) < height) {
                context.fillStyle = colors.cot;
                context.fillText("cot θ", 20, -cotHeight);
            }
        }
        
        context.restore();
    }

    function drawAxes() {
        context.lineWidth = 2;
        
        // X axis - white
        context.beginPath();
        context.strokeStyle = colors.axis;
        context.moveTo(-width/2, 0);
        context.lineTo(width/2, 0);
        context.stroke();
        
        // Y axis - white
        context.beginPath();
        context.strokeStyle = colors.axis;
        context.moveTo(0, -height/2);
        context.lineTo(0, height/2);
        context.stroke();
    }

    function drawUnitCircle() {
        context.strokeStyle = "#ffffff";
        context.lineWidth = 2;
        context.beginPath();
        context.arc(0, 0, scale, 0, Math.PI * 2);
        context.stroke();
    }

    let angle = 0;

    function animate() {
        if (isAnimating) {
            angle += 0.01;
            if(angle > Math.PI * 2) angle = 0;
            
            drawTrigFunctions(angle);
            animationId = requestAnimationFrame(animate);
        }
    }

    // Add keyboard event listener
    document.addEventListener('keydown', function(event) {
        if (event.code === 'Space') {
            event.preventDefault(); // Prevent page scrolling
            isAnimating = !isAnimating; // Toggle animation state
            
            if (isAnimating) {
                animate(); // Resume animation
            } else {
                cancelAnimationFrame(animationId); // Pause animation
            }
        }
    });

    // Start animation
    animate();

    // Optional: Add visual indicator for animation state
    function drawAnimationState() {
        context.save();
        context.scale(1, -1); // Flip text right side up
        context.font = "16px Arial";
        context.fillStyle = "#ffffff";
        context.fillText(isAnimating ? "Press SPACE to pause" : "Press SPACE to resume", -width/2 + 20, -height/2 + 30);
        context.restore();
    }

    // Modify drawTrigFunctions to include animation state indicator
    const originalDrawTrigFunctions = drawTrigFunctions;
    drawTrigFunctions = function(angle) {
        originalDrawTrigFunctions(angle);
        drawAnimationState();
    };
};