window.onload = function() {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = canvas.width = window.innerWidth,
        height = canvas.height = window.innerHeight;

    let isAnimating = true;
    let currentTime = 0;
    let viewMode = "comparison"; // "comparison", "interpolation", "composition"
    
    const colors = {
        axis: "#ffffff",
        object: "#00ff00",
        euler: "#ff0000",
        quaternion: "#0088ff",
        text: "#ffffff",
        grid: "#333333"
    };

    class Quaternion {
        constructor(w, x, y, z) {
            this.w = w;
            this.x = x;
            this.y = y;
            this.z = z;
        }

        // Quaternion multiplication
        multiply(q) {
            return new Quaternion(
                this.w*q.w - this.x*q.x - this.y*q.y - this.z*q.z,
                this.w*q.x + this.x*q.w + this.y*q.z - this.z*q.y,
                this.w*q.y - this.x*q.z + this.y*q.w + this.z*q.x,
                this.w*q.z + this.x*q.y - this.y*q.x + this.z*q.w
            );
        }

        // Create rotation quaternion from axis and angle
        static fromAxisAngle(axis, angle) {
            const halfAngle = angle / 2;
            const s = Math.sin(halfAngle);
            return new Quaternion(
                Math.cos(halfAngle),
                axis.x * s,
                axis.y * s,
                axis.z * s
            );
        }

        // SLERP (Spherical Linear Interpolation)
        static slerp(q1, q2, t) {
            const dot = q1.w*q2.w + q1.x*q2.x + q1.y*q2.y + q1.z*q2.z;
            const theta = Math.acos(dot);
            const sinTheta = Math.sin(theta);
            
            if (sinTheta === 0) return q1;
            
            const w1 = Math.sin((1-t)*theta) / sinTheta;
            const w2 = Math.sin(t*theta) / sinTheta;
            
            return new Quaternion(
                w1*q1.w + w2*q2.w,
                w1*q1.x + w2*q2.x,
                w1*q1.y + w2*q2.y,
                w1*q1.z + w2*q2.z
            );
        }

        // Convert quaternion to rotation matrix
        toMatrix() {
            const {w, x, y, z} = this;
            return [
                [1-2*y*y-2*z*z, 2*x*y-2*w*z, 2*x*z+2*w*y],
                [2*x*y+2*w*z, 1-2*x*x-2*z*z, 2*y*z-2*w*x],
                [2*x*z-2*w*y, 2*y*z+2*w*x, 1-2*x*x-2*y*y]
            ];
        }
    }

    function drawCube(x, y, rotationMatrix, color, scale = 100) {
        // Cube vertices
        const vertices = [
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
        ];

        // Transform vertices
        const transformedVertices = vertices.map(v => {
            const [vx, vy, vz] = v;
            return [
                rotationMatrix[0][0]*vx + rotationMatrix[0][1]*vy + rotationMatrix[0][2]*vz,
                rotationMatrix[1][0]*vx + rotationMatrix[1][1]*vy + rotationMatrix[1][2]*vz,
                rotationMatrix[2][0]*vx + rotationMatrix[2][1]*vy + rotationMatrix[2][2]*vz
            ];
        });

        // Project to 2D
        const projectedVertices = transformedVertices.map(v => ({
            x: x + v[0] * scale,
            y: y + v[1] * scale
        }));

        // Draw edges
        const edges = [
            [0,1], [1,2], [2,3], [3,0],
            [4,5], [5,6], [6,7], [7,4],
            [0,4], [1,5], [2,6], [3,7]
        ];

        context.strokeStyle = color;
        context.lineWidth = 2;
        edges.forEach(([i, j]) => {
            context.beginPath();
            context.moveTo(projectedVertices[i].x, projectedVertices[i].y);
            context.lineTo(projectedVertices[j].x, projectedVertices[j].y);
            context.stroke();
        });
    }

    function drawComparison() {
        const angle = currentTime;
        
        // Euler rotation (prone to gimbal lock)
        const eulerMatrix = [
            [Math.cos(angle), -Math.sin(angle), 0],
            [Math.sin(angle), Math.cos(angle), 0],
            [0, 0, 1]
        ];
        
        // Quaternion rotation
        const quaternion = Quaternion.fromAxisAngle({x: 1/Math.sqrt(3), y: 1/Math.sqrt(3), z: 1/Math.sqrt(3)}, angle);
        const quaternionMatrix = quaternion.toMatrix();

        // Draw both cubes
        drawCube(width/3, height/2, eulerMatrix, colors.euler);
        drawCube(2*width/3, height/2, quaternionMatrix, colors.quaternion);

        // Add labels
        context.fillStyle = colors.text;
        context.font = "20px Arial";
        context.fillText("Euler Rotation", width/3 - 50, height/4);
        context.fillText("Quaternion Rotation", 2*width/3 - 50, height/4);
    }

    function drawInterpolation() {
        // Create two quaternions for interpolation
        const q1 = Quaternion.fromAxisAngle({x: 1, y: 0, z: 0}, 0);
        const q2 = Quaternion.fromAxisAngle({x: 0, y: 1, z: 0}, Math.PI/2);
        
        // Interpolate between them
        const t = (Math.sin(currentTime) + 1) / 2;  // Oscillate between 0 and 1
        const interpolated = Quaternion.slerp(q1, q2, t);
        
        // Draw interpolated rotation
        drawCube(width/2, height/2, interpolated.toMatrix(), colors.quaternion);
        
        // Draw progress bar
        context.fillStyle = colors.text;
        context.fillRect(width/4, height - 50, width/2 * t, 20);
        context.strokeStyle = colors.text;
        context.strokeRect(width/4, height - 50, width/2, 20);
        context.fillText(`Interpolation: ${(t*100).toFixed(0)}%`, width/4, height - 60);
    }

    function drawComposition() {
        // Create two rotations
        const q1 = Quaternion.fromAxisAngle({x: 1, y: 0, z: 0}, currentTime);
        const q2 = Quaternion.fromAxisAngle({x: 0, y: 1, z: 0}, currentTime * 0.5);
        
        // Compose rotations
        const combined = q1.multiply(q2);
        
        // Draw original and composed rotations
        drawCube(width/3, height/2, q1.toMatrix(), colors.euler);
        drawCube(2*width/3, height/2, combined.toMatrix(), colors.quaternion);
        
        context.fillStyle = colors.text;
        context.fillText("Single Rotation", width/3 - 50, height/4);
        context.fillText("Composed Rotations", 2*width/3 - 50, height/4);
    }

    function drawExplanation() {
        context.fillStyle = colors.text;
        context.font = "18px Arial";
        context.textAlign = "left";
        
        let y = 30;
        context.fillText("4원수 (Quaternion) 시각화", 20, y);
        
        y += 30;
        context.font = "16px Arial";
        context.fillText("q = w + xi + yj + zk", 20, y);
        y += 25;
        context.fillText("i² = j² = k² = ijk = -1", 20, y);
        
        y += 40;
        context.fillText("Controls:", 20, y);
        y += 25;
        const ctrlKey = navigator.platform.includes('Mac') ? '⌘' : 'Ctrl';
        context.fillText(`${ctrlKey} + 1: 회전 비교`, 40, y);
        y += 25;
        context.fillText(`${ctrlKey} + 2: 회전 보간`, 40, y);
        y += 25;
        context.fillText(`${ctrlKey} + 3: 회전 합성`, 40, y);
        y += 25;
        context.fillText("Space: Pause/Resume", 40, y);
    }

    function draw() {
        // Clear canvas
        context.fillStyle = 'black';
        context.fillRect(0, 0, width, height);

        // Draw current visualization mode
        switch(viewMode) {
            case "comparison":
                drawComparison();
                break;
            case "interpolation":
                drawInterpolation();
                break;
            case "composition":
                drawComposition();
                break;
        }

        drawExplanation();
    }

    function animate() {
        if (isAnimating) {
            currentTime += 0.02;
            draw();
            requestAnimationFrame(animate);
        }
    }

    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey || event.metaKey) {
            switch(event.key) {
                case '1':
                    viewMode = "comparison";
                    break;
                case '2':
                    viewMode = "interpolation";
                    break;
                case '3':
                    viewMode = "composition";
                    break;
            }
        } else if (event.code === 'Space') {
            isAnimating = !isAnimating;
            if(isAnimating) animate();
        }
    });

    animate();
};