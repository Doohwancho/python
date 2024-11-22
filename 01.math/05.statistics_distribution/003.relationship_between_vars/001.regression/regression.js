window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 12;
    let isAnimating = true;
    let currentTime = 0;
    let points = [];
    let showResiduals = true;
    let showConfidence = true;
    
    const colors = {
        points: "#00ff00",         // Green for data points
        regression: "#ff0000",     // Red for regression line
        residuals: "#0088ff",      // Blue for residuals
        confidence: "#ffff0080",   // Semi-transparent yellow for confidence interval
        grid: "#333333",
        axis: "#ffffff",
        text: "#ffffff",
        highlight: "#ff00ff"       // Magenta for highlights
    };

    // Center coordinate system
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Generate random point with some noise
    function generatePoint() {
        const x = (Math.random() * 6) - 3;
        const y = 0.8 * x + 0.5 + (Math.random() - 0.5) * 0.5;
        return { x, y };
    }

    // Calculate regression parameters
    function calculateRegression(points) {
        if (points.length < 2) return null;

        const n = points.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;

        points.forEach(point => {
            sumX += point.x;
            sumY += point.y;
            sumXY += point.x * point.y;
            sumX2 += point.x * point.x;
            sumY2 += point.y * point.y;
        });

        const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        
        // Calculate R-squared
        const yMean = sumY / n;
        const totalSS = points.reduce((sum, p) => sum + Math.pow(p.y - yMean, 2), 0);
        const residualSS = points.reduce((sum, p) => 
            sum + Math.pow(p.y - (slope * p.x + intercept), 2), 0);
        const rSquared = 1 - (residualSS / totalSS);

        // Calculate standard errors
        const MSE = residualSS / (n - 2);
        const slopeStdError = Math.sqrt(MSE / (sumX2 - sumX * sumX / n));
        const interceptStdError = Math.sqrt(MSE * (1/n + Math.pow(sumX/n, 2)/(sumX2 - sumX * sumX / n)));

        return {
            slope,
            intercept,
            rSquared,
            slopeStdError,
            interceptStdError,
            MSE
        };
    }

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -10; i <= 10; i++) {
            if(i === 0) continue;
            
            // Vertical lines
            context.beginPath();
            context.moveTo(i * scale, -height/2);
            context.lineTo(i * scale, height/2);
            context.stroke();

            // Horizontal lines
            context.beginPath();
            context.moveTo(-width/2, i * scale);
            context.lineTo(width/2, i * scale);
            context.stroke();
        }

        // Draw axes
        context.strokeStyle = colors.axis;
        context.lineWidth = 2;
        
        // X-axis
        context.beginPath();
        context.moveTo(-width/2, 0);
        context.lineTo(width/2, 0);
        context.stroke();

        // Y-axis
        context.beginPath();
        context.moveTo(0, -height/2);
        context.lineTo(0, height/2);
        context.stroke();

        // Add labels
        context.save();
        context.scale(1, -1);
        context.font = '14px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'center';

        // X-axis labels
        for(let i = -5; i <= 5; i++) {
            if(i !== 0) {
                context.fillText(i.toString(), i * scale, 20);
            }
        }

        // Y-axis labels
        for(let i = -5; i <= 5; i++) {
            if(i !== 0) {
                context.fillText(i.toString(), -20, -i * scale);
            }
        }

        context.restore();
    }

    function drawPoints() {
        points.forEach(point => {
            context.beginPath();
            context.arc(point.x * scale, point.y * scale, 4, 0, Math.PI * 2);
            context.fillStyle = colors.points;
            context.fill();
        });
    }

    function drawRegressionLine(reg) {
        if (!reg) return;

        // Draw regression line
        const x1 = -4;
        const y1 = reg.slope * x1 + reg.intercept;
        const x2 = 4;
        const y2 = reg.slope * x2 + reg.intercept;

        context.beginPath();
        context.strokeStyle = colors.regression;
        context.lineWidth = 2;
        context.moveTo(x1 * scale, y1 * scale);
        context.lineTo(x2 * scale, y2 * scale);
        context.stroke();

        // Draw confidence interval
        if (showConfidence && points.length > 2) {
            const tValue = 2.0;  // Approximate t-value for 95% confidence
            for(let x = x1; x <= x2; x += 0.1) {
                const y = reg.slope * x + reg.intercept;
                const xMean = points.reduce((sum, p) => sum + p.x, 0) / points.length;
                const sumX2 = points.reduce((sum, p) => sum + p.x * p.x, 0);
                const SE = Math.sqrt(reg.MSE * (1/points.length + 
                    Math.pow(x - xMean, 2)/(sumX2 - points.length * xMean * xMean)));
                
                const margin = tValue * SE;
                
                context.beginPath();
                context.fillStyle = colors.confidence;
                context.arc(x * scale, y * scale, margin * scale, 0, Math.PI * 2);
                context.fill();
            }
        }
    }

    function drawResiduals(reg) {
        if (!reg || !showResiduals) return;

        points.forEach(point => {
            const predicted = reg.slope * point.x + reg.intercept;
            context.beginPath();
            context.strokeStyle = colors.residuals;
            context.lineWidth = 1;
            context.setLineDash([5, 5]);
            context.moveTo(point.x * scale, point.y * scale);
            context.lineTo(point.x * scale, predicted * scale);
            context.stroke();
            context.setLineDash([]);
        });
    }

    function drawStats(reg) {
        if (!reg) return;

        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';

        const x = -width/2 + 20;
        let y = -height/2 + 30;

        // Regression equation
        context.fillText("회귀방정식:", x, y);
        y += 25;
        context.fillText(
            `y = ${reg.slope.toFixed(3)}x + ${reg.intercept.toFixed(3)}`,
            x, y
        );

        // R-squared
        y += 30;
        context.fillText(`R² = ${reg.rSquared.toFixed(3)}`, x, y);

        // Standard errors
        y += 25;
        context.fillText(
            `표준오차(slope) = ${reg.slopeStdError.toFixed(3)}`,
            x, y
        );
        y += 25;
        context.fillText(
            `표준오차(intercept) = ${reg.interceptStdError.toFixed(3)}`,
            x, y
        );

        // Controls
        y += 40;
        context.fillText("Controls:", x, y);
        y += 25;
        context.fillText("Space: 일시정지", x, y);
        y += 25;
        context.fillText("R: 잔차 표시 전환", x, y);
        y += 25;
        context.fillText("C: 신뢰구간 표시 전환", x, y);

        context.restore();
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);

        // Draw basic elements
        drawGrid();
        
        // Add new point occasionally
        if (isAnimating && currentTime % 60 === 0 && points.length < 50) {
            points.push(generatePoint());
        }

        // Calculate regression if we have points
        const regression = calculateRegression(points);

        // Draw regression elements
        drawRegressionLine(regression);
        drawResiduals(regression);
        drawPoints();
        drawStats(regression);
    }

    function animate() {
        if (isAnimating) {
            currentTime++;
            draw();
            requestAnimationFrame(animate);
        }
    }

    // Add interactions
    document.addEventListener('keydown', function(event) {
        switch(event.code) {
            case 'Space':
                isAnimating = !isAnimating;
                if(isAnimating) animate();
                break;
            case 'KeyR':
                showResiduals = !showResiduals;
                draw();
                break;
            case 'KeyC':
                showConfidence = !showConfidence;
                draw();
                break;
        }
    });

    animate();
};