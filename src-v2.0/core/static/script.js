document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:5001/api';

    const terminalInput = document.getElementById('terminal-input');
    const terminalOutput = document.getElementById('terminal-output');
    const codeDisplay = document.getElementById('code-display');
    const cyContainer = document.getElementById('cy');
    
    let previousGraphElements = null;
    let currentGraphType = 'node'; // State to track current view

    const cy = cytoscape({
        container: cyContainer,
        style: [
            {
                selector: 'node',
                style: {
                    'shape': 'rectangle',
                    'background-color': 'data(color)',
                    'label': 'data(label)',
                    'color': '#111', // Dark text for light background
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '10px',
                    'text-wrap': 'wrap',
                    'text-max-width': '80px',
                    'width': 'label',
                    'height': 'label',
                    'padding': '10px',
                    'border-width': 1,
                    'border-color': '#ccc'
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 1.5,
                    'line-color': '#666', // Darker line color
                    'target-arrow-color': '#666', // Darker arrow color
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            }
        ],
        layout: {
            name: 'dagre',
            rankDir: 'LR', // Left-to-Right
            spacingFactor: 1.25
        }
    });

    terminalInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && terminalInput.value.trim() !== '') {
            const command = terminalInput.value.trim();
            appendToTerminal(`> ${command}`, 'user-command');
            handleCommand(command);
            terminalInput.value = '';
        }
    });

    cy.on('tap', 'node', (event) => {
        const node = event.target;
        const nodeId = node.id();

        if (currentGraphType === 'class') {
            return;
        }

        if (currentGraphType === 'node' && nodeId !== 'Meta' && nodeId.substring(nodeId.length - 3) === '.py' ) {
            fetchCode(nodeId);
            document.querySelector('input[name="graph-type"][value="class"]').checked = true;
            updateGraph('class', nodeId);
        }
    });

    document.querySelectorAll('input[name="graph-type"]').forEach(radio => {
        radio.addEventListener('change', (event) => {
            if (event.target.value === 'node') {
                updateGraph('node');
            }
        });
    });

    const handleCommand = (command) => {
        const parts = command.split(/\s+/);
        if (parts[0].toLowerCase() === 'code_get' && parts.length > 1) {
            const fullNodeId = parts.slice(1).join(' ');
            fetchCode(fullNodeId);
        } else {
            const message = command.startsWith('run message =') ? command.substring(14).trim() : command;
            runMessage(message);
        }
    };

    const fetchCode = async (nodeId) => {
        const fileNodeId = nodeId.split('-')[0];
        appendToTerminal(`Fetching code for: ${fileNodeId}...`, 'system-response');
        try {
            const response = await fetch(`${API_BASE_URL}/code_get`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ node_id: fileNodeId })
            });

            if (!response.ok) throw new Error(`Server error: ${response.statusText}`);

            const data = await response.json();
            if (data.error) throw new Error(data.error);

            codeDisplay.textContent = data.code;
            Prism.highlightElement(codeDisplay);
            appendToTerminal(`Code for ${fileNodeId} loaded successfully.`, 'system-response');
        } catch (error) {
            appendToTerminal(`Error fetching code: ${error.message}`, 'error-response');
        }
    };

    const runMessage = async (message) => {
        appendToTerminal('Agent is processing your request...', 'system-response loading');
        terminalInput.disabled = true;

        codeDisplay.textContent = 'Waiting for result...';

        try {
            const response = await fetch(`${API_BASE_URL}/request`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
            const data = await response.json();
            if (data.error) throw new Error(data.error);
            
            removeLoadingMessage();
            const resultText = data.result || data.stop_message || 'The agent did not produce a result.';
            codeDisplay.textContent = resultText;
            Prism.highlightElement(codeDisplay);
            appendToTerminal(resultText, 'system-response');
            appendToTerminal('Agent processing complete.', 'system-response');

            document.querySelector('input[name="graph-type"][value="node"]').checked = true;
            updateGraph('node');
        } catch (error) {
            removeLoadingMessage();
            const errorMessage = `Error processing message: ${error.message}`;
            appendToTerminal(errorMessage, 'error-response');
            codeDisplay.textContent = 'An error occurred.';
            Prism.highlightElement(codeDisplay);
        } finally {
            terminalInput.disabled = false;
            terminalInput.focus();
        }
    };

    const updateGraph = async (graphType = 'node', nodeId = null) => {
        currentGraphType = graphType;
        try {
            let url = `${API_BASE_URL}/structure?type=${graphType}`;
            if (nodeId) {
                url += `&node_id=${nodeId}`;
            }
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
            
            const data = await response.json();
            if (data.error) throw new Error(data.error);

            if (data.elements) {
                const currentElements = data.elements;
                const prevNodeIds = previousGraphElements 
                    ? new Set(JSON.parse(previousGraphElements).nodes.map(n => n.data.id)) 
                    : new Set();

                currentElements.nodes.forEach(node => {
                    node.data.color = '#a9d4ff'; // Main node color (blue)
                    if (!prevNodeIds.has(node.data.id)) {
                        node.data.color = '#ffc0cb'; // New node color (red)
                    }
                });

                cy.elements().remove();
                cy.add(currentElements);
                cy.layout({ name: 'dagre', rankDir: 'LR', spacingFactor: 1.25 }).run();
                
                previousGraphElements = JSON.stringify(currentElements);
            }
        } catch (error) {
            appendToTerminal(`Failed to update graph: ${error.message}`, 'error-response');
        }
    };

    const appendToTerminal = (text, className) => {
        const line = document.createElement('div');
        line.innerHTML = text.replace(/\n/g, '<br>');
        line.className = `terminal-line ${className || ''}`;
        terminalOutput.appendChild(line);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    };
    
    const removeLoadingMessage = () => {
        const loadingElement = terminalOutput.querySelector('.loading');
        if (loadingElement) {
            loadingElement.textContent = loadingElement.textContent.replace('...', ' done.');
            loadingElement.classList.remove('loading');
        }
    };

    const initialize = () => {
        appendToTerminal('Welcome to the Self-Evolving Software Interface.', 'system-response');
        appendToTerminal('You can type a request or use "code_get <node_id>".', 'system-response');
        updateGraph('node');
        terminalInput.focus();
    };

    initialize();
});