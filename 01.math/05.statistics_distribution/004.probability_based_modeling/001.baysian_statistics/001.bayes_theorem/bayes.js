window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 12;
    let isAnimating = true;
    let animationId = null;
    let dataPoints = [];
    let currentTime = 0;
    
    const colors = {
        prior: "#00ff00",     // Green for prior
        likelihood: "#0088ff", // Blue for likelihood
        posterior: "#ff0000", // Red for posterior
        data: "#ffffff",      // White for data points
        grid: "#333333",      // Dark gray for grid
        axis: "#ffffff",      // White for axes
        text: "#ffffff"       // White for text
    };
    
    // Center the coordinate system
    context.translate(width * 0.5, height * 0.5);
    context.scale(1, -1);

    function normalPDF(x, mean, stdDev) {
        return Math.exp(-0.5 * Math.pow((x - mean) / stdDev, 2)) / (stdDev * Math.sqrt(2 * Math.PI));
    }

    function drawGrid() {
        // Main axes
        context.beginPath();
        context.strokeStyle = colors.axis;
        context.lineWidth = 2;
        
        // X axis
        context.moveTo(-scale * 4, 0);
        context.lineTo(scale * 4, 0);
        context.stroke();

        // Y axis
        context.beginPath();
        context.moveTo(0, -scale);
        context.lineTo(0, scale * 3);
        context.stroke();

        // Add labels
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = colors.text;
        context.textAlign = "center";
        
        // X axis labels
        for(let i = -4; i <= 4; i += 1) {
            context.fillText(i, i * scale, 25);
        }
        
        // Axis titles
        context.font = "18px Arial";
        context.fillText("θ (파라미터)", 0, 50); // Centered x-axis label
        
        // Y-axis label (rotated)
        context.save();
        context.rotate(-Math.PI/2);
        context.fillText("확률 밀도", scale * 1.5, -scale * 4);
        context.restore();
        
        context.restore();
    }

    function drawDistribution(mean, stdDev, color, label, yOffset = 0) {
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;

        const points = [];
        for(let x = -4; x <= 4; x += 0.1) {
            const y = normalPDF(x, mean, stdDev);
            points.push({x: x * scale, y: y * scale * 5 + yOffset});
        }

        // Draw curve
        context.moveTo(points[0].x, points[0].y);
        for(let i = 1; i < points.length; i++) {
            context.lineTo(points[i].x, points[i].y);
        }
        context.stroke();

        // Fill area under curve
        context.lineTo(points[points.length-1].x, yOffset);
        context.lineTo(points[0].x, yOffset);
        context.fillStyle = color + '20';
        context.fill();

        // Add label on the right side
        context.save();
        context.scale(1, -1);
        context.font = "16px Arial";
        context.fillStyle = color;
        context.textAlign = "left";
        context.fillText(label, scale * 4.2, -(yOffset + scale * 0.5));
        context.restore();
    }

    function drawDataPoint(x, y) {
        context.beginPath();
        context.arc(x * scale, y, 5, 0, Math.PI * 2);
        context.fillStyle = colors.data;
        context.fill();
    }

    function drawFormulas(posteriorMean, posteriorStd) {
        context.save();
        context.scale(1, -1);
        context.font = "18px Arial";
        context.textAlign = "left";
        
        // Position formulas on the right side
        let yPos = scale * 1.5;
        const xPos = scale * 4.5;

        // Draw box for formulas
        const boxPadding = 20;
        const boxWidth = scale * 4;
        const boxHeight = 300;
        context.fillStyle = "rgba(0, 0, 0, 0.5)";
        context.fillRect(xPos - boxPadding, -scale * 2, boxWidth, boxHeight);

        // Bayes' theorem
        context.fillStyle = colors.text;
        context.fillText("베이즈 정리:", xPos, yPos);
        yPos += 30;
        context.fillText("P(θ|D) ∝ P(D|θ) × P(θ)", xPos, yPos);
        yPos += 30;
        context.fillText("사후확률 ∝ 가능도 × 사전확률", xPos, yPos);

        // Current estimates
        yPos += 50;
        context.fillStyle = colors.posterior;
        context.fillText("현재 추정치:", xPos, yPos);
        yPos += 30;
        context.fillText(`μ = ${posteriorMean.toFixed(3)}`, xPos, yPos);
        yPos += 30;
        context.fillText(`σ = ${posteriorStd.toFixed(3)}`, xPos, yPos);

        // Data information
        yPos += 50;
        context.fillStyle = colors.data;
        context.fillText(`관측된 데이터 수: ${dataPoints.length}`, xPos, yPos);
        if (dataPoints.length > 0) {
            yPos += 30;
            context.fillText(`데이터 평균: ${(dataPoints.reduce((a,b) => a+b) / dataPoints.length).toFixed(3)}`, xPos, yPos);
        }

        context.restore();
    }

    function updateBayesianInference() {
        // Prior parameters
        const priorMean = 0;
        const priorStd = 1;

        // Generate new data
        const trueValue = 0.5;
        const dataStd = 0.5;
        if(currentTime % 100 === 0 && dataPoints.length < 5) {
            const newData = trueValue + dataStd * (Math.random() - 0.5);
            dataPoints.push(newData);
        }

        // Calculate posterior
        let posteriorMean = priorMean;
        let posteriorStd = priorStd;

        dataPoints.forEach(data => {
            const k = posteriorStd * posteriorStd / (posteriorStd * posteriorStd + dataStd * dataStd);
            posteriorMean = posteriorMean + k * (data - posteriorMean);
            posteriorStd = Math.sqrt((1 - k) * posteriorStd * posteriorStd);
        });

        // Draw distributions with spacing
        const spacing = scale * 0.8;
        drawDistribution(priorMean, priorStd, colors.prior, "사전확률 (Prior)", 0);
        
        if(dataPoints.length > 0) {
            const latestData = dataPoints[dataPoints.length - 1];
            drawDistribution(latestData, dataStd, colors.likelihood, "가능도 (Likelihood)", spacing);
            drawDistribution(posteriorMean, posteriorStd, colors.posterior, "사후확률 (Posterior)", spacing * 2);
        }

        // Draw data points
        dataPoints.forEach(x => {
            drawDataPoint(x, 0);
        });

        // Draw formulas
        drawFormulas(posteriorMean, posteriorStd);
    }

    function drawTitle() {
        context.save();
        context.scale(1, -1);
        context.font = "24px Arial";
        context.fillStyle = colors.text;
        context.textAlign = "center";
        context.fillText("베이지안 추론 과정", 0, -scale * 3);
        context.restore();
    }

    function drawVisualization() {
        context.fillStyle = "#000000";
        context.fillRect(-width/2, -height/2, width, height);
        
        drawTitle();
        drawGrid();
        updateBayesianInference();
    }

    function animate() {
        if (isAnimating) {
            currentTime++;
            drawVisualization();
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