window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    let highlightX = 2;
    
    const colors = {
        exp2: "#ff0000",      // Red for base 2
        exp10: "#00ff00",     // Green for base 10
        expE: "#0088ff",      // Blue for base e
        grid: "#333333",      // Dark gray for grid
        axis: "#ffffff",      // White for axes
        text: "#ffffff",      // White for text
        highlight: "#ffff00"  // Yellow for highlights
    };
    
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
        for(let i = -4; i <= 4; i++) {
            context.fillText(i, i * scale/2 - 10, 20);
        }
        
        // Y axis numbers
        for(let i = -2; i <= 8; i++) {
            if(i !== 0) {
                context.fillText(i, -25, -i * scale/2 + 5);
            }
        }
        context.restore();
    }

    function drawExp(base, color, label) {
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;

        for(let x = -4; x <= 4; x += 0.1) {
            const y = Math.pow(base, x);
            if(y < 8 && y > -8) {
                const screenX = x * scale/2;
                const screenY = y * scale/2;
                
                if(x === -4) {
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
        context.fillText(label, scale * 1.5, -scale * 3);
        context.restore();
    }

    function demonstrateExpProperties(x) {
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        
        let yPos = -height/2 + 120;
        const xPos = -width/4;
        
        // Title for core properties
        context.fillStyle = colors.text;
        context.font = "20px Arial";
        context.fillText("지수함수의 핵심 성질 (Core Properties of Exponential Functions)", xPos, yPos);
        context.font = "16px Arial";

        // 1. Addition becomes multiplication
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("1. 덧셈을 곱셈으로 변환 (Addition → Multiplication)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        const a = 2, b = 3;
        context.fillText(`2^(${a} + ${b}) = 2^${a} × 2^${b}`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`2^5 = 2^2 × 2^3 = ${Math.pow(2,2)} × ${Math.pow(2,3)} = ${Math.pow(2,5)}`, xPos + 20, yPos);

        // 2. Subtraction becomes division
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("2. 뺄셈을 나눗셈으로 변환 (Subtraction → Division)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText(`2^(${a+b} - ${b}) = 2^${a+b} ÷ 2^${b}`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`2^2 = 2^5 ÷ 2^3 = ${Math.pow(2,5)} ÷ ${Math.pow(2,3)} = ${Math.pow(2,2)}`, xPos + 20, yPos);

        // 3. Power rule
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("3. 거듭제곱의 곱은 지수의 곱 ((a^n)^m = a^(n×m))", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText(`(2^2)^3 = 2^(2 × 3) = 2^6 = ${Math.pow(2,6)}`, xPos + 20, yPos);

        // 4. Growth/decay properties
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("4. 성장/감소 특성", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("• 양수 밑: 단조 증가 (2ˣ, eˣ, 10ˣ)", xPos + 20, yPos);
        yPos += 25;
        context.fillText("• 0 < 밑 < 1: 단조 감소 ((1/2)ˣ)", xPos + 20, yPos);
        yPos += 25;
        context.fillText("• 모든 지수함수는 y축과 교차하는 점이 (0,1)", xPos + 20, yPos);

        // Current values
        yPos += 50;
        context.fillStyle = colors.text;
        context.fillText(`현재 x = ${x.toFixed(1)}일 때:`, xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.exp2;
        context.fillText(`2ˣ = ${Math.pow(2, x).toFixed(4)}`, xPos + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.expE;
        context.fillText(`eˣ = ${Math.exp(x).toFixed(4)}`, xPos + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.exp10;
        context.fillText(`10ˣ = ${Math.pow(10, x).toFixed(4)}`, xPos + 20, yPos);

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

        if(Math.abs(x) <= 4) {
            drawPoint(x, Math.pow(2, x), colors.exp2);
            drawPoint(x, Math.exp(x), colors.expE);
            drawPoint(x, Math.pow(10, x), colors.exp10);
        }
    }

    function drawVisualization() {
        context.fillStyle = "#000000";
        context.fillRect(-width/3, -height/2, width, height);
        
        drawGrid();
        drawExp(2, colors.exp2, "y = 2ˣ");
        drawExp(Math.E, colors.expE, "y = eˣ");
        drawExp(10, colors.exp10, "y = 10ˣ");
        
        demonstrateExpProperties(highlightX);
    }

    function animate() {
        if (isAnimating) {
            highlightX = 2 * Math.sin(Date.now() / 1000);
            drawVisualization();
            animationId = requestAnimationFrame(animate);
        }
    }

    canvas.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        const x = ((event.clientX - rect.left) - width/3) / (scale/2);
        if(x >= -4 && x <= 4) {
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