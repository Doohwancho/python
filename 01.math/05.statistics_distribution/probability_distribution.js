// probability_distribution.js - Part 1
window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    // Adjust scale based on screen size
    const scale = Math.min(width, height) / 15;
    let selectedDist = "normal";
    let activeType = "continuous";
    
    const colors = {
        distribution: "#00ff00",
        axis: "#ffffff",
        text: "#ffffff",
        grid: "#333333",
        discrete: "#ff8800",    
        continuous: "#00ffff",  
        highlight: "#ffff00"
    };

    // Center the coordinate system in the middle of the screen
    // Adjust the transform to account for the UI panel width
    const uiPanelWidth = 300; // Width of the UI panel
    const graphCenterX = (width + uiPanelWidth) / 2;
    const graphCenterY = height / 2;
    
    context.translate(graphCenterX, graphCenterY);
    context.scale(1, -1);

    // Create UI controls panel
    const controls = document.createElement('div');
    controls.style.cssText = `
        position: absolute;
        top: 20px;
        left: 20px;
        width: ${uiPanelWidth-40}px;
        color: white;
        background: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 10px;
        max-height: 90vh;
        overflow-y: auto;
    `;
    document.body.appendChild(controls);


    // Distribution type tabs
    const tabContainer = document.createElement('div');
    tabContainer.style.cssText = `
        display: flex;
        margin-bottom: 20px;
        gap: 10px;
    `;
    controls.appendChild(tabContainer);

    const discreteTab = createTab("이산확률분포");
    const continuousTab = createTab("연속확률분포");

    function createTab(text) {
        const tab = document.createElement('button');
        tab.textContent = text;
        tab.style.cssText = `
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background: #333;
            color: white;
            flex: 1;
        `;
        tabContainer.appendChild(tab);
        return tab;
    }

    discreteTab.addEventListener('click', () => switchType('discrete'));
    continuousTab.addEventListener('click', () => switchType('continuous'));

    function switchType(type) {
        activeType = type;
        discreteTab.style.background = type === 'discrete' ? '#666' : '#333';
        continuousTab.style.background = type === 'continuous' ? '#666' : '#333';
        updateDistributionList();
    }

    // Helper functions
    function factorial(n) {
        if (n === 0 || n === 1) return 1;
        if (n > 170) return Infinity; // Prevent overflow
        return n * factorial(n - 1);
    }

    function combination(n, k) {
        if (k > n) return 0;
        if (k === 0 || k === n) return 1;
        if (k > n - k) k = n - k;
        let result = 1;
        for (let i = 0; i < k; i++) {
            result *= (n - i);
            result /= (i + 1);
        }
        return result;
    }

    function gamma(z) {
        // Lanczos approximation for gamma function
        const p = [
            676.5203681218851,
            -1259.1392167224028,
            771.32342877765313,
            -176.61502916214059,
            12.507343278686905,
            -0.13857109526572012,
            9.9843695780195716e-6,
            1.5056327351493116e-7
        ];
        
        if (z < 0.5) {
            return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
        }
        
        z -= 1;
        let x = 0.99999999999980993;
        for (let i = 0; i < p.length; i++) {
            x += p[i] / (z + i + 1);
        }
        
        const t = z + p.length - 0.5;
        return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
    }

    function beta(x, y) {
        return (gamma(x) * gamma(y)) / gamma(x + y);
    }

    // Distributions object will be defined in Part 2...

    function createParamSlider(param, config, onChange) {
        const container = document.createElement('div');
        container.style.marginBottom = '10px';
        
        const label = document.createElement('div');
        label.innerHTML = `${param}: <span id="${param}Value">${config.value.toFixed(2)}</span>`;
        
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = config.min;
        slider.max = config.max;
        slider.step = config.step;
        slider.value = config.value;
        slider.style.width = '100%';
        
        slider.addEventListener('input', (e) => {
            config.value = parseFloat(e.target.value);
            label.querySelector('span').textContent = config.value.toFixed(2);
            onChange();
        });
        
        container.appendChild(label);
        container.appendChild(slider);
        return container;
    }

    function createDistributionCard(distName, dist) {
        const card = document.createElement('div');
        card.style.cssText = `
            background: rgba(50, 50, 50, 0.8);
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            cursor: pointer;
        `;
        
        const title = document.createElement('h3');
        title.textContent = dist.name;
        title.style.margin = '0 0 10px 0';
        
        const description = document.createElement('p');
        description.textContent = dist.description;
        description.style.fontSize = '14px';
        description.style.margin = '0 0 10px 0';
        
        card.appendChild(title);
        card.appendChild(description);
        
        const paramControls = document.createElement('div');
        Object.entries(dist.params).forEach(([param, config]) => {
            const slider = createParamSlider(param, config, draw);
            paramControls.appendChild(slider);
        });
        
        card.appendChild(paramControls);
        paramControls.style.display = selectedDist === distName ? 'block' : 'none';
        
        card.addEventListener('click', () => {
            selectedDist = distName;
            document.querySelectorAll('[data-dist-params]').forEach(el => el.style.display = 'none');
            paramControls.style.display = 'block';
            card.style.background = 'rgba(100, 100, 100, 0.8)';
            draw();
        });
        
        return card;
    }

    // Drawing functions will be continued in Part 2...

    // probability_distribution.js - Part 2
    const distributions = {
        // 이산확률분포
        bernoulli: {
            name: "베르누이분포 (Bernoulli)",
            type: "discrete",
            description: "한 번의 시행에서 성공/실패 확률",
            params: {
                p: { value: 0.5, min: 0, max: 1, step: 0.1 }
            },
            pmf: function(k, p) {
                if (k === 0) return 1 - p;
                if (k === 1) return p;
                return 0;
            },
            moments: function(p) {
                const mean = p;
                const variance = p * (1 - p);
                const skewness = (1 - 2*p) / Math.sqrt(variance);
                const kurtosis = (1 - 6*p*(1-p)) / variance;
                return { mean, variance, skewness, kurtosis };
            }
        },
        binomial: {
            name: "이항분포 (Binomial)",
            type: "discrete",
            description: "n번의 독립적인 베르누이 시행에서 성공 횟수",
            params: {
                n: { value: 10, min: 1, max: 20, step: 1 },
                p: { value: 0.5, min: 0, max: 1, step: 0.1 }
            },
            pmf: function(k, n, p) {
                return combination(n, k) * Math.pow(p, k) * Math.pow(1-p, n-k);
            },
            moments: function(n, p) {
                const mean = n * p;
                const variance = n * p * (1 - p);
                const skewness = (1 - 2*p) / Math.sqrt(n * p * (1-p));
                const kurtosis = 3 + (1 - 6*p*(1-p)) / (n * p * (1-p));
                return { mean, variance, skewness, kurtosis };
            }
        },
        negative_binomial: {
            name: "음이항분포 (Negative Binomial)",
            type: "discrete",
            description: "r번째 성공까지 필요한 시행 횟수",
            params: {
                r: { value: 3, min: 1, max: 10, step: 1 },
                p: { value: 0.5, min: 0, max: 1, step: 0.1 }
            },
            pmf: function(k, r, p) {
                return combination(k-1, r-1) * Math.pow(p, r) * Math.pow(1-p, k-r);
            }
        },
        poisson: {
            name: "포아송분포 (Poisson)",
            type: "discrete",
            description: "단위 시간/공간에서 발생하는 사건의 횟수",
            params: {
                lambda: { value: 3, min: 0.1, max: 10, step: 0.1 }
            },
            pmf: function(k, lambda) {
                return Math.pow(lambda, k) * Math.exp(-lambda) / factorial(k);
            },
            moments: function(lambda) {
                return {
                    mean: lambda,
                    variance: lambda,
                    skewness: 1 / Math.sqrt(lambda),
                    kurtosis: 3 + 1/lambda
                };
            }
        },
        hypergeometric: {
            name: "초기하분포 (Hypergeometric)",
            type: "discrete",
            description: "비복원 추출에서의 성공 횟수",
            params: {
                N: { value: 20, min: 10, max: 50, step: 1 },  // 전체 개수
                K: { value: 10, min: 5, max: 20, step: 1 },   // 성공 개수
                n: { value: 5, min: 1, max: 10, step: 1 }     // 추출 횟수
            },
            pmf: function(k, N, K, n) {
                return (combination(K, k) * combination(N-K, n-k)) / combination(N, n);
            }
        },

        // 연속확률분포
        normal: {
            name: "정규분포 (Normal)",
            type: "continuous",
            description: "대칭적인 종 모양의 분포, 중심극한정리의 기초",
            params: {
                mu: { value: 0, min: -5, max: 5, step: 0.1 },
                sigma: { value: 1, min: 0.1, max: 2, step: 0.1 }
            },
            pdf: function(x, mu, sigma) {
                return Math.exp(-0.5 * Math.pow((x - mu) / sigma, 2)) / (sigma * Math.sqrt(2 * Math.PI));
            },
            moments: function(mu, sigma) {
                return {
                    mean: mu,
                    variance: sigma * sigma,
                    skewness: 0,
                    kurtosis: 3
                };
            }
        },
        gamma: {
            name: "감마분포 (Gamma)",
            type: "continuous",
            description: "대기 시간이나 수명을 모델링, 지수분포의 일반화",
            params: {
                alpha: { value: 2, min: 0.1, max: 5, step: 0.1 },
                beta: { value: 1, min: 0.1, max: 5, step: 0.1 }
            },
            pdf: function(x, alpha, beta) {
                if (x <= 0) return 0;
                return Math.pow(beta, alpha) * Math.pow(x, alpha-1) * Math.exp(-beta * x) / gamma(alpha);
            },
            moments: function(alpha, beta) {
                return {
                    mean: alpha / beta,
                    variance: alpha / (beta * beta),
                    skewness: 2 / Math.sqrt(alpha),
                    kurtosis: 3 + 6/alpha
                };
            }
        },
        inverse_gamma: {
            name: "역감마분포 (Inverse Gamma)",
            type: "continuous",
            description: "베이지안 추론에서 분산의 사전분포로 사용",
            params: {
                alpha: { value: 2, min: 0.1, max: 5, step: 0.1 },
                beta: { value: 1, min: 0.1, max: 5, step: 0.1 }
            },
            pdf: function(x, alpha, beta) {
                if (x <= 0) return 0;
                return Math.pow(beta, alpha) * Math.pow(x, -alpha-1) * Math.exp(-beta/x) / gamma(alpha);
            }
        },
        chi_square: {
            name: "카이제곱분포 (Chi-square)",
            type: "continuous",
            description: "표본 분산과 가설검정에 사용",
            params: {
                df: { value: 3, min: 1, max: 10, step: 1 }
            },
            pdf: function(x, df) {
                if (x <= 0) return 0;
                return Math.pow(x, df/2-1) * Math.exp(-x/2) / (Math.pow(2, df/2) * gamma(df/2));
            },
            moments: function(df) {
                return {
                    mean: df,
                    variance: 2 * df,
                    skewness: Math.sqrt(8/df),
                    kurtosis: 3 + 12/df
                };
            }
        },
        beta: {
            name: "베타분포 (Beta)",
            type: "continuous",
            description: "비율이나 확률의 불확실성을 모델링",
            params: {
                alpha: { value: 2, min: 0.1, max: 5, step: 0.1 },
                beta: { value: 2, min: 0.1, max: 5, step: 0.1 }
            },
            pdf: function(x, alpha, beta_param) {
                if (x <= 0 || x >= 1) return 0;
                return Math.pow(x, alpha-1) * Math.pow(1-x, beta_param-1) / beta(alpha, beta_param);
            },
            moments: function(alpha, beta) {
                const mean = alpha / (alpha + beta);
                const variance = (alpha * beta) / (Math.pow(alpha + beta, 2) * (alpha + beta + 1));
                const skewness = 2 * (beta - alpha) * Math.sqrt(alpha + beta + 1) / 
                                ((alpha + beta + 2) * Math.sqrt(alpha * beta));
                const kurtosis = 3 * (alpha + beta + 1) * (2 * (alpha + beta)^2 + 
                                alpha * beta * (alpha + beta - 6)) / 
                                (alpha * beta * (alpha + beta + 2) * (alpha + beta + 3));
                return { mean, variance, skewness, kurtosis };
            }
        }
    };

    function drawMomentsInfo() {
        const dist = distributions[selectedDist];
        if (!dist || !dist.moments) return;
    
        const params = Object.values(dist.params).map(p => p.value);
        const moments = dist.moments(...params);
    
        context.save();
        context.scale(1, -1);
        
        // Create moments info box
        const boxWidth = 250;
        const boxHeight = 150;
        const boxX = width/2 - boxWidth - 50;  // Right side of the screen
        const boxY = -height/2 + 20;  // Top of the screen
        
        // Draw semi-transparent background
        context.fillStyle = 'rgba(0, 0, 0, 0.8)';
        context.fillRect(boxX, boxY, boxWidth, boxHeight);
        
        // Draw title
        context.font = '18px Arial';
        context.fillStyle = colors.text;
        context.fillText('모멘트 (Moments)', boxX + 10, boxY + 30);
        
        // Draw moments values
        context.font = '14px Arial';
        let yOffset = 60;
        
        // Format numbers to handle very small/large values
        const formatNumber = (num) => {
            if (Math.abs(num) < 0.0001 || Math.abs(num) > 9999) {
                return num.toExponential(3);
            }
            return num.toFixed(4);
        };
    
        const momentLabels = {
            mean: '평균 (Mean)',
            variance: '분산 (Variance)',
            skewness: '왜도 (Skewness)',
            kurtosis: '첨도 (Kurtosis)'
        };
    
        Object.entries(moments).forEach(([moment, value]) => {
            context.fillText(`${momentLabels[moment]}: ${formatNumber(value)}`, 
                            boxX + 10, boxY + yOffset);
            yOffset += 25;
        });
    
        // Visual indicators for skewness and kurtosis
        if (moments.skewness !== undefined && moments.kurtosis !== undefined) {
            // Draw small visualization of skewness
            const skewX = boxX + boxWidth - 60;
            const skewY = boxY + 60;
            const skewSize = 20;
            
            // Draw skewness indicator
            context.strokeStyle = colors.text;
            context.beginPath();
            if (Math.abs(moments.skewness) > 0.01) {
                // Draw skewed bell curve
                const direction = Math.sign(moments.skewness);
                context.moveTo(skewX - skewSize, skewY);
                context.quadraticCurveTo(
                    skewX + direction * skewSize, skewY - skewSize * 2,
                    skewX + skewSize, skewY
                );
            } else {
                // Draw symmetric curve
                context.moveTo(skewX - skewSize, skewY);
                context.quadraticCurveTo(
                    skewX, skewY - skewSize * 2,
                    skewX + skewSize, skewY
                );
            }
            context.stroke();
    
            // Draw kurtosis indicator
            const kurtX = skewX;
            const kurtY = skewY + 40;
            const kurtScale = (moments.kurtosis - 3) / 3; // Relative to normal distribution
            
            context.beginPath();
            context.moveTo(kurtX - skewSize, kurtY);
            context.quadraticCurveTo(
                kurtX, kurtY - skewSize * (2 + kurtScale),
                kurtX + skewSize, kurtY
            );
            context.stroke();
        }
    
        context.restore();
    }

    function updateDistributionList() {
        const container = document.getElementById('distributionList') || document.createElement('div');
        container.id = 'distributionList';
        container.innerHTML = '';
        
        Object.entries(distributions)
            .filter(([_, dist]) => dist.type === activeType)
            .forEach(([name, dist]) => {
                container.appendChild(createDistributionCard(name, dist));
            });
        
        if (!controls.contains(container)) {
            controls.appendChild(container);
        }
    }

