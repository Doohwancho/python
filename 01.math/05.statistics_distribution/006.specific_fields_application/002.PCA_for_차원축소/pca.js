window.onload = function () {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = (canvas.width = window.innerWidth),
        height = (canvas.height = window.innerHeight);

    const scale = Math.min(width, height) / 12;
    let isAnimating = true;
    let currentTime = 0;
    let rotationAngle = 0;
    
    const colors = {
        xAxis: "#ff0000",      // Red for x-axis
        yAxis: "#00ff00",      // Green for y-axis
        zAxis: "#0088ff",      // Blue for z-axis
        grid: "#333333",
        points: "#ffff00",
        pc1: "#ff00ff",        // Magenta for PC1
        pc2: "#00ffff",        // Cyan for PC2
        projection: "#ffffff",
        text: "#ffffff"
    };

    // Center coordinate system
    context.translate(width / 2, height / 2);
    context.scale(1, -1);

    // 3D to 2D projection matrices
    const iso = {
        angle: Math.PI / 6,  // 30 degrees for isometric view
        cos: Math.cos(Math.PI / 6),
        sin: Math.sin(Math.PI / 6)
    };

    // Project 3D point to 2D using isometric projection
    function project(x, y, z) {
        const rotatedX = x * Math.cos(rotationAngle) - z * Math.sin(rotationAngle);
        const rotatedZ = x * Math.sin(rotationAngle) + z * Math.cos(rotationAngle);
        
        return {
            x: (rotatedX - rotatedZ) * iso.cos * scale,
            y: (y + (rotatedX + rotatedZ) * iso.sin) * scale
        };
    }

    // Generate 3D data with correlation and noise
    function generate3DData(n = 100) {
        const data = [];
        for(let i = 0; i < n; i++) {
            // Generate correlated data along a primary direction
            const t = Math.random() * 2 - 1;
            const noise = 0.2;
            data.push({
                x: 2 * t + noise * (Math.random() - 0.5),
                y: 1.5 * t + noise * (Math.random() - 0.5),
                z: t + noise * (Math.random() - 0.5)
            });
        }
        return data;
    }

    // Generate sample 2D data
    function generate2DData(n = 100) {
        const data = [];
        for(let i = 0; i < n; i++) {
            const t = Math.random() * 2 - 1;
            const noise = 0.2;
            data.push({
                x: 2 * t + noise * (Math.random() - 0.5),
                y: 1.5 * t + noise * (Math.random() - 0.5)
            });
        }
        return data;
    }

    // Calculate principal components
    function calculatePCA(data) {
        // Center the data
        const mean = {
            x: data.reduce((sum, p) => sum + p.x, 0) / data.length,
            y: data.reduce((sum, p) => sum + p.y, 0) / data.length
        };
        
        const centered = data.map(p => ({
            x: p.x - mean.x,
            y: p.y - mean.y
        }));

        // Calculate covariance matrix
        const cxx = centered.reduce((sum, p) => sum + p.x * p.x, 0) / data.length;
        const cyy = centered.reduce((sum, p) => sum + p.y * p.y, 0) / data.length;
        const cxy = centered.reduce((sum, p) => sum + p.x * p.y, 0) / data.length;

        // Calculate eigenvectors
        const trace = cxx + cyy;
        const det = cxx * cyy - cxy * cxy;
        const lambda1 = (trace + Math.sqrt(trace * trace - 4 * det)) / 2;
        const lambda2 = (trace - Math.sqrt(trace * trace - 4 * det)) / 2;

        const pc1 = {
            x: cxy,
            y: lambda1 - cxx
        };
        const pc2 = {
            x: cxy,
            y: lambda2 - cxx
        };

        // Normalize principal components
        const mag1 = Math.sqrt(pc1.x * pc1.x + pc1.y * pc1.y);
        const mag2 = Math.sqrt(pc2.x * pc2.x + pc2.y * pc2.y);

        return {
            pc1: { x: pc1.x / mag1, y: pc1.y / mag1 },
            pc2: { x: pc2.x / mag2, y: pc2.y / mag2 },
            mean: mean,
            eigenvalues: [lambda1, lambda2]
        };
    }

    // Project point onto vector
    function projectPoint(point, vector) {
        const dot = point.x * vector.x + point.y * vector.y;
        return {
            x: vector.x * dot,
            y: vector.y * dot
        };
    }

    function drawAxis(color, start, end, label) {
        const startProj = project(start.x, start.y, start.z);
        const endProj = project(end.x, end.y, end.z);

        // Draw axis line
        context.beginPath();
        context.strokeStyle = color;
        context.lineWidth = 2;
        context.moveTo(startProj.x, startProj.y);
        context.lineTo(endProj.x, endProj.y);
        context.stroke();

        // Draw arrow head
        const headLength = 20;
        const dx = endProj.x - startProj.x;
        const dy = endProj.y - startProj.y;
        const angle = Math.atan2(dy, dx);

        context.beginPath();
        context.moveTo(endProj.x, endProj.y);
        context.lineTo(
            endProj.x - headLength * Math.cos(angle - Math.PI/6),
            endProj.y - headLength * Math.sin(angle - Math.PI/6)
        );
        context.lineTo(
            endProj.x - headLength * Math.cos(angle + Math.PI/6),
            endProj.y - headLength * Math.sin(angle + Math.PI/6)
        );
        context.closePath();
        context.fillStyle = color;
        context.fill();

        // Draw label
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = color;
        context.textAlign = 'center';
        context.fillText(label, endProj.x, -endProj.y - 20);
        context.restore();
    }

    function drawGrid3D() {
        const gridSize = 2;
        const step = 0.5;
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw XY grid
        for(let x = -gridSize; x <= gridSize; x += step) {
            for(let y = -gridSize; y <= gridSize; y += step) {
                const start = project(x, y, -gridSize);
                const end = project(x, y, gridSize);
                context.beginPath();
                context.moveTo(start.x, start.y);
                context.lineTo(end.x, end.y);
                context.stroke();

                const start2 = project(-gridSize, y, x);
                const end2 = project(gridSize, y, x);
                context.beginPath();
                context.moveTo(start2.x, start2.y);
                context.lineTo(end2.x, end2.y);
                context.stroke();
            }
        }

        // Draw axes
        drawAxis(colors.xAxis, {x: 0, y: 0, z: 0}, {x: 2, y: 0, z: 0}, "X");
        drawAxis(colors.yAxis, {x: 0, y: 0, z: 0}, {x: 0, y: 2, z: 0}, "Y");
        drawAxis(colors.zAxis, {x: 0, y: 0, z: 0}, {x: 0, y: 0, z: 2}, "Z");
    }

    function drawPoint3D(point, color = colors.points, size = 3) {
        const proj = project(point.x, point.y, point.z);
        context.beginPath();
        context.arc(proj.x, proj.y, size, 0, Math.PI * 2);
        context.fillStyle = color;
        context.fill();
    }

    function drawPrincipalComponents(data) {
        // Calculate covariance matrix
        const mean = {
            x: data.reduce((sum, p) => sum + p.x, 0) / data.length,
            y: data.reduce((sum, p) => sum + p.y, 0) / data.length,
            z: data.reduce((sum, p) => sum + p.z, 0) / data.length
        };

        // Draw PC1 and PC2 (simplified for visualization)
        const pc1 = {x: 1, y: 1, z: 1};  // Simplified PC1 direction
        const pc2 = {x: -1, y: 1, z: 0}; // Simplified PC2 direction
        const length = 2;

        // Draw PC1
        const pc1Start = project(-pc1.x * length, -pc1.y * length, -pc1.z * length);
        const pc1End = project(pc1.x * length, pc1.y * length, pc1.z * length);
        context.beginPath();
        context.strokeStyle = colors.pc1;
        context.lineWidth = 2;
        context.moveTo(pc1Start.x, pc1Start.y);
        context.lineTo(pc1End.x, pc1End.y);
        context.stroke();

        // Draw PC2
        const pc2Start = project(-pc2.x * length, -pc2.y * length, -pc2.z * length);
        const pc2End = project(pc2.x * length, pc2.y * length, pc2.z * length);
        context.beginPath();
        context.strokeStyle = colors.pc2;
        context.lineWidth = 2;
        context.moveTo(pc2Start.x, pc2Start.y);
        context.lineTo(pc2End.x, pc2End.y);
        context.stroke();
    }

    function drawProjectionPlane() {
        // Draw semi-transparent plane representing the projection surface
        const planeSize = 2;
        const corners = [
            project(-planeSize, -planeSize, 0),
            project(planeSize, -planeSize, 0),
            project(planeSize, planeSize, 0),
            project(-planeSize, planeSize, 0)
        ];

        context.beginPath();
        context.moveTo(corners[0].x, corners[0].y);
        corners.forEach(corner => {
            context.lineTo(corner.x, corner.y);
        });
        context.closePath();
        context.fillStyle = "rgba(255, 255, 255, 0.1)";
        context.fill();
    }

    function drawExplanation() {
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';
        
        let yPos = -height/2 + 30;
        const xPos = -width/2 + 20;

        context.fillText("3D PCA Visualization", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.pc1;
        context.fillText("First Principal Component (PC1)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.pc2;
        context.fillText("Second Principal Component (PC2)", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.points;
        context.fillText("Data Points", xPos, yPos);
        yPos += 25;
        context.fillStyle = colors.text;
        context.fillText("Use Space to pause/resume rotation", xPos, yPos);

        context.restore();
    }

    function drawGrid() {
        context.strokeStyle = colors.grid;
        context.lineWidth = 0.5;

        // Draw grid lines
        for(let i = -10; i <= 10; i++) {
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
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'center';

        // Axis labels
        for(let i = -5; i <= 5; i++) {
            if(i !== 0) {
                context.fillText(i.toString(), i * scale, 20);
                context.fillText(i.toString(), -20, -i * scale);
            }
        }

        context.fillText("x", width/2 - 20, 20);
        context.fillText("y", -20, -height/2 + 20);

        context.restore();
    }

    function draw3Dto2D() {
        const data = generate3DData();
        
        // Project 3D to 2D (simple orthographic projection)
        const projected = data.map(p => ({
            x: p.x * Math.cos(rotationAngle) - p.z * Math.sin(rotationAngle),
            y: p.y
        }));

        // Calculate PCA for projected data
        const pca = calculatePCA(projected);

        // Draw projected points
        projected.forEach(point => {
            context.beginPath();
            context.arc(point.x * scale, point.y * scale, 3, 0, Math.PI * 2);
            context.fillStyle = colors.points;
            context.fill();
        });

        // Draw principal components
        const length = scale * 2;
        
        // PC1
        context.beginPath();
        context.strokeStyle = colors.pc1;
        context.lineWidth = 2;
        context.moveTo(-pca.pc1.x * length, -pca.pc1.y * length);
        context.lineTo(pca.pc1.x * length, pca.pc1.y * length);
        context.stroke();

        // PC2
        context.beginPath();
        context.strokeStyle = colors.pc2;
        context.moveTo(-pca.pc2.x * length, -pca.pc2.y * length);
        context.lineTo(pca.pc2.x * length, pca.pc2.y * length);
        context.stroke();

        // Draw projections onto PC1
        projected.forEach(point => {
            const proj = projectPoint(point, pca.pc1);
            context.beginPath();
            context.strokeStyle = colors.projection + '40';
            context.moveTo(point.x * scale, point.y * scale);
            context.lineTo(proj.x * scale, proj.y * scale);
            context.stroke();
        });

        // Add explanatory text
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';
        
        let yPos = -height/2 + 30;
        context.fillText("3D → 2D PCA Visualization", -width/2 + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.pc1;
        context.fillText("First Principal Component (PC1)", -width/2 + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.pc2;
        context.fillText("Second Principal Component (PC2)", -width/2 + 20, yPos);
        
        context.restore();
    }

    function draw2Dto1D() {
        const data = generate2DData();
        const pca = calculatePCA(data);

        // Draw original points
        data.forEach(point => {
            context.beginPath();
            context.arc(point.x * scale, point.y * scale, 3, 0, Math.PI * 2);
            context.fillStyle = colors.points;
            context.fill();
        });

        // Draw PC1 (main axis)
        const length = scale * 3;
        context.beginPath();
        context.strokeStyle = colors.pc1;
        context.lineWidth = 2;
        context.moveTo(-pca.pc1.x * length, -pca.pc1.y * length);
        context.lineTo(pca.pc1.x * length, pca.pc1.y * length);
        context.stroke();

        // Draw projections onto PC1
        data.forEach(point => {
            const proj = projectPoint(point, pca.pc1);
            
            // Line to projection
            context.beginPath();
            context.strokeStyle = colors.projection + '40';
            context.moveTo(point.x * scale, point.y * scale);
            context.lineTo(proj.x * scale, proj.y * scale);
            context.stroke();

            // Projection point
            context.beginPath();
            context.arc(proj.x * scale, proj.y * scale, 2, 0, Math.PI * 2);
            context.fillStyle = colors.projection;
            context.fill();
        });

        // Add explanatory text
        context.save();
        context.scale(1, -1);
        context.font = '16px Arial';
        context.fillStyle = colors.text;
        context.textAlign = 'left';
        
        let yPos = -height/2 + 30;
        context.fillText("2D → 1D PCA Visualization", -width/2 + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.pc1;
        context.fillText("Principal Component (PC1)", -width/2 + 20, yPos);
        yPos += 25;
        context.fillStyle = colors.projection;
        context.fillText("Projected Points", -width/2 + 20, yPos);
        
        context.restore();
    }

    function drawVisualization() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);
        
        drawGrid();
        
        if(mode === "3dto2d") {
            draw3Dto2D();
        } else {
            draw2Dto1D();
        }
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(-width/2, -height/2, width, height);

        // Draw 3D elements
        drawGrid3D();
        drawProjectionPlane();
        
        // Draw data points
        const data = generate3DData();
        data.forEach(point => {
            drawPoint3D(point);
        });

        // Draw principal components
        drawPrincipalComponents(data);
        
        // Draw explanation
        drawExplanation();
    }

    function animate() {
        if(isAnimating) {
            rotationAngle = (currentTime * 0.02) % (Math.PI * 2);
            currentTime++;
            draw();
            requestAnimationFrame(animate);
        }
    }

    // Toggle animation
    document.addEventListener('keydown', function(event) {
        if(event.code === 'Space') {
            isAnimating = !isAnimating;
            if(isAnimating) animate();
        }
    });

    animate();
};