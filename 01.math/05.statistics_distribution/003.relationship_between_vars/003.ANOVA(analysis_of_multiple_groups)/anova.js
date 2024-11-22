window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 12;
    let isAnimating = true;
    let currentTime = 0;
    
    const colors = {
        group1: "#ff0000",     // Red for group 1
        group2: "#00ff00",     // Green for group 2
        group3: "#0088ff",     // Blue for group 3
        mean: "#ffff00",       // Yellow for means
        grandMean: "#ffffff",  // White for grand mean
        variance: "#ff00ff",   // Magenta for variance
        grid: "#333333",
        axis: "#ffffff",
        text: "#ffffff"
    };

    // Center coordinate system
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // Generate sample data for multiple groups
    function generateGroupData(mean, std, n = 30) {
        return Array.from({length: n}, () => 
            mean + std * randNormal()
        );
    }

    function randNormal() {
        const u1 = Math.random();
        const u2 = Math.random();
        return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    }

    // Calculate basic statistics
    function calculateStats(data) {
        const mean = data.reduce((a, b) => a + b, 0) / data.length;
        const variance = data.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (data.length - 1);
        return { mean, variance, std: Math.sqrt(variance) };
    }

    // Calculate ANOVA statistics
    function calculateANOVA(groups) {
        // Calculate grand mean
        const allData = groups.flat();
        const grandMean = allData.reduce((a, b) => a + b, 0) / allData.length;

        // Calculate SSB (Between-group Sum of Squares)
        const SSB = groups.reduce((sum, group) => {
            const groupMean = group.reduce((a, b) => a + b, 0) / group.length;
            return sum + group.length * Math.pow(groupMean - grandMean, 2);
        }, 0);

        // Calculate SSW (Within-group Sum of Squares)
        const SSW = groups.reduce((sum, group) => {
            const groupMean = group.reduce((a, b) => a + b, 0) / group.length;
            return sum + group.reduce((s, x) => s + Math.pow(x - groupMean, 2), 0);
        }, 0);

        // Calculate degrees of freedom
        const dfb = groups.length - 1;  // between groups
        const dfw = allData.length - groups.length;  // within groups

        // Calculate Mean Squares
        const MSB = SSB / dfb;
        const MSW = SSW / dfw;

        // Calculate F-statistic
        const F = MSB / MSW;

        return {
            SSB, SSW, MSB, MSW, F,
            dfb, dfw,
            grandMean
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

        // X-axis labels (group positions)
        for(let i = -4; i <= 4; i += 2) {
            context.fillText(i.toString(), i * scale, 20);
        }

        // Y-axis labels (values)
        for(let i = -4; i <= 4; i += 1) {
            if(i !== 0) {
                context.fillText(i.toString(), -20, -i * scale);
            }
        }

        context.restore();
    }

    function drawGroupData(data, xPos, color, label) {
        const stats = calculateStats(data);
        
        // Draw points
        data.forEach(y => {
            context.beginPath();
            context.arc(xPos * scale, y * scale, 3, 0, Math.PI * 2);
            context.fillStyle = color;
            context.fill();
        });

        // Draw mean line
        context.beginPath();
        context.strokeStyle = colors.mean;
        context.lineWidth = 2;
        context.moveTo((xPos - 0.2) * scale, stats.mean * scale);
        context.lineTo((xPos + 0.2) * scale, stats.mean * scale);
        context.stroke();

        // Draw variance bars (±1 standard deviation)
        context.beginPath();
        context.strokeStyle = colors.variance;
        context.setLineDash([5, 5]);
        context.moveTo(xPos * scale, (stats.mean - stats.std) * scale);
        context.lineTo(xPos * scale, (stats.mean + stats.std) * scale);
        context.stroke();
        context.setLineDash([]);

        // Add label
        context.save();
        context.scale(1, -1);
        context.font = '14px Arial';
        context.fillStyle = color;
        context.textAlign = 'center';
        context.fillText(label, xPos * scale, -stats.mean * scale - 20);
        context.fillText(`μ = ${stats.mean.toFixed(2)}`, xPos * scale, -stats.mean * scale - 40);
        context.fillText(`σ = ${stats.std.toFixed(2)}`, xPos * scale, -stats.mean * scale - 60);
        context.restore();

        return stats;
    }

    function drawANOVAStats(anovaResults) {
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';

        const x = -width/2 + 20;
        let y = -height/2 + 40;

        // ANOVA Results
        context.fillText("ANOVA 결과:", x, y);
        y += 25;
        context.fillText(`F(${anovaResults.dfb}, ${anovaResults.dfw}) = ${anovaResults.F.toFixed(3)}`, x, y);
        y += 25;
        context.fillText(`MSB = ${anovaResults.MSB.toFixed(3)}`, x, y);
        y += 25;
        context.fillText(`MSW = ${anovaResults.MSW.toFixed(3)}`, x, y);
        y += 25;

        // Significance interpretation
        const criticalF = 3.15;  // Example critical F value for α=0.05
        const isSignificant = anovaResults.F > criticalF;
        context.fillStyle = isSignificant ? "#00ff00" : "#ff0000";
        context.fillText(
            isSignificant ? "그룹 간 유의한 차이가 있습니다" : "그룹 간 유의한 차이가 없습니다",
            x, y
        );

        context.restore();
    }

    function drawVisualization() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);

        // Draw grid
        drawGrid();

        // Generate and draw group data
        const time = currentTime * 0.01;
        const group1 = generateGroupData(-1 + Math.sin(time), 0.5);
        const group2 = generateGroupData(0 + Math.cos(time), 0.5);
        const group3 = generateGroupData(1 + Math.sin(time), 0.5);

        drawGroupData(group1, -2, colors.group1, "Group 1");
        drawGroupData(group2, 0, colors.group2, "Group 2");
        drawGroupData(group3, 2, colors.group3, "Group 3");

        // Calculate and draw ANOVA results
        const anovaResults = calculateANOVA([group1, group2, group3]);
        drawANOVAStats(anovaResults);

        // Draw grand mean line
        context.beginPath();
        context.strokeStyle = colors.grandMean;
        context.lineWidth = 2;
        context.setLineDash([10, 5]);
        context.moveTo(-scale * 3, anovaResults.grandMean * scale);
        context.lineTo(scale * 3, anovaResults.grandMean * scale);
        context.stroke();
        context.setLineDash([]);

        // Add grand mean label
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.grandMean;
        context.textAlign = 'right';
        context.fillText(
            `Grand Mean: ${anovaResults.grandMean.toFixed(3)}`,
            width/2 - 20,
            -anovaResults.grandMean * scale - 20
        );
        context.restore();
    }

    function animate() {
        if(isAnimating) {
            currentTime++;
            drawVisualization();
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