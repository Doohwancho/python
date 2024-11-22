window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 12;
    let isAnimating = true;
    let currentTime = 0;
    let sampleMeans = [];
    let currentDistribution = "uniform"; // Can be "uniform", "exponential", "bimodal"
    let sampleSize = 30;
    
    const colors = {
        original: "#00ff00",    // Green for original distribution
        samples: "#0088ff",     // Blue for samples
        means: "#ff0000",       // Red for sample means
        normal: "#ffff00",      // Yellow for normal curve
        grid: "#333333",
        axis: "#ffffff",
        text: "#ffffff"
    };

    // Center coordinate system
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Distribution functions
    const distributions = {
        uniform: {
            name: "균등분포 (Uniform)",
            generate: () => Math.random() * 2 - 1,
            mean: 0,
            std: 1/Math.sqrt(3)
        },
        exponential: {
            name: "지수분포 (Exponential)",
            generate: () => -Math.log(Math.random()),
            mean: 1,
            std: 1
        },
        bimodal: {
            name: "이봉분포 (Bimodal)",
            generate: () => Math.random() < 0.5 ? 
                          Math.random() - 1.5 : Math.random() + 0.5,
            mean: 0,
            std: 1
        }
    };

    function normalPDF(x, mean, std) {
        return Math.exp(-0.5 * Math.pow((x - mean) / std, 2)) / 
               (std * Math.sqrt(2 * Math.PI));
    }

    function generateSample(size) {
        const sample = [];
        for(let i = 0; i < size; i++) {
            sample.push(distributions[currentDistribution].generate());
        }
        return sample;
    }

    function calculateMean(data) {
        return data.reduce((a, b) => a + b) / data.length;
    }

    function calculateStd(data) {
        const mean = calculateMean(data);
        return Math.sqrt(data.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / data.length);
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
        context.beginPath();
        context.moveTo(-width/2, 0);
        context.lineTo(width/2, 0);
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
            context.fillText(i.toString(), i * scale, 20);
        }

        // Y-axis labels
        for(let i = -4; i <= 4; i++) {
            if(i !== 0) {
                context.fillText((i/2).toFixed(1), -20, -i * scale);
            }
        }

        context.restore();
    }

    function drawDistribution(samples, color, yOffset = 0, heightScale = 1) {
        // Create histogram
        const bins = new Array(50).fill(0);
        const binSize = 6 / bins.length;
        
        samples.forEach(value => {
            const binIndex = Math.floor((value + 3) / binSize);
            if(binIndex >= 0 && binIndex < bins.length) {
                bins[binIndex]++;
            }
        });

        // Normalize
        const maxBin = Math.max(...bins);
        const normalizedBins = bins.map(b => (b / maxBin) * heightScale);

        // Draw histogram
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;

        normalizedBins.forEach((height, i) => {
            const x = (i * binSize - 3) * scale;
            const y = height * scale + yOffset;
            
            if(i === 0) {
                context.moveTo(x, yOffset);
            }
            context.lineTo(x, y);
        });

        context.stroke();
    }

    function drawNormalCurve(mean, std, color, yOffset = 0, heightScale = 1) {
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;

        for(let x = -4; x <= 4; x += 0.1) {
            const y = normalPDF(x, mean, std) * heightScale * scale + yOffset;
            const screenX = x * scale;
            
            if(x === -4) {
                context.moveTo(screenX, y);
            } else {
                context.lineTo(screenX, y);
            }
        }

        context.stroke();
    }

    function drawSamplingProcess() {
        // Draw current sample points
        const sample = generateSample(sampleSize);
        const mean = calculateMean(sample);
        sampleMeans.push(mean);
        if(sampleMeans.length > 1000) sampleMeans.shift();

        // Draw original distribution
        drawDistribution([...Array(1000)].map(() => 
            distributions[currentDistribution].generate()),
            colors.original, scale * 2, 1
        );

        // Draw current sample
        drawDistribution(sample, colors.samples, 0, 0.5);

        // Draw sample means distribution
        drawDistribution(sampleMeans, colors.means, -scale * 2, 1);

        // Draw theoretical normal curve for sample means
        const theoreticalStd = distributions[currentDistribution].std / Math.sqrt(sampleSize);
        drawNormalCurve(
            distributions[currentDistribution].mean,
            theoreticalStd,
            colors.normal,
            -scale * 2,
            scale
        );
    }

    function drawExplanations() {
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';

        const x = -width/2 + 20;
        let y = -height/2 + 30;

        // Title
        context.font = '20px Arial';
        context.fillText("중심극한정리 (Central Limit Theorem)", x, y);
        context.font = '16px Arial';
        
        y += 30;
        context.fillText(`현재 분포: ${distributions[currentDistribution].name}`, x, y);
        y += 25;
        context.fillText(`표본 크기: ${sampleSize}`, x, y);
        y += 25;
        context.fillText(`수집된 표본 평균 개수: ${sampleMeans.length}`, x, y);

        // Distribution explanations
        y += 40;
        context.fillStyle = colors.original;
        context.fillText("원래 분포 (상단)", x, y);
        y += 25;
        context.fillStyle = colors.samples;
        context.fillText("현재 표본 (중간)", x, y);
        y += 25;
        context.fillStyle = colors.means;
        context.fillText("표본평균의 분포 (하단)", x, y);
        y += 25;
        context.fillStyle = colors.normal;
        context.fillText("이론적 정규분포", x, y);

        // Controls
        y += 40;
        context.fillStyle = colors.text;
        context.fillText("Controls:", x, y);
        y += 25;
        context.fillText("Space: 일시정지", x, y);
        y += 25;
        context.fillText("1,2,3: 분포 변경", x, y);
        y += 25;
        context.fillText("↑/↓: 표본 크기 조절", x, y);

        context.restore();
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);

        drawGrid();
        drawSamplingProcess();
        drawExplanations();
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
            case 'Digit1':
                currentDistribution = "uniform";
                sampleMeans = [];
                break;
            case 'Digit2':
                currentDistribution = "exponential";
                sampleMeans = [];
                break;
            case 'Digit3':
                currentDistribution = "bimodal";
                sampleMeans = [];
                break;
            case 'ArrowUp':
                sampleSize = Math.min(100, sampleSize + 10);
                sampleMeans = [];
                break;
            case 'ArrowDown':
                sampleSize = Math.max(10, sampleSize - 10);
                sampleMeans = [];
                break;
        }
    });

    animate();
};