// Schema Parser and Visualizer - JavaScript Implementation
// Port of Python schema_visualizer functionality for client-side use

let network = null;
let currentNodes = [];
let currentEdges = [];
let isGenericMode = false;

// Schema Type Colors (matching Python config)
const SCHEMA_COLORS = {
    'Person': '#E74C3C',
    'Organization': '#45B7D1',
    'Place': '#76D7C4',
    'LocalBusiness': '#76D7C4',
    'Product': '#D35400',
    'Offer': '#E67E22',
    'Review': '#9B59B6',
    'Rating': '#8E44AD',
    'AggregateRating': '#D35400',
    'Article': '#9B59B6',
    'BlogPosting': '#8E44AD',
    'NewsArticle': '#6C3483',
    'WebPage': '#7D3C98',
    'WebSite': '#884EA0',
    'Event': '#F39C12',
    'PostalAddress': '#7FB3D5',
    'GeoCoordinates': '#76D7C4',
    'ImageObject': '#58D68D',
    'VideoObject': '#52BE80',
    'ContactPoint': '#85C1E2',
    'OpeningHoursSpecification': '#A9DFBF',
    'ItemList': '#F8B739',
    'ListItem': '#F5B041',
    'BreadcrumbList': '#EB984E',
    'SearchAction': '#5DADE2',
    'Action': '#3498DB',
    'Question': '#AF7AC5',
    'Answer': '#BB8FCE',
    'FAQPage': '#D7BDE2',
    'HowTo': '#85929E',
    'HowToStep': '#99A3A4',
    'default': '#45B7D1'
};

// Generic JSON Parser Class (for any JSON structure)
class GenericJsonParser {
    constructor() {
        this.nodes = [];
        this.edges = [];
        this.nodeCounter = 0;
    }

    parse(jsonInput) {
        try {
            let jsonData;

            // Parse JSON string
            if (typeof jsonInput === 'string') {
                jsonData = JSON.parse(jsonInput);
            } else {
                jsonData = jsonInput;
            }

            // Reset parser state
            this.nodes = [];
            this.edges = [];
            this.nodeCounter = 0;

            // Start parsing from root
            this.recursiveParse(jsonData, null, 'root');

            return {
                nodes: this.nodes,
                edges: this.edges,
                valid: true
            };

        } catch (error) {
            return {
                error: `Invalid JSON format: ${error.message}`,
                valid: false
            };
        }
    }

    recursiveParse(data, parent = null, key = 'root', isArrayItem = false) {
        const nodeId = `node_${this.nodeCounter}`;
        this.nodeCounter++;

        if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
            // Object node
            const label = isArrayItem ? `[${key}]` : key;
            this.nodes.push({
                type: 'object',
                id: nodeId,
                label: label,
                objectType: 'object'
            });

            if (parent) {
                this.edges.push({ from: parent, to: nodeId });
            }

            // Process all properties
            for (const [propKey, propValue] of Object.entries(data)) {
                this.recursiveParse(propValue, nodeId, propKey);
            }

        } else if (Array.isArray(data)) {
            // Array node
            const label = `${key} [${data.length}]`;
            this.nodes.push({
                type: 'array',
                id: nodeId,
                label: label,
                objectType: 'array'
            });

            if (parent) {
                this.edges.push({ from: parent, to: nodeId });
            }

            // Process array items
            data.forEach((item, index) => {
                this.recursiveParse(item, nodeId, index.toString(), true);
            });

        } else {
            // Primitive value (string, number, boolean, null)
            let displayValue = String(data);
            if (displayValue.length > 50) {
                displayValue = displayValue.substring(0, 47) + '...';
            }

            const label = isArrayItem ? displayValue : `${key}: ${displayValue}`;
            this.nodes.push({
                type: 'value',
                id: nodeId,
                label: label,
                objectType: 'primitive'
            });

            if (parent) {
                this.edges.push({ from: parent, to: nodeId });
            }
        }

