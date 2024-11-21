window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    let highlightX = 1;
    
    const colors = {
        exp: "#0088ff",       // Blue for e^x
        derivative: "#ff0000", // Red for derivative
        tangent: "#00ff00",   // Green for tangent line
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

    function drawExp() {
        context.beginPath();
        context.strokeStyle = colors.exp;
        context.lineWidth = 2;

        for(let x = -4; x <= 4; x += 0.1) {
            const y = Math.exp(x);
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
        context.fillStyle = colors.exp;
        context.fillText("y = eˣ", scale * 1.5, -scale * 3);
        context.restore();
    }

    function drawTangentLine(x) {
        const y = Math.exp(x);
        const slope = Math.exp(x);  // derivative of e^x is e^x
        
        // Calculate points for tangent line
        const x1 = x - 1;
        const y1 = y - slope;
        const x2 = x + 1;
        const y2 = y + slope;
        
        context.beginPath();
        context.strokeStyle = colors.tangent;
        context.lineWidth = 2;
        context.setLineDash([5, 5]);
        context.moveTo(x1 * scale/2, y1 * scale/2);
        context.lineTo(x2 * scale/2, y2 * scale/2);
        context.stroke();
        context.setLineDash([]);

        // Draw point of tangency
        context.beginPath();
        context.arc(x * scale/2, y * scale/2, 5, 0, Math.PI * 2);
        context.fillStyle = colors.tangent;
        context.fill();
    }

    function demonstrateProperties(x) {
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        
        let yPos = -height/2 + 120;
        const xPos = -width/4;
        
        // Title
        context.fillStyle = colors.text;
        context.font = "20px Arial";
        context.fillText("자연상수 e의 특성 (Properties of Natural Number e)", xPos, yPos);
        context.font = "16px Arial";

        // 1. Derivative property
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("1. 미분의 특성: eˣ의 미분은 자기 자신", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("d/dx(eˣ) = eˣ", xPos + 20, yPos);
        yPos += 25;
        context.fillText(`현재 x = ${x.toFixed(2)}에서:`, xPos + 20, yPos);
        yPos += 25;
        context.fillText(`• 함숫값: eˣ = ${Math.exp(x).toFixed(4)}`, xPos + 40, yPos);
        yPos += 25;
        context.fillText(`• 순간변화율: d/dx(eˣ) = ${Math.exp(x).toFixed(4)}`, xPos + 40, yPos);

        // 2. Growth property
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("2. 자연 성장의 기초", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("• 연속 복리의 극한", xPos + 20, yPos);
        yPos += 25;
        const n = 10;
        const approxE = Math.pow(1 + 1/n, n);
        context.fillText(`lim(1 + 1/n)ⁿ = e   예: n = ${n}일 때, (1 + 1/${n})^${n} = ${approxE.toFixed(4)}`, xPos + 20, yPos);

        // 3. Natural log property
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("3. 자연로그의 밑", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("• ln(e) = 1", xPos + 20, yPos);
        yPos += 25;
        context.fillText("• eˡⁿ⁽ˣ⁾ = x", xPos + 20, yPos);

        // 4. Series expansion
        yPos += 50;
        context.fillStyle = colors.highlight;
        context.fillText("4. 테일러 급수", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + ...", xPos + 20, yPos);

        // Current point info
        yPos += 50;
        context.fillStyle = colors.tangent;
        context.fillText("초록색 접선: 순간변화율이 함숫값과 같음을 보여줍니다", xPos, yPos);

        context.restore();
    }

    function drawVisualization() {
        context.fillStyle = "#000000";
        context.fillRect(-width/3, -height/2, width, height);
        
        drawGrid();
        drawExp();
        drawTangentLine(highlightX);
        demonstrateProperties(highlightX);
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