# 🌐 Schema Visualizer - Web Interface

## Overview

The Schema Visualizer now includes a beautiful, modern web interface that allows you to visualize Schema.org markup directly in your browser without using the command line!

## Features

✨ **Beautiful Modern UI**
- Stunning gradient design with dark theme
- Smooth animations and transitions
- Responsive layout for all screen sizes

🎯 **Easy to Use**
- Simply paste your JSON-LD schema markup
- Upload JSON files directly
- Click "Visualize" to see your schema as an interactive graph

📊 **Rich Details**
- Real-time statistics (node counts, edges, etc.)
- Schema validation with warnings and errors
- Interactive node information on click

🎨 **Interactive Visualization**
- Drag nodes to rearrange
- Zoom in/out with mouse wheel
- Pan by dragging the background
- Export visualization as PNG image

⚡ **Quick Examples**
- Pre-loaded examples for Person, Product, Local Business, and Article schemas
- One-click to load and visualize

## How to Use

### Method 1: Open Directly in Browser

1. Simply open `index.html` in any modern web browser
2. Paste your Schema.org JSON-LD markup in the text area
3. Click "Visualize" button
4. Explore your schema graph!

### Method 2: Use a Local Server (Recommended for Examples)

If you want to use the example loading feature, run a local server:

```bash
# Using Python 3
python3 -m http.server 8000

# Or using Python 2
python -m SimpleHTTPServer 8000

# Then open in browser
# http://localhost:8000
```

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter` - Visualize the current schema

## UI Elements

### Input Panel (Left Side)
- **Schema Input**: Large text area for pasting JSON-LD
- **Visualize Button**: Process and display your schema
- **Clear Button**: Reset the input and visualization
- **Upload JSON**: Load schema from a file
- **Quick Examples**: Pre-loaded example schemas

### Visualization Panel (Right Side)
- **Interactive Graph**: The main visualization area
- **Fit Button**: Auto-fit the graph to screen
- **Reset Button**: Reset the graph layout
- **Export Button**: Download visualization as PNG

### Details Panel
- **Statistics**: Shows node counts and relationships
- **Validation Messages**: Errors and warnings about your schema
- **Status Messages**: Success/error notifications

## Color Coding

The visualization uses color-coding to help identify different Schema.org types:

- 🔴 **Red** (#E74C3C) - Person
- 🔵 **Blue** (#45B7D1) - Organization, default types
- 🟢 **Green** (#76D7C4) - Place, LocalBusiness, GeoCoordinates
- 🟠 **Orange** (#D35400) - Product, AggregateRating
- 🟣 **Purple** (#9B59B6) - Article, Review
- ⚪ **Gray** (#BDC3C7) - Properties and values

Larger nodes = Schema.org types (@type)
Smaller nodes = Properties and values

## Browser Compatibility

Works best in modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Powered by Vibe Quarters

This tool is built with ❤️ by the [Vibe Quarters](https://www.skool.com/ai-agent-vibe-engineers) community - The AI Agent Engineering Community.

Join us to learn, build, and collaborate on AI projects!

## Example Usage

### Example 1: Paste JSON-LD

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Jane Doe",
  "jobTitle": "Software Engineer",
  "telephone": "+1-555-123-4567",
  "url": "https://janedoe.com"
}
```

1. Copy the above JSON
2. Paste into the text area
3. Click "Visualize"
4. See the interactive graph!

### Example 2: Upload a File

1. Click "Upload JSON" button
2. Select your `.json` or `.jsonld` file
3. Click "Visualize"
4. Explore your schema!

### Example 3: Try Quick Examples

1. Click any example button (Person, Product, etc.)
2. The schema will auto-load and visualize
3. Explore the example to understand Schema.org structure

## Troubleshooting

**Q: Examples don't load?**
A: Make sure you're running a local server (see "Method 2" above) or the examples are in the correct folder.

**Q: Visualization is too crowded?**
A: Use the mouse wheel to zoom out, or click the "Fit" button to auto-fit to screen.

**Q: Can't see all nodes?**
A: Try dragging nodes around or using the "Reset" button to recalculate the layout.

**Q: Invalid JSON error?**
A: Check your JSON syntax using a tool like [JSONLint](https://jsonlint.com/)

## Technical Details

- **Frontend**: Pure HTML, CSS, JavaScript
- **Visualization Library**: vis.js (Network module)
- **No Backend Required**: Runs entirely in the browser
- **No External Dependencies**: All libraries loaded from CDN

## CLI Tool Still Available

The original Python CLI tool is still available and fully functional:

```bash
python schema_visualizer.py input.json
```

See [README.md](README.md) for CLI documentation.

---

**Made with ❤️ by [Vibe Quarters](https://www.skool.com/ai-agent-vibe-engineers)**