// probability_distribution.js - Part 3

function drawGrid() {
    const gridSize = 10;
    context.strokeStyle = colors.grid;
    context.lineWidth = 0.5;

    // Draw grid lines
    for(let i = -gridSize; i <= gridSize; i++) {
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
    context.font = '16px Arial';
    context.fillStyle = colors.text;
    context.textAlign = 'center';

    // X-axis labels
    for(let i = -gridSize; i <= gridSize; i += 2) {
        context.fillText(i.toString(), i * scale, 25);
    }

    // Y-axis labels
    context.textAlign = 'right';
    for(let i = -gridSize; i <= gridSize; i += 2) {
        if(i !== 0) {
            context.fillText((i/5).toFixed(2), -10, -i * scale);
        }
    }

    // Axis titles
    context.font = '18px Arial';
    context.fillText("x", width/2 - 30, 25);
    context.fillText("f(x)", -30, -height/2 + 30);

    context.restore();
}


function drawDistribution() {
    const dist = distributions[selectedDist];
    if (!dist) return;

    const params = Object.values(dist.params).map(p => p.value);
    
    context.beginPath();
    context.strokeStyle = dist.type === 'discrete' ? colors.discrete : colors.continuous;
    context.lineWidth = 2;

    if (dist.type === "continuous") {
        let xMin = -5, xMax = 5;
        if (selectedDist === 'beta') {
            xMin = 0; xMax = 1;
        } else if (['gamma', 'inverse_gamma', 'chi_square'].includes(selectedDist)) {
            xMin = 0; xMax = 10;
        }

        let firstValid = true;
        for(let px = xMin; px <= xMax; px += 0.1) {
            const y = dist.pdf(px, ...params);
            if (!isNaN(y) && isFinite(y)) {
                const screenX = px * scale;
                const screenY = y * scale * 5;

                if (firstValid) {
                    context.moveTo(screenX, screenY);
                    firstValid = false;
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
        }
        context.stroke();
    } else {
        // Discrete distribution drawing code...
        let maxK = 10;
        switch(selectedDist) {
            case 'bernoulli': maxK = 1; break;
            case 'binomial': maxK = params[0]; break;
            case 'negative_binomial': maxK = params[0] * 3; break;
            case 'poisson': maxK = Math.min(20, params[0] * 3); break;
            case 'hypergeometric': maxK = params[2]; break;
        }

        for(let k = 0; k <= maxK; k++) {
            const prob = dist.pmf(k, ...params);
            if (!isNaN(prob) && isFinite(prob)) {
                const screenX = k * scale;
                const screenY = prob * scale * 5;

                // Stem
                context.beginPath();
                context.moveTo(screenX, 0);
                context.lineTo(screenX, screenY);
                context.stroke();

                // Point
                context.beginPath();
                context.arc(screenX, screenY, 4, 0, Math.PI * 2);
                context.fill();
            }
        }
    }
}

function drawDistributionInfo() {
    const dist = distributions[selectedDist];
    if (!dist) return;

    context.save();
    context.scale(1, -1);
    context.font = '18px Arial';
    context.fillStyle = colors.text;
    context.textAlign = 'left';

    // Draw info box
    const boxPadding = 20;
    const boxX = -width/2 + 20;
    const boxY = -height/2 + 20;
    
    context.fillStyle = 'rgba(0, 0, 0, 0.7)';
    context.fillRect(boxX, boxY, 300, 100);
    
    context.fillStyle = colors.text;
    context.fillText(dist.name, boxX + boxPadding, boxY + 30);
    
    context.font = '14px Arial';
    context.fillText(dist.description, boxX + boxPadding, boxY + 60);
    
    // Add type indicator
    context.fillStyle = dist.type === 'discrete' ? colors.discrete : colors.continuous;
    context.fillText(
        dist.type === 'discrete' ? '이산확률분포' : '연속확률분포',
        boxX + boxPadding,
        boxY + 85
    );

    context.restore();
}

// Add explanatory tooltips
function addMomentTooltips() {
    const tooltips = {
        mean: "평균은 확률분포의 중심 위치를 나타냅니다.",
        variance: "분산은 평균으로부터의 퍼짐 정도를 나타냅니다.",
        skewness: "왜도는 분포의 비대칭성을 측정합니다. 양수면 오른쪽으로, 음수면 왼쪽으로 치우침을 의미합니다.",
        kurtosis: "첨도는 분포의 뾰족한 정도를 나타냅니다. 정규분포는 3입니다."
    };

    const tooltip = document.createElement('div');
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-size: 14px;
        display: none;
        pointer-events: none;
    `;
    document.body.appendChild(tooltip);

    // Add event listeners for moments box
    canvas.addEventListener('mousemove', (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Check if mouse is over moments area and show appropriate tooltip
        // Add logic here to show tooltips based on mouse position
    });
}

function draw() {
    // Clear canvas
    context.fillStyle = 'black';
    context.fillRect(-width, -height, width * 2, height * 2);
    
    drawGrid();
    drawDistribution();
    drawDistributionInfo();
    drawMomentsInfo();  // Add this line
}

// Initialize UI and draw
switchType('continuous');  // Start with continuous distributions
draw();

// Add window resize handler
window.addEventListener('resize', function() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const newGraphCenterX = (canvas.width + uiPanelWidth) / 2;
    const newGraphCenterY = canvas.height / 2;
    context.translate(newGraphCenterX, newGraphCenterY);
    context.scale(1, -1);
    draw();
});
}
