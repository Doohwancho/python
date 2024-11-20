window.onload = function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Constants for visualization
    const width = canvas.width;
    const height = canvas.height;
    const centerY = height / 2;
    const scale = 100;
    const gridSize = 50;
    
    // Time variables
    let time = 0;
    let isAnimating = true;
    
    // Fourier components with visibility toggle
    const components = [
        { freq: 1, amp: 1.0, phase: 0, visible: true, color: '#FF0000', name: "Base Wave" },
        { freq: 2, amp: 0.5, phase: Math.PI/4, visible: true, color: '#00FF00', name: "2nd Harmonic" },
        { freq: 3, amp: 0.3, phase: Math.PI/3, visible: true, color: '#0000FF', name: "3rd Harmonic" },
        { freq: 4, amp: 0.2, phase: Math.PI/6, visible: true, color: '#FFFF00', name: "4th Harmonic" }
    ];

    // Create control buttons
    function createControls() {
        const controlPanel = document.createElement('div');
        controlPanel.style.position = 'absolute';
        controlPanel.style.top = '20px';
        controlPanel.style.left = '20px';
        controlPanel.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        controlPanel.style.padding = '10px';
        controlPanel.style.borderRadius = '5px';

        components.forEach((comp, i) => {
            const button = document.createElement('button');
            button.textContent = comp.name;
            button.style.backgroundColor = comp.color;
            button.style.margin = '5px';
            button.style.padding = '5px 10px';
            button.style.border = '2px solid white';
            button.style.borderRadius = '3px';
            button.style.cursor = 'pointer';
            
            if(comp.visible) {
                button.style.opacity = '1';
            } else {
                button.style.opacity = '0.5';
            }

            button.onclick = () => {
                comp.visible = !comp.visible;
                button.style.opacity = comp.visible ? '1' : '0.5';
            };

            controlPanel.appendChild(button);
        });

        document.body.appendChild(controlPanel);
    }

    function drawGrid() {
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 0.5;

        // Vertical grid lines
        for(let x = 0; x < width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }

        // Horizontal grid lines
        for(let y = 0; y < height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
    }

    function drawAxes() {
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;

        // Y axis
        ctx.beginPath();
        ctx.moveTo(width/2, 0);
        ctx.lineTo(width/2, height);
        ctx.stroke();

        // X axis
        ctx.beginPath();
        ctx.moveTo(0, centerY);
        ctx.lineTo(width, centerY);
        ctx.stroke();

        // Draw axis labels
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';
        
        // Y axis labels
        for(let y = -5; y <= 5; y++) {
            const yPos = centerY - y * scale/2;
            ctx.fillText(y/2, width/2 + 5, yPos);
            ctx.beginPath();
            ctx.moveTo(width/2 - 5, yPos);
            ctx.lineTo(width/2 + 5, yPos);
            ctx.stroke();
        }

        // X axis labels
        for(let x = -10; x <= 10; x++) {
            const xPos = width/2 + x * scale;
            ctx.fillText(x + 'π', xPos, centerY + 15);
            ctx.beginPath();
            ctx.moveTo(xPos, centerY - 5);
            ctx.lineTo(xPos, centerY + 5);
            ctx.stroke();
        }
    }

    function drawWave(component) {
        ctx.beginPath();
        ctx.strokeStyle = component.color;
        ctx.lineWidth = 2;
        
        for(let x = 0; x < width; x++) {
            const t = (x - width/2) * 0.02 + time;
            const y = Math.sin(t * component.freq + component.phase) * component.amp;
            
            if(x === 0) {
                ctx.moveTo(x, centerY + y * scale);
            } else {
                ctx.lineTo(x, centerY + y * scale);
            }
        }
        ctx.stroke();
    }

    function drawCombinedWave() {
        ctx.beginPath();
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 2;

        for(let x = 0; x < width; x++) {
            let y = 0;
            const t = (x - width/2) * 0.02 + time;
            
            // Sum only visible components
            components.forEach(comp => {
                if(comp.visible) {
                    y += Math.sin(t * comp.freq + comp.phase) * comp.amp;
                }
            });
            
            if(x === 0) {
                ctx.moveTo(x, centerY + y * scale);
            } else {
                ctx.lineTo(x, centerY + y * scale);
            }
        }
        ctx.stroke();
    }

    function calculateFFT(signal) {
        // Simple FFT calculation - compute magnitude at each frequency
        const frequencies = components.map(comp => comp.freq);
        const maxFreq = Math.max(...frequencies) + 1;
        const fftData = new Array(maxFreq * 2).fill(0);
        
        // For each frequency, calculate its contribution in the signal
        components.forEach(comp => {
            if (comp.visible) {
                fftData[comp.freq] = comp.amp;
            }
        });
        
        return fftData;
    }

    function drawFFT(fftData) {
        const fftHeight = height * 0.3; // Height for FFT visualization
        const barWidth = width / (fftData.length * 2);
        const fftY = height - fftHeight - 20; // Position below waves
        
        // Draw FFT background
        ctx.fillStyle = '#111';
        ctx.fillRect(0, fftY, width, fftHeight);
        
        // Draw FFT grid
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 0.5;
        
        // Horizontal grid lines
        for(let y = 0; y <= fftHeight; y += fftHeight/5) {
            ctx.beginPath();
            ctx.moveTo(0, fftY + y);
            ctx.lineTo(width, fftY + y);
            ctx.stroke();
        }
        
        // Vertical grid lines
        for(let x = 0; x < width; x += width/10) {
            ctx.beginPath();
            ctx.moveTo(x, fftY);
            ctx.lineTo(x, fftY + fftHeight);
            ctx.stroke();
        }
    
        // Draw FFT bars
        fftData.forEach((magnitude, i) => {
            if(magnitude > 0) {
                const barHeight = magnitude * fftHeight;
                const x = width/2 + i * barWidth * 4; // Spread out bars for visibility
                
                // Draw frequency bar
                ctx.fillStyle = `hsl(${i * 360/components.length}, 100%, 50%)`;
                ctx.fillRect(x - barWidth/2, fftY + fftHeight - barHeight, barWidth, barHeight);
                
                // Add frequency label
                ctx.fillStyle = '#fff';
                ctx.font = '12px Arial';
                ctx.textAlign = 'center';
                ctx.fillText(`f${i}`, x, fftY + fftHeight + 15);
                ctx.fillText(`${magnitude.toFixed(2)}`, x, fftY + fftHeight - barHeight - 5);
            }
        });
    
        // Add FFT labels
        ctx.fillStyle = '#fff';
        ctx.font = '14px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('Frequency Spectrum', 10, fftY + 20);
        ctx.fillText('Amplitude', 10, fftY + 40);
    }


    function draw() {
        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, width, height);
        
        drawGrid();
        drawAxes();

        // Draw visible individual components
        components.forEach(comp => {
            if(comp.visible) {
                drawWave(comp);
            }
        });
        
        // Draw combined wave
        drawCombinedWave();

        // Calculate and draw FFT
        const fftData = calculateFFT();
        drawFFT(fftData);

        // Animation control text
        ctx.fillStyle = '#fff';
        ctx.font = '14px Arial';
        ctx.fillText(
            isAnimating ? 'Press SPACE to pause' : 'Press SPACE to resume',
            20, 
            height - 20
        );
    }

    function animate() {
        if (isAnimating) {
            time += 0.02;
            draw();
            requestAnimationFrame(animate);
        }
    }

    // Keyboard controls
    document.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            event.preventDefault();
            isAnimating = !isAnimating;
            if (isAnimating) animate();
        }
    });

    // Initialize controls and start animation
    createControls();
    animate();
};