        return nodeId;
    }

    getStatistics() {
        const objectNodes = this.nodes.filter(n => n.type === 'object').length;
        const arrayNodes = this.nodes.filter(n => n.type === 'array').length;
        const valueNodes = this.nodes.filter(n => n.type === 'value').length;

        return {
            totalNodes: this.nodes.length,
            objectNodes: objectNodes,
            arrayNodes: arrayNodes,
            valueNodes: valueNodes,
            totalEdges: this.edges.length
        };
    }
}

// Schema Parser Class
class SchemaParser {
    constructor() {
        this.nodes = [];
        this.edges = [];
        this.nodeCounter = 0;
    }

    parse(schemaInput) {
        try {
            let schemaData;

            // Parse JSON string
            if (typeof schemaInput === 'string') {
                schemaData = JSON.parse(schemaInput);
            } else {
                schemaData = schemaInput;
            }

            // Reset parser state
            this.nodes = [];
            this.edges = [];
            this.nodeCounter = 0;

            // Parse the schema recursively
            this.recursiveParse(schemaData);

            return {
                nodes: this.nodes,
                edges: this.edges,
                valid: true
            };

        } catch (error) {
            return {
                error: `Invalid JSON format: ${error.message}`,
                valid: false
            };
        }
    }

    recursiveParse(data, parent = null, path = '') {
        let currentNode = null;

        if (typeof data === 'object' && data !== null && !Array.isArray(data)) {
            // Handle @type property (Schema.org type)
            if (data['@type']) {
                let schemaType = data['@type'];

                // Handle multiple types (array)
                if (Array.isArray(schemaType)) {
                    schemaType = schemaType[0];
                }

                // Create unique node identifier
                const nodeId = `${schemaType}_${this.nodeCounter}`;
                this.nodeCounter++;

                // Use 'name' property as label if available
                const nodeLabel = data.name || schemaType;

                // Add type node
                this.nodes.push({
                    type: 'type',
                    id: nodeId,
                    label: nodeLabel,
                    schemaType: schemaType
                });

                // Connect to parent if exists
                if (parent) {
                    this.edges.push({ from: parent, to: nodeId });
                }

                currentNode = nodeId;
            }

            // Process all properties
            for (const [key, value] of Object.entries(data)) {
                if (['@type', '@context', 'name'].includes(key)) {
                    continue;
                }

                // Handle @id specially
                if (key === '@id') {
                    const propId = `id_${this.nodeCounter}`;
                    this.nodeCounter++;
                    this.nodes.push({
                        type: 'property',
                        id: propId,
                        label: `@id: ${value}`,
                        propertyType: 'identifier'
                    });
                    if (currentNode) {
                        this.edges.push({ from: currentNode, to: propId });
                    }
                    continue;
                }

                // Create property node
                const propId = `${key}_${this.nodeCounter}`;
                this.nodeCounter++;

                // Check if value is complex
                const isComplex = typeof value === 'object' && value !== null;

                if (isComplex) {
                    // For complex values, create property node and recurse
                    this.nodes.push({
                        type: 'property',
                        id: propId,
                        label: key,
                        propertyType: 'property'
                    });

                    const sourceNode = currentNode || parent;
                    if (sourceNode) {
                        this.edges.push({ from: sourceNode, to: propId });
                    }

                    this.recursiveParse(value, propId, `${path}_${key}`);
                } else {
                    // For simple values, create property node with value
                    let displayValue = String(value);
                    if (displayValue.length > 50) {
                        displayValue = displayValue.substring(0, 47) + '...';
                    }

                    const label = `${key}: ${displayValue}`;
                    this.nodes.push({
                        type: 'property',
                        id: propId,
                        label: label,
                        propertyType: 'property'
                    });

                    const sourceNode = currentNode || parent;
                    if (sourceNode) {
                        this.edges.push({ from: sourceNode, to: propId });
                    }
                }
            }

        } else if (Array.isArray(data)) {
            // Handle arrays
            data.forEach((item, index) => {
                this.recursiveParse(item, parent, `${path}_${index}`);
            });
        }

        return currentNode;
    }

