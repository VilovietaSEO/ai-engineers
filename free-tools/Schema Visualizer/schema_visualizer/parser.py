"""
Schema parser for converting JSON-LD to graph structure
"""

import json
from typing import Dict, List, Tuple, Set, Any


class SchemaParser:
    """Parse Schema.org JSON-LD markup into graph nodes and edges"""

    def __init__(self):
        self.nodes: Set[Tuple] = set()
        self.edges: Set[Tuple] = set()
        self.node_counter = 0

    def parse(self, schema_input: str) -> Dict[str, Any]:
        """
        Parse schema input and return nodes and edges

        Args:
            schema_input: JSON-LD string or file path

        Returns:
            Dictionary with 'nodes', 'edges', and optionally 'error'
        """
        try:
            # Try to parse as JSON
            if isinstance(schema_input, str):
                if schema_input.strip().startswith('{') or schema_input.strip().startswith('['):
                    schema_data = json.loads(schema_input)
                else:
                    # Assume it's a file path
                    with open(schema_input, 'r', encoding='utf-8') as f:
                        schema_data = json.load(f)
            else:
                schema_data = schema_input

            # Reset nodes and edges
            self.nodes = set()
            self.edges = set()
            self.node_counter = 0

            # Parse the schema
            self._recursive_parse(schema_data)

            return {
                "nodes": list(self.nodes),
                "edges": list(self.edges),
                "valid": True
            }

        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON format: {str(e)}",
                "valid": False
            }
        except FileNotFoundError as e:
            return {
                "error": f"File not found: {str(e)}",
                "valid": False
            }
        except Exception as e:
            return {
                "error": f"Error parsing schema: {str(e)}",
                "valid": False
            }

    def _recursive_parse(self, data: Any, parent: str = None, path: str = "") -> str:
        """
        Recursively parse schema data to extract nodes and edges

        Args:
            data: Current data being parsed
            parent: Parent node identifier
            path: Current path in the schema hierarchy

        Returns:
            Current node identifier
        """
        current_node = None

        if isinstance(data, dict):
            # Handle @type property (Schema.org type)
            if "@type" in data:
                schema_type = data["@type"]

                # Handle multiple types (array)
                if isinstance(schema_type, list):
                    schema_type = schema_type[0]

                # Create unique node identifier
                node_id = f"{schema_type}_{self.node_counter}"
                self.node_counter += 1

                # Use 'name' property as label if available, otherwise use type
                node_label = data.get('name', schema_type)

                # Add type node
                self.nodes.add(("type", node_id, node_label, schema_type))

                # Connect to parent if exists
                if parent:
                    self.edges.add((parent, node_id))

                current_node = node_id

            # Process all properties
            for key, value in data.items():
                if key in ["@type", "@context", "name"]:
                    continue

                # Handle @id specially (it's a reference)
                if key == "@id":
                    prop_id = f"id_{self.node_counter}"
                    self.node_counter += 1
                    self.nodes.add(("property", prop_id, f"@id: {value}", "identifier"))
                    if current_node:
                        self.edges.add((current_node, prop_id))
                    continue

                # Create property node
                prop_id = f"{key}_{self.node_counter}"
                self.node_counter += 1

                # Determine if this property has a complex value
                is_complex = isinstance(value, (dict, list))

                if is_complex:
                    # For complex values, create property node and recurse
                    self.nodes.add(("property", prop_id, key, "property"))
                    if current_node:
                        self.edges.add((current_node, prop_id))
                    else:
                        self.edges.add((parent, prop_id))

                    self._recursive_parse(value, prop_id, f"{path}_{key}")
                else:
                    # For simple values, create property node with value
                    display_value = str(value)
                    if len(display_value) > 50:
                        display_value = display_value[:47] + "..."

                    label = f"{key}: {display_value}"
                    self.nodes.add(("property", prop_id, label, "property"))

                    if current_node:
                        self.edges.add((current_node, prop_id))
                    elif parent:
                        self.edges.add((parent, prop_id))

        elif isinstance(data, list):
            # Handle arrays (e.g., multiple items in a list)
            for index, item in enumerate(data):
                self._recursive_parse(item, parent, f"{path}_{index}")

        return current_node

    def validate_schema(self, schema_data: Dict) -> Dict[str, Any]:
        """
        Validate schema structure

        Args:
            schema_data: Parsed JSON data

        Returns:
            Validation result with warnings and errors
        """
        warnings = []
        errors = []

        # Check for @context
        if isinstance(schema_data, dict):
            if "@context" not in schema_data:
                warnings.append("Missing @context - recommended to include Schema.org context")

            # Check for @type
            if "@type" not in schema_data:
                errors.append("Missing @type - required for Schema.org markup")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about parsed schema"""
        type_nodes = sum(1 for n in self.nodes if n[0] == "type")
        property_nodes = sum(1 for n in self.nodes if n[0] == "property")

        return {
            "total_nodes": len(self.nodes),
            "type_nodes": type_nodes,
            "property_nodes": property_nodes,
            "total_edges": len(self.edges)
        }
