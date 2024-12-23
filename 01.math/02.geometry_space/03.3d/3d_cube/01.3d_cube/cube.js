window.onload = function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const width = canvas.width;
    const height = canvas.height;

    ctx.translate(width/2, height/2);

    // Camera settings
    const camera = {
        position: { x: 0, y: 0, z: -400 },  // Camera position
        rotation: { x: 0, y: 0, z: 0 },     // Camera rotation
        distance: 400                        // Camera distance from origin
    };

    let isDragging = false;
    let previousMousePosition = { x: 0, y: 0 };

    const cubeSize = 100;
    let isAnimating = true;
    let animationId = null;

    // Define vertices
    const vertices = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ].map(vertex => vertex.map(coord => coord * cubeSize));

    const edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ];

    // 3D Matrix transformations
    function rotatePoint(point, rotation) {
        let [x, y, z] = point;

        // Rotate around X axis
        let temp = y;
        y = y * Math.cos(rotation.x) - z * Math.sin(rotation.x);
        z = temp * Math.sin(rotation.x) + z * Math.cos(rotation.x);

        // Rotate around Y axis
        temp = x;
        x = x * Math.cos(rotation.y) + z * Math.sin(rotation.y);
        z = -temp * Math.sin(rotation.y) + z * Math.cos(rotation.y);

        // Rotate around Z axis
        temp = x;
        x = x * Math.cos(rotation.z) - y * Math.sin(rotation.z);
        y = temp * Math.sin(rotation.z) + y * Math.cos(rotation.z);

        return [x, y, z];
    }

    function projectPoint(point) {
        let [x, y, z] = point;
        
        // Apply camera rotation
        [x, y, z] = rotatePoint([x, y, z], camera.rotation);
        
        // Apply perspective projection
        z += camera.distance;
        if (z <= 0) z = 0.1; // Prevent division by zero
        
        const scale = camera.distance / z;
        return [x * scale, y * scale];
    }

    function drawAxes() {
        const axisLength = cubeSize * 2;
        
        // Transform axis endpoints
        const origin = projectPoint([0, 0, 0]);
        const xEnd = projectPoint([axisLength, 0, 0]);
        const yEnd = projectPoint([0, axisLength, 0]);
        const zEnd = projectPoint([0, 0, axisLength]);

        // Draw X axis (red)
        ctx.beginPath();
        ctx.strokeStyle = '#ff0000';
        ctx.moveTo(origin[0], origin[1]);
        ctx.lineTo(xEnd[0], xEnd[1]);
        ctx.stroke();
        ctx.fillStyle = '#ff0000';
        ctx.fillText('X', xEnd[0], xEnd[1]);

        // Draw Y axis (green)
        ctx.beginPath();
        ctx.strokeStyle = '#00ff00';
        ctx.moveTo(origin[0], origin[1]);
        ctx.lineTo(yEnd[0], yEnd[1]);
        ctx.stroke();
        ctx.fillStyle = '#00ff00';
        ctx.fillText('Y', yEnd[0], yEnd[1]);

        // Draw Z axis (blue)
        ctx.beginPath();
        ctx.strokeStyle = '#0000ff';
        ctx.moveTo(origin[0], origin[1]);
        ctx.lineTo(zEnd[0], zEnd[1]);
        ctx.stroke();
        ctx.fillStyle = '#0000ff';
        ctx.fillText('Z', zEnd[0], zEnd[1]);
    }

    function drawCube() {
        ctx.fillStyle = '#000000';
        ctx.fillRect(-width/2, -height/2, width, height);

        drawAxes();

        // Project vertices
        const projectedVertices = vertices.map(vertex => projectPoint(vertex));

        // Draw edges
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        edges.forEach(([i, j]) => {
            ctx.beginPath();
            ctx.moveTo(projectedVertices[i][0], projectedVertices[i][1]);
            ctx.lineTo(projectedVertices[j][0], projectedVertices[j][1]);
            ctx.stroke();
        });

        // Draw vertices
        ctx.fillStyle = '#ffff00';
        projectedVertices.forEach(([x, y]) => {
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, Math.PI * 2);
            ctx.fill();
        });

        // Display camera angles
        ctx.fillStyle = '#ffffff';
        ctx.font = '14px Arial';
        const angles = {
            x: (camera.rotation.x * 180 / Math.PI) % 360,
            y: (camera.rotation.y * 180 / Math.PI) % 360,
            z: (camera.rotation.z * 180 / Math.PI) % 360
        };
        ctx.fillText(`Camera angles: X: ${angles.x.toFixed(0)}° Y: ${angles.y.toFixed(0)}° Z: ${angles.z.toFixed(0)}°`, 
                    -width/2 + 20, -height/2 + 30);
    }

    // Mouse controls
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        previousMousePosition = {
            x: e.clientX,
            y: e.clientY
        };
    });

    canvas.addEventListener('mousemove', (e) => {
        if (!isDragging) return;

        const deltaMove = {
            x: e.clientX - previousMousePosition.x,
            y: e.clientY - previousMousePosition.y
        };

        // Update camera rotation based on mouse movement
        camera.rotation.y += deltaMove.x * 0.005;
        camera.rotation.x += deltaMove.y * 0.005;

        previousMousePosition = {
            x: e.clientX,
            y: e.clientY
        };

        drawCube();
    });

    canvas.addEventListener('mouseup', () => {
        isDragging = false;
    });

    // Zoom control
    canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        camera.distance += e.deltaY;
        camera.distance = Math.max(200, Math.min(800, camera.distance));
        drawCube();
    });

    // Create camera control panel
    function createControls() {
        const controlPanel = document.createElement('div');
        controlPanel.style.position = 'absolute';
        controlPanel.style.top = '20px';
        controlPanel.style.right = '20px';
        controlPanel.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        controlPanel.style.padding = '10px';
        controlPanel.style.borderRadius = '5px';
        controlPanel.style.color = 'white';

        // Rotation controls
        ['X', 'Y', 'Z'].forEach(axis => {
            const container = document.createElement('div');
            container.style.marginBottom = '10px';

            const label = document.createElement('div');
            label.textContent = `Camera ${axis} Rotation`;
            label.style.marginBottom = '5px';
            container.appendChild(label);

            const slider = document.createElement('input');
            slider.type = 'range';
            slider.min = '0';
            slider.max = '360';
            slider.value = '0';
            slider.style.width = '200px';
            slider.oninput = (e) => {
                camera.rotation[axis.toLowerCase()] = e.target.value * Math.PI / 180;
                drawCube();
            };
            container.appendChild(slider);

            controlPanel.appendChild(container);
        });

        // Distance control
        const distanceContainer = document.createElement('div');
        const distanceLabel = document.createElement('div');
        distanceLabel.textContent = 'Camera Distance';
        distanceContainer.appendChild(distanceLabel);

        const distanceSlider = document.createElement('input');
        distanceSlider.type = 'range';
        distanceSlider.min = '200';
        distanceSlider.max = '800';
        distanceSlider.value = camera.distance.toString();
        distanceSlider.style.width = '200px';
        distanceSlider.oninput = (e) => {
            camera.distance = parseInt(e.target.value);
            drawCube();
        };
        distanceContainer.appendChild(distanceSlider);
        controlPanel.appendChild(distanceContainer);

        document.body.appendChild(controlPanel);
    }

    // Instructions
    function addInstructions() {
        const instructions = document.createElement('div');
        instructions.style.position = 'absolute';
        instructions.style.bottom = '20px';
        instructions.style.left = '20px';
        instructions.style.color = 'white';
        instructions.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        instructions.style.padding = '10px';
        instructions.style.borderRadius = '5px';
        instructions.innerHTML = `
            Mouse Controls:<br>
            • Drag to rotate view<br>
            • Scroll to zoom in/out
        `;
        document.body.appendChild(instructions);
    }

    createControls();
    addInstructions();
    drawCube();
};