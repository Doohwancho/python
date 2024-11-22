window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 15;
    let animationPhase = 0;  // Control different visualization phases
    let isAnimating = true;
    let currentTime = 0;
    let samples = [];
    let confidenceInterval = null;
    
    const colors = {
        population: "#00ff00",
        sample: "#ff8800",
        statistic: "#00ffff",
        parameter: "#ff0000",
        hypothesis: "#ffff00",
        error: "#ff00ff",
        text: "#ffffff",
        grid: "#333333",
        axis: "#ffffff"
    };

    // Center the coordinate system
    const graphCenterX = width * 0.5;
    const graphCenterY = height * 0.5;
    context.translate(graphCenterX, graphCenterY);
    context.scale(1, -1);


    const phases = [
        {
            title: "1단계: 모집단 (Population)",
            description: [
                "• 모집단: 관심 있는 전체 대상",
                "• 모수: 모집단의 특성 (평균 μ=0, 표준편차 σ=1)",
                "• 이 예제에서는 정규분포 N(0,1)을 사용",
                "",
                "현재 보이는 녹색 곡선이 모집단의 분포입니다.",
                "스페이스바를 눌러 다음 단계로 진행하세요."
            ]
        },
        {
            title: "2단계: 표본 추출 (Sampling)",
            description: [
                "• 표본: 모집단에서 무작위로 선택된 부분집합",
                "• 표본 크기: n=30",
                "• 주황색 점: 각 표본의 평균",
                "• 반투명 주황색 곡선: 각 표본의 분포",
                "",
                "여러 표본이 추출되는 과정을 보여줍니다."
            ]
        },
        {
            title: "3단계: 표본 분포 (Sampling Distribution)",
            description: [
                "• 표본 분포: 표본 통계량(평균)들의 분포",
                "• 중심극한정리에 의해 정규분포에 근사",
                "• 표준 오차: σ/√n",
                "",
                "주황색 점들의 분포가 표본 평균들의 분포를 나타냅니다."
            ]
        },
        {
            title: "4단계: 신뢰 구간 (Confidence Interval)",
            description: [
                "• 95% 신뢰구간: 모수가 포함될 것으로 기대되는 구간",
                "• 빨간색 선: 신뢰구간의 범위",
                "• 계산: 표본평균 ± (1.96 × 표준오차)",
                "",
                "이 구간은 반복적인 표본 추출에서 95%의 확률로",
                "진정한 모수를 포함합니다."
            ]
        },
        {
            title: "5단계: 가설 검정 (Hypothesis Testing)",
            description: [
                "• 귀무가설(H₀): μ = 0",
                "• 대립가설(H₁): μ ≠ 0",
                "• 유의수준: α = 0.05 (5%)",
                "• 분홍색 영역: 기각역 (Type I 오류 위험)",
                "",
                "기각역을 벗어나면 귀무가설을 기각합니다."
            ]
        }
    ];


    // Population parameters
    const populationMean = 0;
    const populationStd = 1;
    
    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -10; i <= 10; i++) {
            if(i === 0) continue;
            
            // Vertical grid lines
            context.beginPath();
            context.moveTo(i * scale, -height/2);
            context.lineTo(i * scale, height/2);
            context.stroke();

            // Horizontal grid lines
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
        context.fillText("x", width/2 - 20, 20);

        // Y-axis labels
        context.textAlign = 'right';
        for(let i = -5; i <= 5; i++) {
            if(i !== 0) {
                context.fillText((i/5).toFixed(2), -10, -i * scale);
            }
        }
        context.fillText("y", -10, -height/2 + 20);

        context.restore();
    }

    function drawPhaseInfo() {
        const currentPhase = phases[Math.floor(animationPhase)];
        if (!currentPhase) return;

        context.save();
        context.scale(1, -1);

        // Draw phase title
        context.font = 'bold 24px Arial';
        context.fillStyle = colors.text;
        context.fillText(currentPhase.title, -width/2 + 50, -height/2 + 50);

        // Draw description
        context.font = '16px Arial';
        let yPos = -height/2 + 100;
        currentPhase.description.forEach(line => {
            context.fillText(line, -width/2 + 50, yPos);
            yPos += 25;
        });

        // Draw progress indicator
        const totalPhases = phases.length;
        const progress = `${Math.floor(animationPhase + 1)}/${totalPhases}`;
        context.fillText(`진행 단계: ${progress}`, -width/2 + 50, height/2 - 30);

        context.restore();
    }

    function normalPDF(x, mean, std) {
        return Math.exp(-0.5 * Math.pow((x - mean) / std, 2)) / (std * Math.sqrt(2 * Math.PI));
    }

    function generateSample(size = 30) {
        // Box-Muller transform for normal distribution
        let sample = [];
        for(let i = 0; i < size; i++) {
            let u1 = Math.random();
            let u2 = Math.random();
            let z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
            sample.push(z * populationStd + populationMean);
        }
        return sample;
    }

    function calculateSampleStatistics(sample) {
        const mean = sample.reduce((a, b) => a + b) / sample.length;
        const variance = sample.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (sample.length - 1);
        return { mean, std: Math.sqrt(variance) };
    }

    function drawPopulation() {
        context.beginPath();
        context.strokeStyle = colors.population;
        context.lineWidth = 2;

        // Draw normal distribution
        for(let x = -4; x <= 4; x += 0.1) {
            const y = normalPDF(x, populationMean, populationStd);
            const screenX = x * scale;
            const screenY = y * scale * 5;

            if(x === -4) {
                context.moveTo(screenX, screenY);
            } else {
                context.lineTo(screenX, screenY);
            }
        }
        context.stroke();

        // Label population parameters
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.population;
        context.fillText(`모집단 (Population): N(${populationMean}, ${populationStd}²)`, -scale * 4, -scale * 2);
        context.restore();
    }

    function drawSamples() {
        // Draw sample points
        samples.forEach(sample => {
            const stats = calculateSampleStatistics(sample);
            
            // Draw sample mean
            context.beginPath();
            context.arc(stats.mean * scale, 0, 5, 0, Math.PI * 2);
            context.fillStyle = colors.sample;
            context.fill();

            // Draw sample distribution
            context.beginPath();
            context.strokeStyle = colors.sample + '40';  // Add transparency
            context.lineWidth = 1;
            
            for(let x = -4; x <= 4; x += 0.1) {
                const y = normalPDF(x, stats.mean, stats.std);
                const screenX = x * scale;
                const screenY = y * scale * 3;

                if(x === -4) {
                    context.moveTo(screenX, screenY);
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
            context.stroke();
        });
    }

    function drawConfidenceInterval() {
        if (!confidenceInterval) return;

        const { lower, upper } = confidenceInterval;
        
        // Draw interval
        context.beginPath();
        context.strokeStyle = colors.parameter;
        context.lineWidth = 3;
        context.moveTo(lower * scale, -scale);
        context.lineTo(upper * scale, -scale);
        context.stroke();

        // Draw endpoints
        context.beginPath();
        context.moveTo(lower * scale, -scale - 10);
        context.lineTo(lower * scale, -scale + 10);
        context.stroke();

        context.beginPath();
        context.moveTo(upper * scale, -scale - 10);
        context.lineTo(upper * scale, -scale + 10);
        context.stroke();

        // Label
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.parameter;
        context.fillText(`95% 신뢰구간: (${lower.toFixed(2)}, ${upper.toFixed(2)})`, -scale * 4, scale);
        context.restore();
    }

    function drawHypothesisTest() {
        const nullHypothesis = 0;  // H₀: μ = 0
        const criticalValue = 1.96;  // For 95% confidence level

        // Draw null hypothesis distribution
        context.beginPath();
        context.strokeStyle = colors.hypothesis;
        context.lineWidth = 2;
        
        for(let x = -4; x <= 4; x += 0.1) {
            const y = normalPDF(x, nullHypothesis, 1/Math.sqrt(30));  // Standard error
            const screenX = x * scale;
            const screenY = y * scale * 10;

            if(x === -4) {
                context.moveTo(screenX, screenY);
            } else {
                context.lineTo(screenX, screenY);
            }
        }
        context.stroke();

        // Draw critical regions
        context.fillStyle = colors.error + '40';
        
        // Left critical region
        context.beginPath();
        let y0 = 0;
        for(let x = -4; x <= -criticalValue; x += 0.1) {
            const y = normalPDF(x, nullHypothesis, 1/Math.sqrt(30)) * scale * 10;
            if(x === -4) {
                context.moveTo(x * scale, y0);
            }
            context.lineTo(x * scale, y);
        }
        context.lineTo(-criticalValue * scale, y0);
        context.fill();

        // Right critical region
        context.beginPath();
        for(let x = criticalValue; x <= 4; x += 0.1) {
            const y = normalPDF(x, nullHypothesis, 1/Math.sqrt(30)) * scale * 10;
            if(x === criticalValue) {
                context.moveTo(x * scale, y0);
            }
            context.lineTo(x * scale, y);
        }
        context.lineTo(4 * scale, y0);
        context.fill();
    }

    function drawExplanations() {
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        
        let yPos = -height/2 + 30;
        const xPos = -width/2 + 20;

        const phases = [
            "1. 모집단 (Population): 정규분포 N(0, 1)",
            "2. 표본 추출 (Sampling): n=30인 표본들",
            "3. 표본 분포 (Sampling Distribution): 표본 평균들의 분포",
            "4. 신뢰 구간 (Confidence Interval): 95% 신뢰수준",
            "5. 가설 검정 (Hypothesis Testing): H₀: μ = 0",
            "Space Bar: 다음 단계로"
        ];

        phases.forEach((text, i) => {
            context.fillStyle = i === Math.floor(animationPhase) ? colors.highlight : colors.text;
            context.fillText(text, xPos, yPos);
            yPos += 25;
        });

        context.restore();
    }

    function drawSamplingDistribution() {
        if (samples.length === 0) return;
    
        // Calculate mean and standard error of sample means
        const sampleMeans = samples.map(s => calculateSampleStatistics(s).mean);
        const meanOfMeans = sampleMeans.reduce((a,b) => a+b) / sampleMeans.length;
        const stdError = 1/Math.sqrt(30);  // Theoretical standard error
    
        // Draw sampling distribution curve
        context.beginPath();
        context.strokeStyle = colors.statistic;
        context.lineWidth = 2;
    
        for(let x = -4; x <= 4; x += 0.1) {
            const y = normalPDF(x, meanOfMeans, stdError);
            const screenX = x * scale;
            const screenY = y * scale * 8;  // Scale up for visibility
    
            if(x === -4) {
                context.moveTo(screenX, screenY);
            } else {
                context.lineTo(screenX, screenY);
            }
        }
        context.stroke();
    
        // Draw all sample means as points
        sampleMeans.forEach(mean => {
            context.beginPath();
            context.arc(mean * scale, 0, 5, 0, Math.PI * 2);
            context.fillStyle = colors.sample;
            context.fill();
        });
    
        // Label
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.statistic;
        context.fillText(`표본평균의 분포 (SE = ${stdError.toFixed(3)})`, -scale * 4, -scale * 3);
        context.restore();
    }

    function updateAnimation() {
        if(animationPhase < 1) {
            // Phase 0: Show population
        } else if(animationPhase < 2) {
            // Phase 1: Generate samples
            if(currentTime % 30 === 0 && samples.length < 10) {
                samples.push(generateSample());
            }
        } else if(animationPhase < 3) {
            // Phase 2: Show sampling distribution
            if(samples.length < 10 && currentTime % 30 === 0) {
                samples.push(generateSample());
            }
        } else if(animationPhase < 4) {
            // Phase 3: Show confidence interval
            if(!confidenceInterval) {
                const sampleMeans = samples.map(s => calculateSampleStatistics(s).mean);
                const meanOfMeans = sampleMeans.reduce((a,b) => a+b) / sampleMeans.length;
                const stdError = 1/Math.sqrt(30);
                confidenceInterval = {
                    lower: meanOfMeans - 1.96 * stdError,
                    upper: meanOfMeans + 1.96 * stdError
                };
            }
        }
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);
    
        // Draw grid and axes
        drawGrid();
    
        // Draw statistical elements based on current phase
        switch(Math.floor(animationPhase)) {
            case 0:
                drawPopulation();
                break;
            case 1:
                drawPopulation();
                drawSamples();
                break;
            case 2:
                drawPopulation();
                drawSamples();
                drawSamplingDistribution();
                break;
            case 3:
                drawPopulation();
                drawSamples();
                drawSamplingDistribution();
                drawConfidenceInterval();
                break;
            case 4:
                drawPopulation();
                drawSamples();
                drawSamplingDistribution();
                drawConfidenceInterval();
                drawHypothesisTest();
                break;
        }
    
        // Draw phase information
        drawPhaseInfo();
    }

    // Handle space bar to advance phases
    document.addEventListener('keydown', function(event) {
        if(event.code === 'Space') {
            event.preventDefault();
            animationPhase = Math.min(animationPhase + 1, phases.length - 1);
            if(!isAnimating) {
                isAnimating = true;
                animate();
            }
        }
    });

    function animate() {
        if(isAnimating) {
            currentTime++;
            updateAnimation();
            draw();
            requestAnimationFrame(animate);
        }
    }

    animate();
};