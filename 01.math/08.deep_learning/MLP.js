window.onload = function() {
    const canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        width = canvas.width = window.innerWidth,
        height = canvas.height = window.innerHeight;

    let currentMode = "mlp";  // mlp, perceptron, loss, activation, matrix, binary, backprop

    let isAnimating = true;
    let currentTime = 0;

    // const colors = {
    //     neuron: "#00ff00",        // Green for neurons
    //     connection: "#ffffff",     // White for connections
    //     activation: "#ff0000",     // Red for activation
    //     error: "#ff00ff",         // Magenta for error/loss
    //     gradient: "#0088ff",      // Blue for gradients
    //     text: "#ffffff",
    //     highlight: "#ffff00",     // Yellow for highlights
    //     background: "#000000"
    // };
    const colors = {
        neuron: "#00ff00",        // Green for neurons
        connection: "#ffffff",     // White for connections
        class1: "#ff4444",        // Bright red for class 1
        class2: "#4444ff",        // Bright blue for class 2
        gradient: "#00ffff",      // Cyan for gradients
        text: "#ffffff",          // White for text
        highlight: "#ffff00",     // Yellow for highlights
        background: "#000000",    // Black background
        positive: "#ff4444",      // Bright red for positive gradients
        negative: "#4444ff"       // Bright blue for negative gradients
    };

    // MLP structure definition
    const network = {
        layers: [
            {size: 3, nodes: []},  // Input layer
            {size: 4, nodes: []},  // Hidden layer
            {size: 2, nodes: []}   // Output layer
        ],
        weights: [],
        activations: []
    };

    // Initialize network
    function initializeNetwork() {
        // Initialize node positions
        network.layers.forEach((layer, i) => {
            const layerX = width * (i + 1)/(network.layers.length + 1);
            layer.nodes = [];
            
            for(let j = 0; j < layer.size; j++) {
                const nodeY = height * (j + 1)/(layer.size + 1);
                layer.nodes.push({
                    x: layerX,
                    y: nodeY,
                    activation: 0,
                    error: 0
                });
            }
        });

        // Initialize weights randomly
        network.weights = [];
        for(let i = 0; i < network.layers.length - 1; i++) {
            const layerWeights = [];
            for(let j = 0; j < network.layers[i].size; j++) {
                const nodeWeights = [];
                for(let k = 0; k < network.layers[i + 1].size; k++) {
                    nodeWeights.push(Math.random() * 2 - 1);
                }
                layerWeights.push(nodeWeights);
            }
            network.weights.push(layerWeights);
        }
    }

    function drawNetwork(highlightFeature = null) {
        // Draw connections first
        for(let i = 0; i < network.layers.length - 1; i++) {
            const currentLayer = network.layers[i];
            const nextLayer = network.layers[i + 1];
            
            currentLayer.nodes.forEach((node, j) => {
                nextLayer.nodes.forEach((nextNode, k) => {
                    const weight = network.weights[i][j][k];
                    const alpha = Math.abs(weight);
                    
                    context.beginPath();
                    context.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
                    context.lineWidth = Math.abs(weight) * 3;
                    context.moveTo(node.x, node.y);
                    context.lineTo(nextNode.x, nextNode.y);
                    context.stroke();
                });
            });
        }

        // Draw nodes
        network.layers.forEach((layer, i) => {
            layer.nodes.forEach((node, j) => {
                context.beginPath();
                context.arc(node.x, node.y, 20, 0, Math.PI * 2);
                
                // Color based on activation
                const activation = Math.sin(currentTime + i + j) * 0.5 + 0.5;
                context.fillStyle = `rgb(0, ${Math.floor(activation * 255)}, 0)`;
                context.fill();
                
                context.strokeStyle = colors.neuron;
                context.lineWidth = 2;
                context.stroke();

                // Add activation value
                context.fillStyle = colors.text;
                context.font = "12px Arial";
                context.textAlign = "center";
                context.fillText(activation.toFixed(2), node.x, node.y);
            });
        });

        // Draw layer labels
        context.font = "16px Arial";
        context.fillStyle = colors.text;
        context.textAlign = "center";
        context.fillText("Input Layer", network.layers[0].nodes[0].x, 30);
        context.fillText("Hidden Layer", network.layers[1].nodes[0].x, 30);
        context.fillText("Output Layer", network.layers[2].nodes[0].x, 30);
    }

    function drawPerceptron() {
        // Draw single perceptron with inputs
        const centerX = width/2;
        const centerY = height/2;
        
        // Draw inputs
        const inputs = [-1, 0, 1];
        const weights = [0.5, -0.8, 0.3];
        
        inputs.forEach((input, i) => {
            const x = centerX - 200;
            const y = centerY + (i - 1) * 80;
            
            // Draw input node
            context.beginPath();
            context.arc(x, y, 20, 0, Math.PI * 2);
            context.fillStyle = colors.neuron;
            context.fill();
            context.stroke();
            
            // Draw connection
            context.beginPath();
            context.strokeStyle = `rgba(255, 255, 255, ${Math.abs(weights[i])})`;
            context.lineWidth = Math.abs(weights[i]) * 5;
            context.moveTo(x + 20, y);
            context.lineTo(centerX - 20, centerY);
            context.stroke();
            
            // Label input
            context.fillStyle = colors.text;
            context.font = "16px Arial";
            context.textAlign = "center";
            context.fillText(`x${i+1}: ${input}`, x, y - 30);
            context.fillText(`w${i+1}: ${weights[i]}`, (x + centerX)/2, y - 10);
        });

        // Draw perceptron
        context.beginPath();
        context.arc(centerX, centerY, 30, 0, Math.PI * 2);
        context.fillStyle = colors.neuron;
        context.fill();
        context.stroke();

        // Calculate and show activation
        const sum = inputs.reduce((acc, curr, i) => acc + curr * weights[i], 0);
        const activation = 1 / (1 + Math.exp(-sum));  // Sigmoid

        // Show calculation steps
        context.fillStyle = colors.text;
        context.textAlign = "left";
        context.font = "16px Arial";
        
        let textY = height/4;
        context.fillText("Perceptron Calculation:", width * 0.7, textY);
        textY += 30;
        context.fillText(`Weighted sum = ${sum.toFixed(3)}`, width * 0.7, textY);
        textY += 30;
        context.fillText(`Activation = σ(sum) = ${activation.toFixed(3)}`, width * 0.7, textY);

        // Draw output
        const outputX = centerX + 200;
        context.beginPath();
        context.strokeStyle = colors.connection;
        context.lineWidth = 2;
        context.moveTo(centerX + 30, centerY);
        context.lineTo(outputX, centerY);
        context.stroke();

        context.beginPath();
        context.arc(outputX, centerY, 20, 0, Math.PI * 2);
        context.fillStyle = `rgb(0, ${Math.floor(activation * 255)}, 0)`;
        context.fill();
        context.stroke();

        context.fillStyle = colors.text;
        context.fillText(activation.toFixed(3), outputX, centerY - 40);
    }

    function drawLossFunction() {
        // Draw loss landscape
        const centerX = width/2;
        const centerY = height/2;
        
        context.beginPath();
        context.strokeStyle = colors.gradient;
        context.lineWidth = 2;

        // Draw parabolic loss function
        for(let x = -width/4; x <= width/4; x++) {
            const xVal = x / 100;
            const yVal = xVal * xVal;  // Simple quadratic loss
            const screenY = centerY - yVal * 100;
            
            if(x === -width/4) {
                context.moveTo(centerX + x, screenY);
            } else {
                context.lineTo(centerX + x, screenY);
            }
        }
        context.stroke();

        // Draw current point on loss curve
        const currentX = Math.sin(currentTime) * width/4;
        const currentLoss = Math.pow(currentX/100, 2);
        const pointY = centerY - currentLoss * 100;

        // Draw current point
        context.beginPath();
        context.arc(centerX + currentX, pointY, 8, 0, Math.PI * 2);
        context.fillStyle = colors.highlight;
        context.fill();
        context.strokeStyle = colors.text;
        context.stroke();

        // Draw gradient vector - make it clearer
        const gradientX = 2 * (currentX/100);  // Derivative of x^2
        const arrowLength = 50;
        
        // Draw gradient arrow
        const gradientColor = gradientX > 0 ? colors.positive : colors.negative;
        context.beginPath();
        context.strokeStyle = gradientColor;
        context.lineWidth = 3;
        context.moveTo(centerX + currentX, pointY);
        context.lineTo(centerX + currentX - gradientX * arrowLength, pointY);
        
        // Add arrowhead
        const headLength = 10;
        const angle = gradientX > 0 ? Math.PI : 0;
        context.lineTo(
            centerX + currentX - gradientX * arrowLength + headLength * Math.cos(angle ± Math.PI/6),
            pointY + headLength * Math.sin(angle ± Math.PI/6)
        );
        context.stroke();

        // Add explanatory text with better visibility
        context.fillStyle = colors.text;  // Make sure text is white
        context.font = "18px Arial";      // Slightly larger font
        context.textAlign = "left";
        
        let textY = height/4;
        let textX = 50;
        // Add text background for better readability
        const textLines = [
            "Loss Function Visualization:",
            `Current Loss = ${currentLoss.toFixed(3)}`,
            `Gradient = ${gradientX.toFixed(3)}`,
            "Arrow shows direction of steepest descent",
            "Red arrow = positive gradient",
            "Blue arrow = negative gradient"
        ];

        // Draw semi-transparent background for text
        context.fillStyle = "rgba(0, 0, 0, 0.7)";
        context.fillRect(
            textX - 10, 
            textY - 30, 
            300, 
            textLines.length * 30 + 20
        );

        // Draw text
        context.fillStyle = colors.text;
        textLines.forEach(line => {
            context.fillText(line, textX, textY);
            textY += 30;
        });
    }

    function drawActivationFunction() {
        const functions = {
            sigmoid: x => 1 / (1 + Math.exp(-x)),
            tanh: x => Math.tanh(x),
            relu: x => Math.max(0, x)
        };

        const colors = {
            sigmoid: "#ff0000",
            tanh: "#00ff00",
            relu: "#0088ff"
        };

        // Draw axes
        const centerX = width/2;
        const centerY = height/2;
        const scale = 100;

        context.strokeStyle = colors.text;
        context.lineWidth = 1;
        
        // X-axis
        context.beginPath();
        context.moveTo(centerX - width/3, centerY);
        context.lineTo(centerX + width/3, centerY);
        context.stroke();
        
        // Y-axis
        context.beginPath();
        context.moveTo(centerX, centerY - height/3);
        context.lineTo(centerX, centerY + height/3);
        context.stroke();

        // Draw activation functions
        Object.entries(functions).forEach(([name, func], index) => {
            context.beginPath();
            context.strokeStyle = colors[name];
            context.lineWidth = 2;

            for(let x = -5; x <= 5; x += 0.1) {
                const y = func(x);
                const screenX = centerX + x * scale;
                const screenY = centerY - y * scale;

                if(x === -5) {
                    context.moveTo(screenX, screenY);
                } else {
                    context.lineTo(screenX, screenY);
                }
            }
            context.stroke();

            // Add label
            context.fillStyle = colors[name];
            context.font = "16px Arial";
            context.textAlign = "left";
            context.fillText(name, centerX + width/4, centerY - 100 + index * 30);
        });

        // Show animation point
        const x = Math.sin(currentTime) * 3;
        Object.entries(functions).forEach(([name, func]) => {
            const y = func(x);
            const screenX = centerX + x * scale;
            const screenY = centerY - y * scale;

            context.beginPath();
            context.arc(screenX, screenY, 5, 0, Math.PI * 2);
            context.fillStyle = colors[name];
            context.fill();
        });

        // Add explanatory text
        context.fillStyle = colors.text;
        context.font = "16px Arial";
        context.textAlign = "left";
        context.fillText(`Input: ${x.toFixed(2)}`, 50, height/4);
        Object.entries(functions).forEach(([name, func], index) => {
            context.fillStyle = colors[name];
            context.fillText(
                `${name}(x) = ${func(x).toFixed(3)}`, 
                50, 
                height/4 + 30 * (index + 1)
            );
        });
    }

    function drawMatrixTransformation() {
        const centerX = width/2;
        const centerY = height/2;
        
        // Example input
        const input = [0.5, -0.3, 0.8];
        const weights = [
            [0.1, 0.2, -0.1],
            [-0.2, 0.3, 0.2],
            [0.3, -0.2, 0.1]
        ];
    
        // Draw input vector as column matrix
        function drawMatrix(matrix, x, y, label) {
            const cellHeight = 40;
            const cellWidth = 60;
            const matrixHeight = matrix.length * cellHeight;
            
            // Draw brackets
            context.strokeStyle = colors.text;
            context.lineWidth = 2;
            
            // Left bracket
            context.beginPath();
            context.moveTo(x + 10, y);
            context.lineTo(x, y);
            context.lineTo(x, y + matrixHeight);
            context.lineTo(x + 10, y + matrixHeight);
            context.stroke();
    
            // Right bracket
            context.beginPath();
            context.moveTo(x + cellWidth - 10, y);
            context.lineTo(x + cellWidth, y);
            context.lineTo(x + cellWidth, y + matrixHeight);
            context.lineTo(x + cellWidth - 10, y + matrixHeight);
            context.stroke();
    
            // Draw values
            context.font = "16px Arial";
            context.fillStyle = colors.text;
            context.textAlign = "center";
            
            if(Array.isArray(matrix[0])) {
                // 2D matrix
                for(let i = 0; i < matrix.length; i++) {
                    for(let j = 0; j < matrix[i].length; j++) {
                        context.fillText(
                            matrix[i][j].toFixed(2),
                            x + j * cellWidth + cellWidth/2,
                            y + i * cellHeight + cellHeight/2
                        );
                    }
                }
            } else {
                // 1D vector
                for(let i = 0; i < matrix.length; i++) {
                    context.fillText(
                        matrix[i].toFixed(2),
                        x + cellWidth/2,
                        y + i * cellHeight + cellHeight/2
                    );
                }
            }
    
            // Draw label
            context.fillText(label, x + cellWidth/2, y - 20);
        }
    
        // Draw matrices
        drawMatrix(input, centerX - 300, centerY - 100, "Input");
        drawMatrix(weights, centerX - 100, centerY - 100, "Weights");
    
        // Draw multiplication animation
        const t = (Math.sin(currentTime) + 1) / 2;
        const result = new Array(3).fill(0);
        
        for(let i = 0; i < 3; i++) {
            for(let j = 0; j < 3; j++) {
                result[i] += input[j] * weights[i][j] * (j < t * 3 ? 1 : 0);
            }
        }
    
        drawMatrix(result, centerX + 200, centerY - 100, "Output");
    
        // Draw animation lines
        const highlightIndex = Math.floor(t * 3);
        if(highlightIndex < 3) {
            context.strokeStyle = colors.highlight;
            context.setLineDash([5, 5]);
            context.beginPath();
            context.moveTo(centerX - 270, centerY - 80 + highlightIndex * 40);
            context.lineTo(centerX - 70, centerY - 80 + highlightIndex * 40);
            context.stroke();
            context.setLineDash([]);
        }
    
        // Add explanation
        context.fillStyle = colors.text;
        context.textAlign = "left";
        context.font = "16px Arial";
        let textY = height - 200;
        [
            "Matrix Multiplication in Neural Networks:",
            "• Input vector: x = [x₁, x₂, x₃]ᵀ",
            "• Weight matrix: W = [w₁₁ w₁₂ w₁₃; w₂₁ w₂₂ w₂₃; w₃₁ w₃₂ w₃₃]",
            "• Output: y = Wx",
            `• Current calculation: row ${highlightIndex + 1}`
        ].forEach(line => {
            context.fillText(line, 50, textY);
            textY += 25;
        });
    }
    
    function drawBinaryClassification() {
        const centerX = width/2;
        const centerY = height/2;
        
        // Generate sample data
        const samples = [];
        for(let i = 0; i < 50; i++) {
            const isOne = Math.random() > 0.5;
            samples.push({
                x: (Math.random() - 0.5) + (isOne ? 1 : -1),
                y: (Math.random() - 0.5) + (isOne ? 1 : -1),
                label: isOne ? 1 : 0
            });
        }
    
        // Draw coordinate system
        context.strokeStyle = colors.grid;
        context.lineWidth = 1;
        const scale = 100;
    
        // Grid
        for(let i = -5; i <= 5; i++) {
            context.beginPath();
            context.moveTo(centerX + i * scale, centerY - 5 * scale);
            context.lineTo(centerX + i * scale, centerY + 5 * scale);
            context.stroke();
    
            context.beginPath();
            context.moveTo(centerX - 5 * scale, centerY + i * scale);
            context.lineTo(centerX + 5 * scale, centerY + i * scale);
            context.stroke();
        }
    
        // Draw decision boundary (animated)
        const angle = currentTime % (Math.PI * 2);
        context.strokeStyle = colors.highlight;
        context.lineWidth = 2;
        context.beginPath();
        context.moveTo(centerX - 5 * scale * Math.cos(angle), 
                      centerY - 5 * scale * Math.sin(angle));
        context.lineTo(centerX + 5 * scale * Math.cos(angle), 
                      centerY + 5 * scale * Math.sin(angle));
        context.stroke();
    
    // Draw samples with brighter colors
    samples.forEach(sample => {
        context.beginPath();
        context.arc(
            centerX + sample.x * scale,
            centerY + sample.y * scale,
            6,  // Slightly larger points
            0,
            Math.PI * 2
        );
        context.fillStyle = sample.label ? colors.class1 : colors.class2;
        context.fill();
        context.strokeStyle = colors.text;
        context.stroke();
    });

    // Add better text visibility
    const textBackground = {
        x: 30,
        y: 30,
        width: 300,
        height: 150
    };

    // Draw text background
    context.fillStyle = "rgba(0, 0, 0, 0.7)";
    context.fillRect(
        textBackground.x,
        textBackground.y,
        textBackground.width,
        textBackground.height
    );

    // Draw text
    context.fillStyle = colors.text;
    context.font = "18px Arial";
    let textY = textBackground.y + 30;
    [
        "Binary Classification:",
        "• Red points: Class 1",
        "• Blue points: Class 0",
        "• Yellow line: Decision boundary",
        `• Accuracy: ${calculateAccuracy(samples, angle).toFixed(2)}%`
    ].forEach(line => {
        context.fillText(line, textBackground.x + 20, textY);
        textY += 25;
    });
    }
    
    function calculateAccuracy(samples, angle) {
        let correct = 0;
        samples.forEach(sample => {
            const prediction = sample.x * Math.cos(angle) + 
                             sample.y * Math.sin(angle) > 0 ? 1 : 0;
            if(prediction === sample.label) correct++;
        });
        return (correct / samples.length) * 100;
    }
    
    function drawBackpropagation() {
        const centerX = width/2;
        const centerY = height/2;
        
        // Draw simplified network
        const layers = [2, 3, 1];  // Simple network architecture
        const nodes = [];
        const errors = [];
        
        // Calculate node positions
        layers.forEach((size, layerIndex) => {
            nodes[layerIndex] = [];
            errors[layerIndex] = [];
            for(let i = 0; i < size; i++) {
                const x = centerX + (layerIndex - 1) * 200;
                const y = centerY + (i - size/2) * 100;
                nodes[layerIndex].push({x, y});
                errors[layerIndex].push(Math.sin(currentTime + i + layerIndex));
            }
        });
    
        // Draw connections with clearer gradients
        for(let l = 0; l < layers.length - 1; l++) {
            for(let i = 0; i < layers[l]; i++) {
                for(let j = 0; j < layers[l+1]; j++) {
                    const gradient = errors[l][i] * errors[l+1][j];
                    const color = gradient > 0 ? colors.positive : colors.negative;
                    context.strokeStyle = color;
                    context.globalAlpha = Math.min(Math.abs(gradient) + 0.2, 1);  // Increase minimum opacity
                    
                    context.beginPath();
                    context.moveTo(nodes[l][i].x, nodes[l][i].y);
                    context.lineTo(nodes[l+1][j].x, nodes[l+1][j].y);
                    context.lineWidth = 3;  // Thicker lines
                    context.stroke();
                }
            }
        }
        context.globalAlpha = 1;
    
        // Draw nodes with error values
        layers.forEach((size, l) => {
            for(let i = 0; i < size; i++) {
                // Draw node
                context.beginPath();
                context.arc(nodes[l][i].x, nodes[l][i].y, 20, 0, Math.PI * 2);
                context.fillStyle = colors.neuron;
                context.fill();
                context.strokeStyle = colors.text;
                context.stroke();
    
                // Draw error value
                context.fillStyle = colors.text;
                context.font = "12px Arial";
                context.textAlign = "center";
                context.fillText(
                    `δ: ${errors[l][i].toFixed(2)}`,
                    nodes[l][i].x,
                    nodes[l][i].y + 30
                );
            }
        });
    
        // Add explanation
        // context.fillStyle = colors.text;
        // context.font = "16px Arial";
        // context.textAlign = "left";
        // let textY = 50;
        // [
        //     "Backpropagation:",
        //     "• Red connections: Positive gradients",
        //     "• Blue connections: Negative gradients",
        //     "• δ: Error gradient at each node",
        //     "• Opacity: Gradient magnitude",
        //     "• Chain rule: δⱼ = Σ(δₖ·wⱼₖ)·f'(zⱼ)"
        // ].forEach(line => {
        //     context.fillText(line, 50, textY);
        //     textY += 25;
        // });
    }

    function draw() {
        // Clear canvas
        context.fillStyle = colors.background;
        context.fillRect(0, 0, width, height);

        switch(currentMode) {
            case "mlp":
                drawNetwork();
                break;
            case "perceptron":
                drawPerceptron();
                break;
            case "loss":
                drawLossFunction();
                break;
            case "activation":
                drawActivationFunction();
                break;
            case "matrix":
                drawMatrixTransformation();
                break;
            case "binary":
                drawBinaryClassification();
                break;
            case "backprop":
                drawBackpropagation();
                break;
        }

        // Draw mode selection info
        context.fillStyle = colors.text;
        context.font = "16px Arial";
        context.textAlign = "left";
        
        let textY = height - 600;
        [
            "Controls:",
            "Ctrl + 1: Full MLP",
            "Ctrl + 2: Perceptron",
            "Ctrl + 3: Loss Function",
            "Ctrl + 4: Activation Functions",
            "Ctrl + 5: Matrix Transformation",
            "Ctrl + 6: Binary Classification",
            "Ctrl + 7: Back Propagation",
            "Space: Pause/Resume"
        ].forEach(line => {
            context.fillText(line, 20, textY);
            textY += 25;
        });
    }

    function animate() {
        if (isAnimating) {
            currentTime += 0.02;
            draw();
            requestAnimationFrame(animate);
        }
    }

    // Initialize
    initializeNetwork();

    // Event handlers
    document.addEventListener('keydown', function(event) {
        if (event.ctrlKey || event.metaKey) {
            switch(event.key) {
                case '1':
                    currentMode = "mlp";
                    break;
                case '2':
                    currentMode = "perceptron";
                    break;
                case '3':
                    currentMode = "loss";
                    break;
                case '4':
                    currentMode = "activation";
                    break;
                case '5':
                    currentMode = "matrix";
                    break;
                case '6':
                    currentMode = "binary";
                    break;
                case '7':
                    currentMode = "backprop";
                    break;
            }
        } else if (event.code === 'Space') {
            isAnimating = !isAnimating;
            if(isAnimating) animate();
        }
    });

    animate();
};