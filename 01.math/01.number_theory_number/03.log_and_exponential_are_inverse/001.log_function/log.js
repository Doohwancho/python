window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    let highlightX = 8;
    
    const colors = {
        log2: "#ff0000",      // Red for log base 2
        log10: "#00ff00",     // Green for log base 10
        loge: "#0088ff",      // Blue for natural log
        grid: "#333333",      // Dark gray for grid
        axis: "#ffffff",      // White for axes
        text: "#ffffff",      // White for text
        highlight: "#ffff00"  // Yellow for highlights
    };
    
    // Move origin to show negative x values
    context.translate(width / 3, height / 2);
    context.scale(1, -1);

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -width/3; i < width*2/3; i += scale/2) {
            context.beginPath();
            context.strokeStyle = i === 0 ? colors.axis : colors.grid;
            context.moveTo(i, -height/2);
            context.lineTo(i, height/2);
            context.stroke();
        }
        
        for(let i = -height/2; i < height/2; i += scale/2) {
            context.beginPath();
            context.strokeStyle = i === 0 ? colors.axis : colors.grid;
            context.moveTo(-width/3, i);
            context.lineTo(width*2/3, i);
            context.stroke();
        }

        // Add scale numbers
        context.save();
        context.scale(1, -1);
        context.font = "12px Arial";
        context.fillStyle = colors.text;
        
        // X axis numbers
        for(let i = 0; i <= 16; i += 2) {
            if(i !== 0) {
                context.fillText(i, i * scale/2 - 10, 20);
            }
        }
        
        // Y axis numbers
        for(let i = -4; i <= 4; i++) {
            if(i !== 0) {
                context.fillText(i, -25, -i * scale/2 + 5);
            }
        }
        context.restore();
    }

    function drawLog(base, color, label) {
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;

        for(let x = 0.1; x <= 16; x += 0.1) {
            const y = Math.log(x) / Math.log(base);
            if(y < 4 && y > -4) {
                const screenX = x * scale/2;
                const screenY = y * scale/2;
                
                if(x === 0.1) {
                    context.moveTo(screenX, screenY);
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
        }
        context.stroke();

        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = color;
        context.fillText(label, scale * 6, -scale * (1 + Math.log(16)/Math.log(base)/4));
        context.restore();
    }

    function demonstrateLogProperties(x) {
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        
        // Calculate example values
        const a = 2;
        const b = 4;
        const product = a * b;
        
        let yPos = -height/2 + 120;
        const xPos = -width/4;
        
        // Title for core properties
        context.fillStyle = colors.text;
        context.font = "20px Arial";
        context.fillText("로그의 핵심 성질 (Core Properties of Logarithms)", xPos, yPos);
        context.font = "16px Arial";

        // 1. Multiplication becomes addition
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("1. 곱셈을 덧셈으로 변환 (Multiplication → Addition)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText(`${a} × ${b} = ${product}  →  log(${a} × ${b}) = log(${a}) + log(${b})`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`log₂(${product}) = log₂(${a}) + log₂(${b})`, xPos + 20, yPos);
        context.fillText(`${Math.log2(product).toFixed(2)} = ${Math.log2(a).toFixed(2)} + ${Math.log2(b).toFixed(2)}`, xPos + 250, yPos);

        // 2. Division becomes subtraction
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("2. 나눗셈을 뺄셈으로 변환 (Division → Subtraction)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText(`${product} ÷ ${a} = ${b}  →  log(${product} ÷ ${a}) = log(${product}) - log(${a})`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`log₂(${b}) = log₂(${product}) - log₂(${a})`, xPos + 20, yPos);
        context.fillText(`${Math.log2(b).toFixed(2)} = ${Math.log2(product).toFixed(2)} - ${Math.log2(a).toFixed(2)}`, xPos + 250, yPos);

        // 3. Power becomes multiplication
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("3. 거듭제곱을 곱셈으로 변환 (Power → Multiplication)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText(`${a}³ = ${Math.pow(a, 3)}  →  log(${a}³) = 3 × log(${a})`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`log₂(${Math.pow(a, 3)}) = 3 × log₂(${a})`, xPos + 20, yPos);
        context.fillText(`${Math.log2(Math.pow(a, 3)).toFixed(2)} = 3 × ${Math.log2(a).toFixed(2)}`, xPos + 250, yPos);

        // Current values section
        yPos += 50;
        context.fillStyle = colors.text;
        context.fillText(`현재 x = ${x.toFixed(1)}일 때:`, xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.log2;
        context.fillText(`log₂(${x.toFixed(1)}) = ${(Math.log(x) / Math.log(2)).toFixed(4)}`, xPos + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.loge;
        context.fillText(`ln(${x.toFixed(1)}) = ${Math.log(x).toFixed(4)}`, xPos + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.log10;
        context.fillText(`log₁₀(${x.toFixed(1)}) = ${Math.log10(x).toFixed(4)}`, xPos + 20, yPos);

        context.restore();

        // Draw points on curves
        function drawPoint(x, y, color) {
            const screenX = x * scale/2;
            const screenY = y * scale/2;
            context.beginPath();
            context.arc(screenX, screenY, 5, 0, Math.PI * 2);
            context.fillStyle = color;
            context.fill();
        }

        drawPoint(x, Math.log2(x), colors.log2);
        drawPoint(x, Math.log(x), colors.loge);
        drawPoint(x, Math.log10(x), colors.log10);
    }

    function drawVisualization() {
        context.fillStyle = "#000000";
        context.fillRect(-width/3, -height/2, width, height);
        
        drawGrid();
        drawLog(2, colors.log2, "y = log₂(x)");
        drawLog(Math.E, colors.loge, "y = ln(x)");
        drawLog(10, colors.log10, "y = log₁₀(x)");
        
        demonstrateLogProperties(highlightX);
    }

    function animate() {
        if (isAnimating) {
            highlightX = 8 + Math.sin(Date.now() / 1000) * 4;
            drawVisualization();
            animationId = requestAnimationFrame(animate);
        }
    }

    canvas.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        const x = ((event.clientX - rect.left) - width/3) / (scale/2);
        if(x > 0 && x <= 16) {
            highlightX = x;
            if(!isAnimating) {
                drawVisualization();
            }
        }
    });

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