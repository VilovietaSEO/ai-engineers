"""
Schema visualizer using PyVis for interactive graph visualization
"""

import os
import webbrowser
from pyvis.network import Network
from typing import List, Tuple, Dict, Any
from .config import VisualizerConfig


class SchemaVisualizer:
    """Create interactive visualizations of schema graphs"""

    def __init__(self, layout="force_directed", theme="dark", width="100%", height="1000px"):
        """
        Initialize visualizer

        Args:
            layout: Layout type ('force_directed', 'hierarchical', 'circular')
            theme: Color theme ('dark', 'light', 'blue')
            width: Graph width
            height: Graph height
        """
        self.layout = layout
        self.theme = theme
        self.width = width
        self.height = height
        self.config = VisualizerConfig()

    def create_visualization(
        self,
        nodes: List[Tuple],
        edges: List[Tuple],
        output_file: str = "schema_visualization.html",
        auto_open: bool = True
    ) -> str:
        """
        Create interactive visualization from nodes and edges

        Args:
            nodes: List of node tuples (type, id, label, schema_type)
            edges: List of edge tuples (source, target)
            output_file: Output HTML file path
            auto_open: Whether to auto-open the visualization in browser

        Returns:
            Path to generated HTML file
        """
        # Get theme settings
        theme_config = self.config.THEMES.get(self.theme, self.config.THEMES["dark"])

        # Create network
        net = Network(
            notebook=False,
            height=self.height,
            width=self.width,
            bgcolor=theme_config["bgcolor"],
            font_color=theme_config["font_color"],
            directed=True
        )

        # Apply layout settings
        self._apply_layout(net)

        # Add nodes
        for node in nodes:
            node_kind = node[0]
            node_id = node[1]
            node_label = node[2]

            # Get node style based on type
            if node_kind == "type" and len(node) > 3:
                schema_type = node[3]
                style = self.config.get_node_style(schema_type)
            elif node_kind == "property":
                style = self.config.get_property_style()
            else:
                style = self.config.get_node_style("type")

            # Add node with styling
            net.add_node(
                node_id,
                label=node_label,
                title=self._create_tooltip(node),
                color=style["color"],
                size=style["size"],
                font={"color": theme_config["font_color"]}
            )

        # Add edges
        for edge in edges:
            net.add_edge(
                edge[0],
                edge[1],
                color=theme_config["edge_color"],
                width=1,
                arrows="to"
            )

        # Customize physics for better visualization
        if self.layout == "force_directed":
            net.set_options("""
            {
                "physics": {
                    "enabled": true,
                    "barnesHut": {
                        "gravitationalConstant": -8000,
                        "centralGravity": 0.3,
                        "springLength": 95,
                        "springConstant": 0.04,
                        "damping": 0.09,
                        "avoidOverlap": 0.1
                    },
                    "minVelocity": 0.75
                },
                "interaction": {
                    "hover": true,
                    "tooltipDelay": 100
                }
            }
            """)

        # Save the graph
        net.save_graph(output_file)

        # Add custom styling to HTML
        self._enhance_html(output_file)

        print(f"\nVisualization saved to: {output_file}")

        # Auto-open in browser
        if auto_open:
            abs_path = os.path.abspath(output_file)
            webbrowser.open(f"file://{abs_path}")
            print(f"Opening visualization in browser...")

        return output_file

    def _apply_layout(self, net: Network):
        """Apply layout configuration to network"""
        layout_config = self.config.LAYOUTS.get(self.layout)

        if not layout_config:
            return

        if "physics" in layout_config:
            net.toggle_physics(layout_config["physics"])

        if "hierarchical" in layout_config and layout_config.get("hierarchical"):
            net.set_options(f"""
            {{
                "layout": {{
                    "hierarchical": {str(layout_config["hierarchical"]).replace("'", '"').replace("True", "true").replace("False", "false")}
                }}
            }}
            """)

    def _create_tooltip(self, node: Tuple) -> str:
        """Create tooltip for node"""
        node_kind = node[0]
        node_label = node[2]

        if node_kind == "type" and len(node) > 3:
            schema_type = node[3]
            return f"Type: {schema_type}\nLabel: {node_label}"
        elif node_kind == "property":
            return f"Property: {node_label}"
        else:
            return node_label

    def _enhance_html(self, html_file: str):
        """Add custom styling and controls to generated HTML"""
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Add title and custom styling
        enhanced_html = html_content.replace(
            '</head>',
            '''
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                }
                .header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .header h1 {
                    margin: 0;
                    font-size: 24px;
                    font-weight: 600;
                }
                .header p {
                    margin: 5px 0 0 0;
                    font-size: 14px;
                    opacity: 0.9;
                }
                .controls {
                    background: #f8f9fa;
                    padding: 10px 20px;
                    border-bottom: 1px solid #dee2e6;
                    font-size: 12px;
                    color: #495057;
                }
                #mynetwork {
                    width: 100%;
                    height: calc(100vh - 120px);
                }
            </style>
            <title>Schema Visualization - MapPackSEO Toolbox</title>
            </head>
            '''
        )

        # Add header
        enhanced_html = enhanced_html.replace(
            '<body>',
            '''<body>
            <div class="header">
                <h1>Schema Markup Visualizer</h1>
                <p>Interactive visualization of Schema.org structured data</p>
            </div>
            <div class="controls">
                Use mouse to drag nodes • Scroll to zoom • Click nodes for details
            </div>
            '''
        )

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)

    def export_json(self, nodes: List[Tuple], edges: List[Tuple], output_file: str):
        """Export graph data as JSON"""
        import json

        graph_data = {
            "nodes": [
                {
                    "id": node[1],
                    "label": node[2],
                    "type": node[0],
                    "schema_type": node[3] if len(node) > 3 else None
                }
                for node in nodes
            ],
            "edges": [
                {"source": edge[0], "target": edge[1]}
                for edge in edges
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2)

        print(f"Graph data exported to: {output_file}")
        return output_file
