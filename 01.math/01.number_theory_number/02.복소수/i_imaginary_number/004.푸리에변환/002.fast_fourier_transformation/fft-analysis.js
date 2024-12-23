window.onload = function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Audio context setup
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    const mainGainNode = audioContext.createGain();  // Main volume control
    mainGainNode.gain.value = 0.1;  // Lower overall volume
    analyser.fftSize = 2048;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    // Connect analyser to audio output
    analyser.connect(mainGainNode);
    mainGainNode.connect(audioContext.destination);  // Connect to speakers

    const width = canvas.width;
    const height = canvas.height;
    let isAnimating = true;

    // Create oscillators with audio frequencies
    const oscillators = [
        { freq: 440, type: 'sine', gain: 0.5, active: false, name: 'A4 (440Hz)' },
        { freq: 523.25, type: 'sine', gain: 0.5, active: false, name: 'C5 (523Hz)' },
        { freq: 659.25, type: 'sine', gain: 0.5, active: false, name: 'E5 (659Hz)' }
    ];

    const oscNodes = oscillators.map(osc => {
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.type = osc.type;
        oscillator.frequency.setValueAtTime(osc.freq, audioContext.currentTime);
        gainNode.gain.setValueAtTime(0, audioContext.currentTime);
        
        oscillator.connect(gainNode);
        gainNode.connect(analyser);
        
        oscillator.start();
        return { oscillator, gainNode };
    });

    function createControls() {
        const controlPanel = document.createElement('div');
        controlPanel.style.position = 'absolute';
        controlPanel.style.top = '20px';
        controlPanel.style.left = '20px';
        controlPanel.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
        controlPanel.style.padding = '10px';
        controlPanel.style.borderRadius = '5px';
        
        oscillators.forEach((osc, i) => {
            const button = document.createElement('button');
            button.textContent = osc.name;
            button.style.backgroundColor = `hsl(${i * 120}, 70%, 50%)`;
            button.style.margin = '5px';
            button.style.padding = '5px 10px';
            button.style.border = '2px solid white';
            button.style.borderRadius = '3px';
            button.style.color = 'white';
            button.style.cursor = 'pointer';
            button.style.opacity = '0.5';
            
            button.onclick = () => {
                osc.active = !osc.active;
                button.style.opacity = osc.active ? '1' : '0.5';
                
                oscNodes[i].gainNode.gain.setValueAtTime(
                    osc.active ? osc.gain : 0,
                    audioContext.currentTime
                );
            };

            controlPanel.appendChild(button);
        });

        // Add volume slider
        const volumeControl = document.createElement('input');
        volumeControl.type = 'range';
        volumeControl.min = 0;
        volumeControl.max = 100;
        volumeControl.value = 10;
        volumeControl.style.width = '100%';
        volumeControl.style.margin = '10px 5px';
        
        volumeControl.oninput = (e) => {
            mainGainNode.gain.value = e.target.value / 100;
        };

        const volumeLabel = document.createElement('div');
        volumeLabel.textContent = 'Volume';
        volumeLabel.style.color = 'white';
        volumeLabel.style.marginLeft = '5px';

        controlPanel.appendChild(volumeLabel);
        controlPanel.appendChild(volumeControl);

        document.body.appendChild(controlPanel);
    }

    function drawAxes() {
        ctx.strokeStyle = '#666';
        ctx.lineWidth = 2;
        ctx.font = '12px Arial';
        ctx.fillStyle = '#666';

        // Y axis
        ctx.beginPath();
        ctx.moveTo(50, 0);
        ctx.lineTo(50, height);
        ctx.stroke();

        // X axis
        ctx.beginPath();
        ctx.moveTo(50, height - 50);
        ctx.lineTo(width, height - 50);
        ctx.stroke();

        // Y axis labels (amplitude)
        for(let i = 0; i <= 10; i++) {
            const y = height - 50 - (i * (height - 100) / 10);
            ctx.fillText(i * 10 + '%', 10, y);
        }

        // X axis labels (frequency) - adjusted to show relevant frequency range
        const maxFreq = 1000;  // Show up to 1000 Hz
        for(let i = 0; i <= 10; i++) {
            const x = 50 + i * (width - 100) / 10;
            ctx.fillText(i * (maxFreq/10) + 'Hz', x, height - 20);
        }
    }

    function drawFFT() {
        analyser.getByteFrequencyData(dataArray);

        ctx.fillStyle = '#000';
        ctx.fillRect(0, 0, width, height);

        drawAxes();

        // Draw frequency data
        const maxFreq = 1000;  // Show up to 1000 Hz
        const maxBin = Math.floor(maxFreq * analyser.fftSize / audioContext.sampleRate);
        const binWidth = (width - 100) / maxBin;

        ctx.beginPath();
        ctx.strokeStyle = '#0F0';
        ctx.lineWidth = 2;

        for(let i = 0; i < maxBin; i++) {
            const x = 50 + i * binWidth;
            const barHeight = (dataArray[i] / 255) * (height - 100);
            
            if(i === 0) {
                ctx.moveTo(x, height - 50 - barHeight);
            } else {
                ctx.lineTo(x, height - 50 - barHeight);
            }

            // Mark significant peaks and their frequencies
            if(i > 0 && i < maxBin - 1) {
                if(dataArray[i] > dataArray[i-1] && 
                   dataArray[i] > dataArray[i+1] && 
                   dataArray[i] > 100) {
                    const freq = i * audioContext.sampleRate / analyser.fftSize;
                    ctx.fillStyle = '#F00';
                    ctx.fillRect(x - 2, height - 50 - barHeight - 2, 4, 4);
                    ctx.fillText(Math.round(freq) + 'Hz', x, height - 50 - barHeight - 10);
                }
            }
        }
        ctx.stroke();

        // Draw active frequencies markers
        oscillators.forEach((osc, index) => {
            if(osc.active) {
                const freqBin = Math.floor(osc.freq * analyser.fftSize / audioContext.sampleRate);
                const x = 50 + freqBin * binWidth;
                ctx.fillStyle = `hsl(${index * 120}, 70%, 50%)`;
                ctx.fillRect(x - 2, height - 50, 4, -20);
                ctx.fillText(osc.freq + 'Hz', x, height - 80);
            }
        });
    }

    function animate() {
        if (isAnimating) {
            drawFFT();
            requestAnimationFrame(animate);
        }
    }

    document.addEventListener('keydown', (event) => {
        if (event.code === 'Space') {
            event.preventDefault();
            isAnimating = !isAnimating;
            if (isAnimating) animate();
        }
    });

    createControls();
    animate();

    // Initialize audio context on user interaction
    document.addEventListener('click', () => {
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }
    }, { once: true });
};