    validateSchema(schemaData) {
        const warnings = [];
        const errors = [];

        if (typeof schemaData === 'object' && schemaData !== null && !Array.isArray(schemaData)) {
            // Check for @context
            if (!schemaData['@context']) {
                warnings.push('Missing @context - recommended to include Schema.org context');
            }

            // Check for @type
            if (!schemaData['@type']) {
                errors.push('Missing @type - required for Schema.org markup');
            }
        }

        return {
            valid: errors.length === 0,
            errors: errors,
            warnings: warnings
        };
    }

    getStatistics() {
        const typeNodes = this.nodes.filter(n => n.type === 'type').length;
        const propertyNodes = this.nodes.filter(n => n.type === 'property').length;

        return {
            totalNodes: this.nodes.length,
            typeNodes: typeNodes,
            propertyNodes: propertyNodes,
            totalEdges: this.edges.length
        };
    }
}

// Visualize the schema
function visualizeSchema() {
    const input = document.getElementById('schema-input').value.trim();

    if (!input) {
        const modeText = isGenericMode ? 'JSON data' : 'Schema.org JSON-LD markup';
        showMessage(`Please enter some ${modeText}`, 'error');
        return;
    }

    let parser, result, validation;

    if (isGenericMode) {
        // Generic JSON Mode
        parser = new GenericJsonParser();
        result = parser.parse(input);

        if (!result.valid) {
            showMessage(result.error, 'error');
            return;
        }

        validation = { valid: true, errors: [], warnings: [] };
    } else {
        // Schema.org Mode
        parser = new SchemaParser();
        result = parser.parse(input);

        if (!result.valid) {
            showMessage(result.error, 'error');
            return;
        }

        // Validate schema
        let schemaData;
        try {
            schemaData = JSON.parse(input);
        } catch (e) {
            schemaData = {};
        }

        validation = parser.validateSchema(schemaData);
    }

    // Store for later use
    currentNodes = result.nodes;
    currentEdges = result.edges;

    // Create visualization
    createVisualization(result.nodes, result.edges);

    // Show statistics
    const stats = parser.getStatistics();
    showStatistics(stats, isGenericMode);

    // Show validation messages
    showValidationMessages(validation);

    // Show success message
    const successMsg = isGenericMode ? 'JSON visualized successfully!' : 'Schema visualized successfully!';
    showMessage(successMsg, 'success');

    // Show details panel
    document.getElementById('details-panel').style.display = 'block';
}

