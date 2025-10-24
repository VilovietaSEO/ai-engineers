#!/bin/bash

# Schema Visualizer - Automated Installation Script
# Made by Vibe Coders - https://www.skool.com/ai-agent-vibe-engineers

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║     Schema Visualizer - Installation Script              ║"
echo "║     Vibe Coders Community                                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
echo "🔍 Checking for Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    echo "✅ Python 3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    echo "✅ Python found: $(python --version)"
else
    echo "❌ Error: Python is not installed!"
    echo "   Please install Python 3.7 or higher from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
echo ""
echo "🔍 Checking Python version..."
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Error: Python 3.7 or higher is required!"
    echo "   You have Python $PYTHON_VERSION"
    echo "   Please upgrade from https://www.python.org/downloads/"
    exit 1
else
    echo "✅ Python version $PYTHON_VERSION is compatible"
fi

# Check if pip is installed
echo ""
echo "🔍 Checking for pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    echo "✅ pip3 found"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    echo "✅ pip found"
else
    echo "❌ Error: pip is not installed!"
    echo "   pip usually comes with Python. Try reinstalling Python."
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
echo "   This may take a minute..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Error: Failed to install dependencies"
    echo "   Try running: $PIP_CMD install --user -r requirements.txt"
    exit 1
fi

# Test the installation
echo ""
echo "🧪 Testing installation..."
if $PYTHON_CMD -c "import pyvis" 2>/dev/null; then
    echo "✅ Installation test passed!"
else
    echo "❌ Error: pyvis module not found"
    echo "   Try running: $PIP_CMD install --user pyvis"
    exit 1
fi

# Run example
echo ""
echo "🎨 Running example visualization..."
echo "   This will create and open an interactive graph..."
echo ""
$PYTHON_CMD schema_visualizer.py examples/person_schema.json

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  ✨ Installation Complete! ✨                             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 You're ready to visualize schemas!"
echo ""
echo "Try these commands:"
echo "  $PYTHON_CMD schema_visualizer.py examples/local_business_schema.json"
echo "  $PYTHON_CMD schema_visualizer.py examples/product_schema.json --theme blue"
echo "  $PYTHON_CMD schema_visualizer.py examples/article_schema.json --layout hierarchical"
echo ""
echo "📖 For more help, see README.md"
echo "💬 Join Vibe Coders: https://www.skool.com/ai-agent-vibe-engineers"
echo ""
