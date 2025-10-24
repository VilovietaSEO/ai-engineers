#!/usr/bin/env python3
"""
Schema Visualizer CLI Tool
A standalone tool for visualizing Schema.org markup as interactive graphs

Usage:
    python schema_visualizer.py input.json
    python schema_visualizer.py input.json -o output.html
    python schema_visualizer.py input.json --layout hierarchical --theme light
    python schema_visualizer.py input.json --export-json graph.json
    python schema_visualizer.py --stdin  (read from stdin)

Author: MapPackSEO Toolbox
"""

import argparse
import sys
import os
from schema_visualizer import SchemaParser, SchemaVisualizer, VisualizerConfig


def print_banner():
    """Print tool banner"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║         Schema Markup Visualizer - CLI Tool              ║
║         MapPackSEO Toolbox                                ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_statistics(stats):
    """Print schema statistics"""
    print("\n📊 Schema Statistics:")
    print(f"   Total Nodes: {stats['total_nodes']}")
    print(f"   - Type Nodes: {stats['type_nodes']}")
    print(f"   - Property Nodes: {stats['property_nodes']}")
    print(f"   Total Edges: {stats['total_edges']}")


def main():
    parser = argparse.ArgumentParser(
        description="Visualize Schema.org markup as interactive graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s schema.json
  %(prog)s schema.json -o visualization.html
  %(prog)s schema.json --layout hierarchical --theme light
  %(prog)s schema.json --export-json data.json --no-open
  cat schema.json | %(prog)s --stdin

Available Layouts:
  force_directed  - Dynamic force-directed layout (default)
  hierarchical    - Hierarchical tree layout
  circular        - Circular layout

Available Themes:
  dark   - Dark theme (default)
  light  - Light theme
  blue   - Blue theme
        """
    )

    # Input options
    parser.add_argument(
        'input',
        nargs='?',
        help='Path to JSON-LD schema file (or use --stdin)'
    )
    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read schema from stdin instead of file'
    )

    # Output options
    parser.add_argument(
        '-o', '--output',
        default='schema_visualization.html',
        help='Output HTML file path (default: schema_visualization.html)'
    )
    parser.add_argument(
        '--export-json',
        metavar='FILE',
        help='Export graph data as JSON to specified file'
    )

    # Visualization options
    parser.add_argument(
        '--layout',
        choices=['force_directed', 'hierarchical', 'circular'],
        default='force_directed',
        help='Graph layout algorithm (default: force_directed)'
    )
    parser.add_argument(
        '--theme',
        choices=['dark', 'light', 'blue'],
        default='dark',
        help='Color theme (default: dark)'
    )
    parser.add_argument(
        '--width',
        default='100%%',
        help='Graph width (default: 100%%)'
    )
    parser.add_argument(
        '--height',
        default='1000px',
        help='Graph height (default: 1000px)'
    )

    # Behavior options
    parser.add_argument(
        '--no-open',
        action='store_true',
        help='Do not auto-open visualization in browser'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate schema and show warnings'
    )

    args = parser.parse_args()

    # Validate input
    if not args.stdin and not args.input:
        parser.error("Either provide input file or use --stdin")

    if not args.quiet:
        print_banner()

    # Read input
    try:
        if args.stdin:
            if not args.quiet:
                print("📖 Reading schema from stdin...")
            schema_input = sys.stdin.read()
        else:
            if not args.quiet:
                print(f"📖 Reading schema from: {args.input}")

            if not os.path.exists(args.input):
                print(f"❌ Error: File not found: {args.input}")
                sys.exit(1)

            with open(args.input, 'r', encoding='utf-8') as f:
                schema_input = f.read()

    except Exception as e:
        print(f"❌ Error reading input: {e}")
        sys.exit(1)

    # Parse schema
    if not args.quiet:
        print("🔍 Parsing schema...")

    parser_obj = SchemaParser()
    result = parser_obj.parse(schema_input)

    if not result.get('valid', False):
        print(f"❌ Error: {result.get('error', 'Unknown parsing error')}")
        sys.exit(1)

    nodes = result['nodes']
    edges = result['edges']

    if not args.quiet:
        print(f"✅ Successfully parsed schema")
        stats = parser_obj.get_statistics()
        print_statistics(stats)

    # Validate if requested
    if args.validate and not args.quiet:
        import json
        schema_data = json.loads(schema_input)
        validation = parser_obj.validate_schema(schema_data)

        if validation['errors']:
            print("\n⚠️  Validation Errors:")
            for error in validation['errors']:
                print(f"   - {error}")

        if validation['warnings']:
            print("\n⚠️  Validation Warnings:")
            for warning in validation['warnings']:
                print(f"   - {warning}")

    # Create visualization
    if not args.quiet:
        print(f"\n🎨 Creating visualization...")
        print(f"   Layout: {args.layout}")
        print(f"   Theme: {args.theme}")

    visualizer = SchemaVisualizer(
        layout=args.layout,
        theme=args.theme,
        width=args.width,
        height=args.height
    )

    try:
        output_file = visualizer.create_visualization(
            nodes=nodes,
            edges=edges,
            output_file=args.output,
            auto_open=not args.no_open
        )

        if not args.quiet:
            print(f"✅ Visualization created successfully!")
            print(f"   File: {os.path.abspath(output_file)}")

    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        sys.exit(1)

    # Export JSON if requested
    if args.export_json:
        try:
            visualizer.export_json(nodes, edges, args.export_json)
            if not args.quiet:
                print(f"✅ Graph data exported to: {args.export_json}")
        except Exception as e:
            print(f"❌ Error exporting JSON: {e}")

    if not args.quiet:
        print("\n✨ Done!\n")


if __name__ == "__main__":
    main()