// Create vis.js network visualization
function createVisualization(nodes, edges) {
    console.log('createVisualization called with', nodes.length, 'nodes and', edges.length, 'edges');

    const container = document.getElementById('network-container');
    if (!container) {
        console.error('Network container not found!');
        return;
    }

    console.log('Container dimensions:', container.clientWidth, 'x', container.clientHeight);

    // Ensure container has dimensions
    if (container.clientHeight === 0) {
        console.warn('Container has no height! Setting explicit height...');
        container.style.height = '600px';
    }

    // Hide empty state
    const emptyState = document.getElementById('empty-state');
    if (emptyState) {
        emptyState.style.display = 'none';
    }

    try {
        // Determine if dark mode is active
        const isDarkMode = document.documentElement.classList.contains('dark');
        const edgeColor = isDarkMode ? '#e2e8f0' : '#1e293b';
        const fontColor = isDarkMode ? '#e2e8f0' : '#1e293b';

        // Prepare nodes for vis.js
        const visNodes = nodes.map(node => {
            let color, size, title;

            if (isGenericMode) {
                // Generic JSON Mode colors
                if (node.type === 'object') {
                    color = '#45B7D1'; // Blue for objects
                    size = 18;
                    title = `Object: ${node.label}`;
                } else if (node.type === 'array') {
                    color = '#F39C12'; // Orange for arrays
                    size = 15;
                    title = `Array: ${node.label}`;
                } else {
                    color = '#BDC3C7'; // Gray for values
                    size = 10;
                    title = `Value: ${node.label}`;
                }
            } else {
                // Schema.org Mode colors
                if (node.type === 'type') {
                    color = SCHEMA_COLORS[node.schemaType] || SCHEMA_COLORS.default;
                    size = 18;
                    title = `Type: ${node.schemaType}\nLabel: ${node.label}`;
                } else {
                    color = '#BDC3C7';
                    size = 10;
                    title = `Property: ${node.label}`;
                }
            }

            return {
                id: node.id,
                label: node.label,
                title: title,
                color: color, // SIMPLE string, not object!
                size: size,
                font: {
                    color: fontColor,
                    size: 12,
                    face: 'Inter, sans-serif'
                },
                shape: 'dot'
            };
        });

        // Prepare edges for vis.js
        const visEdges = edges.map(edge => ({
            from: edge.from,
            to: edge.to,
            color: edgeColor,
            width: 1,
            arrows: 'to'
        }));

        // Create network data
        const data = {
            nodes: new vis.DataSet(visNodes),
            edges: new vis.DataSet(visEdges)
        };

        // Network options
        const options = {
            physics: {
                enabled: true,
                stabilization: {
                    enabled: true,
                    iterations: 200, // Limit iterations
                    updateInterval: 25
                },
                barnesHut: {
                    gravitationalConstant: -8000,
                    centralGravity: 0.3,
                    springLength: 95,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.1
                },
                minVelocity: 0.75
            },
            interaction: {
                hover: true,
                tooltipDelay: 100,
                zoomView: true,
                dragView: true
            }
        };

        // Create network
        if (network) {
            network.destroy();
        }

        network = new vis.Network(container, data, options);
        console.log('Network created successfully!');

        // Simple approach: just fit the network after physics stabilizes
        network.once('stabilizationIterationsDone', function() {
            console.log('Stabilization complete, fitting network...');
            network.fit({
                animation: {
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }
            });
        });

    } catch (error) {
        console.error('Error creating visualization:', error);
        alert(`Error creating visualization: ${error.message}\n\nPlease check the browser console for details.`);
    }
}

// Highlight clicked node
function highlightNode(node) {
    let message = '';
    if (node.type === 'type') {
        message = `<strong>Type:</strong> ${node.schemaType}<br><strong>Label:</strong> ${node.label}`;
    } else {
        message = `<strong>Property:</strong> ${node.label}`;
    }

    showMessage(message, 'info', true);
}

