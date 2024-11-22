window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 8;
    let currentCorrelation = 0.8;  // Initial correlation
    let isAnimating = true;
    let currentTime = 0;
    
    const colors = {
        points: "#00ff00",      // Green for points
        regression: "#ff0000",  // Red for regression line
        grid: "#333333",       // Dark gray for grid
        axis: "#ffffff",       // White for axes
        text: "#ffffff",       // White for text
        highlight: "#ffff00"   // Yellow for highlights
    };

    // Center coordinate system
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Generate correlated data
    function generateData(correlation, n = 50) {
        const data = [];
        for(let i = 0; i < n; i++) {
            // Generate x from normal distribution
            const x = randNormal();
            
            // Generate correlated y
            const y = correlation * x + Math.sqrt(1 - correlation * correlation) * randNormal();
            
            data.push({x, y});
        }
        return data;
    }

    // Generate normal random numbers using Box-Muller transform
    function randNormal() {
        const u1 = Math.random();
        const u2 = Math.random();
        return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    }

    // Calculate correlation coefficient
    function calculateCorrelation(data) {
        const n = data.length;
        let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0, sumY2 = 0;
        
        data.forEach(point => {
            sumX += point.x;
            sumY += point.y;
            sumXY += point.x * point.y;
            sumX2 += point.x * point.x;
            sumY2 += point.y * point.y;
        });

        const numerator = n * sumXY - sumX * sumY;
        const denominator = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
        
        return numerator / denominator;
    }

    // Calculate regression line
    function calculateRegression(data) {
        const correlation = calculateCorrelation(data);
        const stdX = Math.sqrt(data.reduce((sum, p) => sum + p.x * p.x, 0) / data.length);
        const stdY = Math.sqrt(data.reduce((sum, p) => sum + p.y * p.y, 0) / data.length);
        const slope = correlation * stdY / stdX;
        const intercept = 0;  // Since data is centered
        
        return {slope, intercept};
    }

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -10; i <= 10; i++) {
            if(i === 0) continue;
            
            // Vertical lines
            context.beginPath();
            context.moveTo(i * scale/2, -height/2);
            context.lineTo(i * scale/2, height/2);
            context.stroke();

            // Horizontal lines
            context.beginPath();
            context.moveTo(-width/2, i * scale/2);
            context.lineTo(width/2, i * scale/2);
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
        for(let i = -4; i <= 4; i++) {
            if(i !== 0) {
                context.fillText(i.toString(), i * scale, 20);
            }
        }

        // Y-axis labels
        for(let i = -4; i <= 4; i++) {
            if(i !== 0) {
                context.fillText(i.toString(), -20, -i * scale);
            }
        }

        context.restore();
    }

    function drawCorrelationStrength(r) {
        context.save();
        context.scale(1, -1);
        
        // Draw correlation meter background
        const meterWidth = 200;
        const meterHeight = 20;
        const meterX = -width/4;
        const meterY = -height/3;

        context.fillStyle = "#333";
        context.fillRect(meterX, meterY, meterWidth, meterHeight);

        // Draw correlation strength
        const strengthWidth = Math.abs(r) * meterWidth;
        context.fillStyle = r >= 0 ? "#00ff00" : "#ff0000";
        context.fillRect(meterX + meterWidth/2, meterY, 
                        r >= 0 ? strengthWidth : -strengthWidth, meterHeight);

        // Draw center line
        context.fillStyle = "#fff";
        context.fillRect(meterX + meterWidth/2 - 1, meterY, 2, meterHeight);

        // Draw labels
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'center';
        context.fillText("-1", meterX, meterY + 40);
        context.fillText("0", meterX + meterWidth/2, meterY + 40);
        context.fillText("+1", meterX + meterWidth, meterY + 40);
        context.fillText(`현재 상관계수: ${r.toFixed(3)}`, meterX + meterWidth/2, meterY - 20);

        context.restore();
    }

    function drawCorrelationFormula(data) {
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';

        const x = -width/2 + 20;
        let y = -height/2 + 30;

        // Title
        context.fillText("상관계수 (Correlation Coefficient)", x, y);
        y += 30;

        // Formula
        context.fillText("r = ", x, y);
        y += 30;
        context.fillText("∑(x - x̄)(y - ȳ)", x + 40, y - 10);
        context.fillText("━━━━━━━━━━━━━━━", x + 40, y);
        context.fillText("√∑(x - x̄)² ∑(y - ȳ)²", x + 40, y + 20);

        // Description of strength
        y += 60;
        const r = calculateCorrelation(data);
        let strength = "";
        if (Math.abs(r) > 0.7) strength = "강한";
        else if (Math.abs(r) > 0.3) strength = "중간 정도의";
        else strength = "약한";

        let direction = r > 0 ? "양의" : "음의";
        context.fillText(`${strength} ${direction} 상관관계`, x, y);

        context.restore();
    }

    function drawScatterPlot(data) {
        // Draw points
        data.forEach(point => {
            context.beginPath();
            context.arc(point.x * scale, point.y * scale, 3, 0, Math.PI * 2);
            context.fillStyle = colors.points;
            context.fill();
        });

        // Draw regression line
        const regression = calculateRegression(data);
        const x1 = -4;
        const y1 = regression.slope * x1 + regression.intercept;
        const x2 = 4;
        const y2 = regression.slope * x2 + regression.intercept;

        context.beginPath();
        context.strokeStyle = colors.regression;
        context.lineWidth = 2;
        context.moveTo(x1 * scale, y1 * scale);
        context.lineTo(x2 * scale, y2 * scale);
        context.stroke();
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);

        // Generate data with current correlation
        const angle = currentTime * 0.02;
        currentCorrelation = Math.cos(angle);
        const data = generateData(currentCorrelation);

        // Draw elements
        drawGrid();
        drawScatterPlot(data);
        drawCorrelationStrength(currentCorrelation);
        drawCorrelationFormula(data);
    }

    function animate() {
        if(isAnimating) {
            currentTime++;
            draw();
            requestAnimationFrame(animate);
        }
    }

    // Add interaction
    document.addEventListener('keydown', function(event) {
        if(event.code === 'Space') {
            isAnimating = !isAnimating;
            if(isAnimating) animate();
        }
    });

    animate();
};