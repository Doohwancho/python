window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let isAnimating = true;
    let animationId = null;
    let time = 0;
    
    const colors = {
        growth: "#00ff00",    // Green for population growth
        decay: "#ff0000",     // Red for radioactive decay
        cooling: "#0088ff",   // Blue for Newton's cooling
        compound: "#ffff00",  // Yellow for compound interest
        grid: "#333333",      // Dark gray for grid
        axis: "#ffffff",      // White for axes
        text: "#ffffff"       // White for text
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
        
        // Time axis (x) labels
        for(let i = 0; i <= 8; i++) {
            context.fillText(i + "시간", i * scale/2 - 10, 20);
        }
        
        // Value axis (y) labels
        for(let i = 0; i <= 4; i++) {
            context.fillText((i * 25) + "%", -40, -i * scale + 5);
        }
        context.restore();
    }

    // Population growth: P(t) = P₀e^(rt)
    function drawPopulationGrowth(t) {
        const r = 0.5;  // growth rate
        context.beginPath();
        context.strokeStyle = colors.growth;
        context.lineWidth = 2;

        for(let x = 0; x <= 8; x += 0.1) {
            const y = Math.exp(r * x);
            if(y < 4) {
                const screenX = x * scale/2;
                const screenY = y * scale;
                
                if(x === 0) {
                    context.moveTo(screenX, screenY);
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
        }
        context.stroke();

        // Current point
        if(t <= 8) {
            const currentY = Math.exp(r * t);
            context.beginPath();
            context.arc(t * scale/2, currentY * scale, 5, 0, Math.PI * 2);
            context.fillStyle = colors.growth;
            context.fill();
        }
    }

    // Radioactive decay: N(t) = N₀e^(-λt)
    function drawRadioactiveDecay(t) {
        const lambda = 0.3;  // decay constant
        context.beginPath();
        context.strokeStyle = colors.decay;
        context.lineWidth = 2;

        for(let x = 0; x <= 8; x += 0.1) {
            const y = Math.exp(-lambda * x);
            const screenX = x * scale/2;
            const screenY = y * scale;
            
            if(x === 0) {
                context.moveTo(screenX, screenY);
            } else {
                context.lineTo(screenX, screenY);
            }
        }
        context.stroke();

        // Current point
        if(t <= 8) {
            const currentY = Math.exp(-lambda * t);
            context.beginPath();
            context.arc(t * scale/2, currentY * scale, 5, 0, Math.PI * 2);
            context.fillStyle = colors.decay;
            context.fill();
        }
    }

    // Newton's law of cooling: T(t) = Ts + (T₀-Ts)e^(-kt)
    function drawCooling(t) {
        const k = 0.4;     // cooling constant
        const Ts = 0.2;    // surrounding temperature
        const T0 = 1;      // initial temperature
        
        context.beginPath();
        context.strokeStyle = colors.cooling;
        context.lineWidth = 2;

        for(let x = 0; x <= 8; x += 0.1) {
            const y = Ts + (T0 - Ts) * Math.exp(-k * x);
            const screenX = x * scale/2;
            const screenY = y * scale;
            
            if(x === 0) {
                context.moveTo(screenX, screenY);
            } else {
                context.lineTo(screenX, screenY);
            }
        }
        context.stroke();

        // Current point
        if(t <= 8) {
            const currentY = Ts + (T0 - Ts) * Math.exp(-k * t);
            context.beginPath();
            context.arc(t * scale/2, currentY * scale, 5, 0, Math.PI * 2);
            context.fillStyle = colors.cooling;
            context.fill();
        }
    }

    // Compound interest: A(t) = P(1 + r/n)^(nt) ≈ Pe^(rt)
    function drawCompoundInterest(t) {
        const r = 0.4;    // interest rate
        context.beginPath();
        context.strokeStyle = colors.compound;
        context.lineWidth = 2;

        for(let x = 0; x <= 8; x += 0.1) {
            const y = Math.exp(r * x);
            if(y < 4) {
                const screenX = x * scale/2;
                const screenY = y * scale;
                
                if(x === 0) {
                    context.moveTo(screenX, screenY);
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
        }
        context.stroke();

        // Current point
        if(t <= 8) {
            const currentY = Math.exp(r * t);
            context.beginPath();
            context.arc(t * scale/2, currentY * scale, 5, 0, Math.PI * 2);
            context.fillStyle = colors.compound;
            context.fill();
        }
    }

    function displayExplanations(t) {
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        
        let yPos = -height/2 + 60;
        const xPos = -width/4;
        
        // Title
        context.fillStyle = colors.text;
        context.font = "20px Arial";
        context.fillText("자연상수 e를 활용한 자연현상 모델링", xPos, yPos);
        context.font = "16px Arial";
        yPos += 30;
        context.fillText("(Natural Phenomena Modeled with e)", xPos, yPos);

        // Time display
        yPos += 40;
        context.fillText(`경과 시간: ${t.toFixed(1)} 시간`, xPos, yPos);

        // Population Growth
        yPos += 40;
        context.fillStyle = colors.growth;
        context.fillText("1. 개체수 증가 (Population Growth)", xPos, yPos);
        yPos += 25;
        context.fillText(`P(t) = P₀e^(rt)    현재 값: ${(Math.exp(0.5 * t)).toFixed(2)}P₀`, xPos + 20, yPos);

        // Radioactive Decay
        yPos += 40;
        context.fillStyle = colors.decay;
        context.fillText("2. 방사성 붕괴 (Radioactive Decay)", xPos, yPos);
        yPos += 25;
        context.fillText(`N(t) = N₀e^(-λt)    현재 값: ${(Math.exp(-0.3 * t)).toFixed(2)}N₀`, xPos + 20, yPos);

        // Newton's Cooling
        yPos += 40;
        context.fillStyle = colors.cooling;
        context.fillText("3. 뉴턴의 냉각법칙 (Newton's Cooling)", xPos, yPos);
        yPos += 25;
        context.fillText(`T(t) = Ts + (T₀-Ts)e^(-kt)    현재 값: ${(0.2 + 0.8 * Math.exp(-0.4 * t)).toFixed(2)}T₀`, xPos + 20, yPos);

        // Compound Interest
        yPos += 40;
        context.fillStyle = colors.compound;
        context.fillText("4. 연속 복리 (Continuous Compound Interest)", xPos, yPos);
        yPos += 25;
        context.fillText(`A(t) = Pe^(rt)    현재 값: ${(Math.exp(0.4 * t)).toFixed(2)}P`, xPos + 20, yPos);

        context.restore();
    }

    function drawVisualization() {
        context.fillStyle = "#000000";
        context.fillRect(-width/3, -height/2, width, height);
        
        drawGrid();
        drawPopulationGrowth(time);
        drawRadioactiveDecay(time);
        drawCooling(time);
        drawCompoundInterest(time);
        displayExplanations(time);
    }

    function animate() {
        if (isAnimating) {
            time += 0.02;
            if(time > 8) time = 0;
            
            drawVisualization();
            animationId = requestAnimationFrame(animate);
        }
    }

    canvas.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        const x = ((event.clientX - rect.left) - width/3) / (scale/2);
        if(x >= 0 && x <= 8) {
            time = x;
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