// Show statistics
function showStatistics(stats, isGeneric = false) {
    const statsGrid = document.getElementById('stats-grid');

    if (isGeneric) {
        statsGrid.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Total Nodes</div>
                <div class="stat-value">${stats.totalNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Objects</div>
                <div class="stat-value">${stats.objectNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Arrays</div>
                <div class="stat-value">${stats.arrayNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Values</div>
                <div class="stat-value">${stats.valueNodes}</div>
            </div>
        `;
    } else {
        statsGrid.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Total Nodes</div>
                <div class="stat-value">${stats.totalNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Type Nodes</div>
                <div class="stat-value">${stats.typeNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Properties</div>
                <div class="stat-value">${stats.propertyNodes}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Connections</div>
                <div class="stat-value">${stats.totalEdges}</div>
            </div>
        `;
    }
}

// Show validation messages
function showValidationMessages(validation) {
    const messagesDiv = document.getElementById('messages');
    let html = '';

    if (validation.errors.length > 0) {
        html += '<div class="message message-error"><i class="fas fa-exclamation-circle"></i><div>';
        html += '<strong>Errors:</strong><ul>';
        validation.errors.forEach(error => {
            html += `<li>${error}</li>`;
        });
        html += '</ul></div></div>';
    }

    if (validation.warnings.length > 0) {
        html += '<div class="message message-warning"><i class="fas fa-exclamation-triangle"></i><div>';
        html += '<strong>Warnings:</strong><ul>';
        validation.warnings.forEach(warning => {
            html += `<li>${warning}</li>`;
        });
        html += '</ul></div></div>';
    }

    messagesDiv.innerHTML = html;
}

// Show message as toast notification
function showMessage(message, type = 'info', isHtml = false) {
    console.log(`[${type.toUpperCase()}] ${message}`);

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    // Icon based on type
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    const icon = icons[type] || icons.info;

    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <div>${isHtml ? message : escapeHtml(message)}</div>
    `;

    // Add to document
    document.body.appendChild(toast);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Helper to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Clear input
function clearInput() {
    document.getElementById('schema-input').value = '';
    if (network) {
        network.destroy();
        network = null;
    }
    document.getElementById('details-panel').style.display = 'none';
    document.getElementById('empty-state').style.display = 'flex';
}

// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        document.getElementById('schema-input').value = content;
        showMessage(`File "${file.name}" loaded successfully!`, 'success');
    };
    reader.onerror = function() {
        showMessage('Error reading file', 'error');
    };
    reader.readAsText(file);
}

// Toggle between Schema.org and Generic JSON modes
function toggleMode() {
    isGenericMode = document.getElementById('mode-toggle').checked;
    const textarea = document.getElementById('schema-input');

    if (isGenericMode) {
        // Generic JSON Mode
        textarea.placeholder = `Paste any JSON data here...

Example:
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "active": true
    }
  ],
  "settings": {
    "theme": "dark",
    "notifications": true
  }
}`;
        showMessage('Switched to Generic JSON Mode', 'info');
    } else {
        // Schema.org Mode
        textarea.placeholder = `Paste your Schema.org JSON-LD here...

Example:
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "John Doe",
  "jobTitle": "Software Engineer",
  "url": "https://example.com"
}`;
        showMessage('Switched to Schema.org Mode', 'info');
    }

    // Update example buttons
    updateExampleButtons();

    // Clear visualization if exists
    if (network) {
        network.destroy();
        network = null;
        document.getElementById('details-panel').style.display = 'none';
        document.getElementById('empty-state').style.display = 'flex';
    }
}

// Update example buttons based on mode
function updateExampleButtons() {
    const examplesContainer = document.querySelector('.examples');

    if (isGenericMode) {
        // Generic JSON examples
        examplesContainer.innerHTML = `
            <div class="section-title">
                <i class="fas fa-lightbulb"></i>
                <span>Quick Examples</span>
            </div>
            <button class="example-btn" onclick="loadExample('api_response')">
                <i class="fas fa-server"></i> API Response
            </button>
            <button class="example-btn" onclick="loadExample('config')">
                <i class="fas fa-cog"></i> Configuration
            </button>
            <button class="example-btn" onclick="loadExample('ecommerce')">
                <i class="fas fa-shopping-cart"></i> E-commerce Order
            </button>
            <button class="example-btn" onclick="loadExample('analytics')">
                <i class="fas fa-chart-line"></i> Analytics Data
            </button>
        `;
    } else {
        // Schema.org examples
        examplesContainer.innerHTML = `
            <div class="section-title">
                <i class="fas fa-lightbulb"></i>
                <span>Quick Examples</span>
            </div>
            <button class="example-btn" onclick="loadExample('person')">
                <i class="fas fa-user"></i> Person Schema
            </button>
            <button class="example-btn" onclick="loadExample('product')">
                <i class="fas fa-box"></i> Product Schema
            </button>
            <button class="example-btn" onclick="loadExample('local_business')">
                <i class="fas fa-store"></i> Local Business Schema
            </button>
            <button class="example-btn" onclick="loadExample('article')">
                <i class="fas fa-newspaper"></i> Article Schema
            </button>
        `;
    }
}

// Embedded example schemas
const EXAMPLES = {
    person: {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "John Doe",
        "jobTitle": "Software Engineer",
        "telephone": "+1-555-123-4567",
        "email": "john.doe@example.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "123 Main St",
            "addressLocality": "San Francisco",
            "addressRegion": "CA",
            "postalCode": "94102",
            "addressCountry": "US"
        },
        "worksFor": {
            "@type": "Organization",
            "name": "Tech Company Inc.",
            "url": "https://techcompany.com"
        },
        "sameAs": [
            "https://twitter.com/johndoe",
            "https://linkedin.com/in/johndoe"
        ]
    },
    product: {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Executive Anvil",
        "image": [
            "https://example.com/photos/1x1/photo.jpg",
            "https://example.com/photos/4x3/photo.jpg",
            "https://example.com/photos/16x9/photo.jpg"
        ],
        "description": "Sleek and efficient anvil, perfect for business executives.",
        "sku": "0446310786",
        "mpn": "925872",
        "brand": {
            "@type": "Brand",
            "name": "ACME"
        },
        "review": {
            "@type": "Review",
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "4",
                "bestRating": "5"
            },
            "author": {
                "@type": "Person",
                "name": "Fred Flintstone"
            }
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.4",
            "reviewCount": "89"
        },
        "offers": {
            "@type": "Offer",
            "url": "https://example.com/anvil",
            "priceCurrency": "USD",
            "price": "119.99",
            "priceValidUntil": "2024-12-31",
            "itemCondition": "https://schema.org/NewCondition",
            "availability": "https://schema.org/InStock"
        }
    },
    local_business: {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "The Best Coffee Shop",
        "image": "https://example.com/photos/coffee-shop.jpg",
        "@id": "https://example.com/coffee-shop",
        "url": "https://example.com",
        "telephone": "+1-555-987-6543",
        "priceRange": "$$",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "456 Coffee Ave",
            "addressLocality": "Seattle",
            "addressRegion": "WA",
            "postalCode": "98101",
            "addressCountry": "US"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 47.6062,
            "longitude": -122.3321
        },
        "openingHoursSpecification": [
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                "opens": "07:00",
                "closes": "19:00"
            },
            {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Saturday", "Sunday"],
                "opens": "08:00",
                "closes": "20:00"
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "312"
        }
    },
    article: {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "How to Optimize Your Local SEO Strategy",
        "image": "https://example.com/article-image.jpg",
        "author": {
            "@type": "Person",
            "name": "Jane Smith",
            "url": "https://example.com/authors/jane-smith"
        },
        "publisher": {
            "@type": "Organization",
            "name": "SEO News",
            "logo": {
                "@type": "ImageObject",
                "url": "https://example.com/logo.png"
            }
        },
        "datePublished": "2024-01-15",
        "dateModified": "2024-01-20",
        "description": "Learn the best practices for local SEO optimization in 2024.",
        "articleBody": "In this comprehensive guide, we'll explore the essential strategies for improving your local search visibility..."
    }
};

// Generic JSON examples
const GENERIC_EXAMPLES = {
    api_response: {
        "status": "success",
        "data": {
            "users": [
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com",
                    "profile": {
                        "firstName": "John",
                        "lastName": "Doe",
                        "age": 30,
                        "verified": true
                    }
                },
                {
                    "id": 2,
                    "username": "janedoe",
                    "email": "jane@example.com",
                    "profile": {
                        "firstName": "Jane",
                        "lastName": "Doe",
                        "age": 28,
                        "verified": true
                    }
                }
            ],
            "pagination": {
                "page": 1,
                "perPage": 10,
                "total": 2
            }
        },
        "timestamp": "2024-01-15T10:30:00Z"
    },
    config: {
        "app": {
            "name": "My Application",
            "version": "1.2.3",
            "environment": "production"
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb",
            "poolSize": 20
        },
        "features": {
            "authentication": true,
            "analytics": true,
            "beta": false
        },
        "services": [
            {
                "name": "email",
                "enabled": true,
                "provider": "sendgrid"
            },
            {
                "name": "storage",
                "enabled": true,
                "provider": "s3"
            }
        ]
    },
    ecommerce: {
        "order": {
            "orderId": "ORD-2024-001",
            "customer": {
                "customerId": "CUST-123",
                "name": "Alice Smith",
                "email": "alice@example.com"
            },
            "items": [
                {
                    "productId": "PROD-A",
                    "name": "Wireless Mouse",
                    "quantity": 2,
                    "price": 29.99
                },
                {
                    "productId": "PROD-B",
                    "name": "USB Cable",
                    "quantity": 1,
                    "price": 9.99
                }
            ],
            "shipping": {
                "method": "express",
                "address": {
                    "street": "123 Main St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zip": "94102"
                },
                "tracking": "TRK123456789"
            },
            "payment": {
                "method": "credit_card",
                "status": "completed",
                "amount": 69.97
            }
        }
    },
    analytics: {
        "website": "example.com",
        "period": "2024-01",
        "metrics": {
            "visitors": {
                "total": 15420,
                "unique": 12350,
                "returning": 3070
            },
            "pageviews": {
                "total": 45600,
                "averagePerSession": 2.96
            },
            "engagement": {
                "avgSessionDuration": 185,
                "bounceRate": 42.5
            }
        },
        "topPages": [
            {
                "url": "/products",
                "views": 8500,
                "avgTimeOnPage": 245
            },
            {
                "url": "/blog",
                "views": 6200,
                "avgTimeOnPage": 320
            }
        ],
        "sources": {
            "organic": 8500,
            "direct": 4200,
            "social": 2100,
            "referral": 620
        }
    }
};

// Load example schemas
function loadExample(type) {
    console.log('Loading example:', type);

    // Choose the right example set based on mode
    const exampleSet = isGenericMode ? GENERIC_EXAMPLES : EXAMPLES;
    const example = exampleSet[type];

    if (!example) {
        console.error('Example not found:', type);
        alert(`Example "${type}" not found!`);
        return;
    }

    try {
        // Format and display the example
        const formattedJson = JSON.stringify(example, null, 2);
        document.getElementById('schema-input').value = formattedJson;
        console.log('Example loaded successfully:', type);

        // Auto-visualize after a short delay
        setTimeout(() => {
            console.log('Auto-visualizing example...');
            visualizeSchema();
        }, 300);
    } catch (error) {
        console.error('Error loading example:', error);
        alert(`Error loading example: ${error.message}`);
    }
}

// Network control functions
function fitNetwork() {
    if (network) {
        network.fit({
            animation: {
                duration: 500,
                easingFunction: 'easeInOutQuad'
            }
        });
    }
}

function resetPhysics() {
    if (network) {
        network.setOptions({ physics: { enabled: true } });
        network.stabilize();
    }
}

function exportImage() {
    if (network) {
        const canvas = network.canvas.frame.canvas;
        const dataURL = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = 'schema-visualization.png';
        link.href = dataURL;
        link.click();
        showMessage('Image exported successfully!', 'success');
    } else {
        showMessage('No visualization to export', 'warning');
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to visualize
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        visualizeSchema();
    }
});

// Initial message
console.log('%c🎨 Schema Visualizer', 'font-size: 20px; color: #667eea; font-weight: bold;');
console.log('%cPowered by Vibe Coders - https://www.skool.com/ai-agent-vibe-engineers', 'color: #667eea;');
console.log('Tip: Press Ctrl/Cmd + Enter to visualize');
