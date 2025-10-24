# 🎨 Schema Visualizer - Interactive JSON Graph Generator

<div align="center">

![Schema Visualizer Banner](https://img.shields.io/badge/Schema-Visualizer-6366f1?style=for-the-badge)
![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=for-the-badge&logo=javascript&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Transform Schema.org markup or any JSON data into beautiful, interactive network graphs!**

Built with ❤️ by Rabih Rizk for [**Vibe Coders**](https://www.skool.com/ai-agent-vibe-engineers) - The AI Agent Engineering Community

[Join Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers) · [Report Bug](https://github.com/yourusername/schema-visualizer/issues) · [Request Feature](https://github.com/yourusername/schema-visualizer/issues)

</div>

---

## 📖 Table of Contents

- [What is This?](#-what-is-this)
- [Why Use This Tool?](#-why-use-this-tool)
- [Quick Start (5 Minutes!)](#-quick-start-5-minutes)
- [Step-by-Step Installation](#-step-by-step-installation)
- [How to Use](#-how-to-use)
- [Examples & Screenshots](#-examples--screenshots)
- [All Available Options](#-all-available-options)
- [Troubleshooting](#-troubleshooting)
- [About Vibe Coders](#-about-vibe-coders)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 NEW: Enhanced Web Interface with Dual Mode Support!

**Want to get started instantly?** Simply open `index.html` in your browser - no installation needed!

### ✨ Major Features

#### 🔄 **Dual Visualization Modes**
- **Schema.org Mode** - Specialized for Schema.org JSON-LD markup with type-specific coloring
- **Generic JSON Mode** - Visualize ANY JSON structure (APIs, configs, databases, analytics)
- Easy toggle switch between modes with dynamic examples

#### 🌓 **Dark/Light Theme Support**
- Professional light theme with neutral stone colors
- Rich dark theme with charcoal palette
- Instant theme switching with preference persistence
- Auto-detects system theme preference

#### 🎨 **Beautiful Modern Interface**
- Modern dark slate header design
- Smooth transitions and animations
- Professional color palette (indigo primary colors)
- Responsive layout that works on all screen sizes
- Custom-styled components with proper contrast

#### 📊 **Advanced Features**
- ✅ Paste or upload JSON files directly
- ✅ Real-time statistics and validation
- ✅ Interactive graph visualization (zoom, pan, drag nodes)
- ✅ Export visualizations as PNG images
- ✅ Quick example library (8 examples total - 4 Schema, 4 Generic)
- ✅ Toast notifications for user feedback
- ✅ Keyboard shortcuts (Ctrl/Cmd + Enter to visualize)

[👉 See Web Interface Guide](WEB_INTERFACE.md)

For advanced users who prefer the command line, continue reading below for the CLI tool documentation.

---

## 🎯 What is This?

The **Schema Visualizer** is a versatile tool that transforms both Schema.org structured data (JSON-LD) and **any generic JSON data** into **interactive, beautiful network graphs** that you can explore in your web browser.

Think of it as a "mind map generator" for JSON data - whether it's website structured data, API responses, configuration files, or database exports!

### 🌐 Two Ways to Use

1. **🚀 Web Interface (ENHANCED!)** - Simply open `index.html` in your browser
   - No installation required!
   - **Dual Mode**: Schema.org or Generic JSON visualization
   - Dark/Light theme toggle
   - Paste or upload your data
   - Instant visualization with beautiful modern UI
   - [Learn more about the Web Interface →](WEB_INTERFACE.md)

2. **💻 Command-Line Tool** - Powerful CLI for advanced users
   - Generate visualizations from terminal
   - Batch processing support
   - Multiple output formats
   - Full customization options

### Real-World Use Cases

#### Schema.org Mode
- **SEO Professionals**: Visualize and validate schema markup for clients
- **Web Developers**: Debug complex schema relationships
- **Content Creators**: Understand how different content pieces connect
- **Digital Marketers**: Create visual reports of structured data implementations

#### Generic JSON Mode
- **API Developers**: Visualize complex API response structures
- **DevOps Engineers**: Map configuration files and service dependencies
- **Data Analysts**: Explore nested JSON data from databases
- **WordPress Developers**: Visualize post meta, theme configs, and plugin data
- **E-commerce Teams**: Map order structures, product catalogs, and inventory
- **Marketing Teams**: Visualize analytics data and campaign structures
- **Students & Learners**: Understand JSON data structures visually

---

## 🌟 Why Use This Tool?

✅ **Dual Mode Support** - Schema.org AND Generic JSON visualization
✅ **Zero Configuration** - Works out of the box, no installation needed
✅ **Interactive** - Drag, zoom, and explore your data visually
✅ **Beautiful Themes** - Modern dark/light theme toggle with professional colors
✅ **30+ Schema Types Supported** - Person, Product, Article, LocalBusiness, and more!
✅ **Works with ANY JSON** - API responses, configs, databases, analytics
✅ **Multiple Layouts** - Force-directed, hierarchical, or circular arrangements
✅ **Export Options** - Save as PNG images or JSON for further analysis
✅ **8 Built-in Examples** - Learn from real-world Schema.org and JSON examples
✅ **Theme Persistence** - Remembers your dark/light theme preference
✅ **Keyboard Shortcuts** - Ctrl/Cmd + Enter to visualize quickly
✅ **Beginner Friendly** - Clear error messages and helpful warnings
✅ **Portable** - Self-contained, works anywhere (web browser or Python)

---

## ⚡ Quick Start (5 Minutes!)

Want to get started immediately? Follow these 3 simple steps:

### Step 1: Download or Clone This Repository

```bash
# Option A: Using git (recommended)
git clone https://github.com/yourusername/schema-visualizer.git
cd schema-visualizer

# Option B: Download ZIP
# Click the green "Code" button above → Download ZIP → Extract it
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! Only one dependency needed: `pyvis` 🎉

### Step 3: Try It Out!

```bash
# Run with an example schema
python schema_visualizer.py examples/local_business_schema.json
```

Your browser will automatically open with an interactive visualization! 🎨

---

## 🔧 Step-by-Step Installation

### Prerequisites

Before you begin, make sure you have:

- **Python 3.7 or higher** installed on your computer
  - Check by running: `python --version` or `python3 --version`
  - Don't have Python? [Download it here](https://www.python.org/downloads/)

- **pip** (Python package manager) - Usually comes with Python
  - Check by running: `pip --version` or `pip3 --version`

### Installation Instructions

#### For macOS/Linux Users:

```bash
# 1. Navigate to where you want to install
cd ~/Documents  # or any folder you prefer

# 2. Clone the repository
git clone https://github.com/yourusername/schema-visualizer.git

# 3. Go into the project folder
cd schema-visualizer

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test it works!
python schema_visualizer.py examples/person_schema.json
```

#### For Windows Users:

```cmd
# 1. Navigate to where you want to install
cd C:\Users\YourName\Documents

# 2. Clone the repository
git clone https://github.com/yourusername/schema-visualizer.git

# 3. Go into the project folder
cd schema-visualizer

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test it works!
python schema_visualizer.py examples/person_schema.json
```

#### Without Git (Manual Download):

1. Click the green **"Code"** button at the top of this page
2. Select **"Download ZIP"**
3. Extract the ZIP file to your desired location
4. Open Terminal (Mac/Linux) or Command Prompt (Windows)
5. Navigate to the extracted folder: `cd path/to/schema-visualizer`
6. Run: `pip install -r requirements.txt`
7. Test: `python schema_visualizer.py examples/person_schema.json`

---

## 🚀 How to Use

### Basic Usage

The simplest way to use the visualizer:

```bash
python schema_visualizer.py path/to/your/schema.json
```

This will:
1. Parse your schema file
2. Generate an interactive HTML visualization
3. Automatically open it in your default browser

### Common Use Cases

#### 1. Visualize Your Own Schema File

```bash
python schema_visualizer.py my_schema.json
```

#### 2. Save to a Specific Output File

```bash
python schema_visualizer.py my_schema.json -o my_visualization.html
```

#### 3. Use a Different Layout

```bash
# Hierarchical tree layout (great for nested schemas)
python schema_visualizer.py my_schema.json --layout hierarchical

# Circular layout (good for small schemas)
python schema_visualizer.py my_schema.json --layout circular

# Force-directed layout (default, best for most cases)
python schema_visualizer.py my_schema.json --layout force_directed
```

#### 4. Change the Color Theme

```bash
# Light theme (for presentations)
python schema_visualizer.py my_schema.json --theme light

# Dark theme (default, easy on eyes)
python schema_visualizer.py my_schema.json --theme dark

# Blue theme (professional look)
python schema_visualizer.py my_schema.json --theme blue
```

#### 5. Export Graph Data as JSON

```bash
# Save the graph structure for analysis
python schema_visualizer.py my_schema.json --export-json graph_data.json
```

#### 6. Combine Multiple Options

```bash
python schema_visualizer.py my_schema.json \
  --layout hierarchical \
  --theme light \
  --output business_schema_viz.html \
  --export-json business_graph.json
```

---

## 📸 Examples & Screenshots

### Try These Example Commands

We've included 4 example schemas for you to explore:

#### Example 1: Person Schema
```bash
python schema_visualizer.py examples/person_schema.json --layout hierarchical
```
**What it shows**: A person with their organization and address

#### Example 2: Local Business Schema
```bash
python schema_visualizer.py examples/local_business_schema.json --theme light
```
**What it shows**: A local business with opening hours, ratings, and location

#### Example 3: Product Schema
```bash
python schema_visualizer.py examples/product_schema.json --theme blue
```
**What it shows**: A product with offers, reviews, ratings, and brand info

#### Example 4: Article Schema
```bash
python schema_visualizer.py examples/article_schema.json --layout circular
```
**What it shows**: An article with author and publisher information

### Understanding the Visualization

When you open the generated HTML file, you'll see:

#### Schema.org Mode
**Node Types:**
- 🔴 **Large Colored Nodes** = Schema.org types (@type)
  - Example: Person, Product, Organization
- ⚪ **Small Gray Nodes** = Properties and values
  - Example: name, price, address

**Colors by Schema Type:**
- 🔴 **Red** = Person
- 🔵 **Cyan** = Organization
- 🟢 **Green** = Place/LocalBusiness
- 🟡 **Orange** = Product/Offer
- 🟣 **Purple** = Article/BlogPosting

#### Generic JSON Mode
**Node Types:**
- 🔵 **Blue Nodes** = Objects (larger size)
- 🟠 **Orange Nodes** = Arrays (medium size)
- ⚪ **Gray Nodes** = Primitive values (smaller size)

**Interactions:**
- **Click & Drag** = Move nodes around
- **Scroll** = Zoom in/out
- **Hover** = See node details
- **Click Node** = Highlight its connections
- **Theme Toggle** = Switch between dark/light mode (top-right button)
- **Mode Toggle** = Switch between Schema.org and Generic JSON modes

---

## ⚙️ All Available Options

### Command Syntax

```bash
python schema_visualizer.py [INPUT_FILE] [OPTIONS]
```

### Input Options

| Option | Description | Example |
|--------|-------------|---------|
| `input` | Path to your JSON-LD schema file | `my_schema.json` |
| `--stdin` | Read schema from stdin instead of file | `cat schema.json \| python schema_visualizer.py --stdin` |

### Output Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output HTML file path | `-o output.html` |
| `--export-json` | - | Export graph data as JSON | `--export-json graph.json` |

### Visualization Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--layout` | `force_directed`, `hierarchical`, `circular` | `force_directed` | Graph layout algorithm |
| `--theme` | `dark`, `light`, `blue` | `dark` | Color theme |
| `--width` | Any CSS width | `100%` | Graph width |
| `--height` | Any CSS height | `1000px` | Graph height |

### Behavior Options

| Option | Description |
|--------|-------------|
| `--no-open` | Don't auto-open visualization in browser |
| `--quiet` | Minimal output (suppress progress messages) |
| `--validate` | Validate schema and show warnings |

### Complete Example

```bash
python schema_visualizer.py examples/local_business_schema.json \
  --output visualizations/business.html \
  --export-json data/business_graph.json \
  --layout hierarchical \
  --theme light \
  --width 1200px \
  --height 800px \
  --validate \
  --no-open
```

---

## 🐛 Troubleshooting

### Problem: "File not found" Error

**Solution:**
```bash
# Use absolute paths if needed
python schema_visualizer.py /full/path/to/schema.json

# Or navigate to the folder first
cd /path/to/your/schema/
python /path/to/schema_visualizer.py schema.json
```

### Problem: "Invalid JSON format" Error

**Solution:**
- Verify your JSON-LD is valid JSON using [JSONLint](https://jsonlint.com/)
- Check for missing commas, brackets, or quotes
- Use the `--validate` flag to see detailed errors:
  ```bash
  python schema_visualizer.py my_schema.json --validate
  ```

### Problem: Visualization Doesn't Open Automatically

**Solution:**
```bash
# Use --no-open and manually open the file
python schema_visualizer.py my_schema.json --no-open
# Then open schema_visualization.html in your browser
```

### Problem: "pip: command not found"

**Solution:**
```bash
# Try using pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt
```

### Problem: Empty or Strange Visualization

**Solution:**
- Ensure your schema has `@type` properties
- Use `--validate` to check for schema issues:
  ```bash
  python schema_visualizer.py my_schema.json --validate
  ```
- Try a different layout:
  ```bash
  python schema_visualizer.py my_schema.json --layout hierarchical
  ```

### Problem: Permission Denied

**Solution:**
```bash
# On Mac/Linux, try with sudo
sudo pip install -r requirements.txt

# Or install for your user only
pip install --user -r requirements.txt
```

### Still Having Issues?

1. Check that Python 3.7+ is installed: `python --version`
2. Make sure pyvis is installed: `pip list | grep pyvis`
3. Try running with Python 3 explicitly: `python3 schema_visualizer.py ...`
4. Join [Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers) and ask the community!

---

## 🎓 About Vibe Coders

<div align="center">

### **Vibe Coders - AI Agent Engineering Community**

This tool was created by and for the amazing community at **Vibe Coders**!

🌐 **[Join Vibe Coders on Skool](https://www.skool.com/ai-agent-vibe-engineers)**

</div>

**Who We Are:**

Vibe Coders is a vibrant community of AI enthusiasts, developers, and engineers who are passionate about building intelligent agents and automation tools. We share knowledge, collaborate on projects, and help each other grow in the exciting field of AI engineering.

**What We Do:**

- 🤖 Build AI agents and automation tools
- 📚 Share tutorials and learning resources
- 💡 Collaborate on open-source projects
- 🎯 Help each other solve real-world problems
- 🚀 Stay ahead of AI/ML trends and technologies

**Why Join?**

- ✅ Access to exclusive AI engineering tutorials
- ✅ Weekly challenges and projects
- ✅ Supportive community of builders
- ✅ Direct help from experienced developers
- ✅ Networking with AI professionals
- ✅ Early access to tools like this one!

**Ready to Level Up Your AI Skills?**

👉 **[Join Vibe Coders Today!](https://www.skool.com/ai-agent-vibe-engineers)** 👈

---

## 💻 Using as a Python Library

You can also import and use this tool in your own Python code:

```python
from schema_visualizer import SchemaParser, SchemaVisualizer

# Parse a schema file
parser = SchemaParser()
result = parser.parse("path/to/schema.json")

if result['valid']:
    # Create visualization
    visualizer = SchemaVisualizer(layout="hierarchical", theme="dark")
    visualizer.create_visualization(
        nodes=result['nodes'],
        edges=result['edges'],
        output_file="output.html"
    )

    # Get statistics
    stats = parser.get_statistics()
    print(f"Total nodes: {stats['total_nodes']}")
    print(f"Type nodes: {stats['type_nodes']}")
    print(f"Property nodes: {stats['property_nodes']}")
else:
    print(f"Error: {result['error']}")
```

---

## 🤝 Contributing

We love contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Report Bugs** - Found a problem? [Open an issue](https://github.com/yourusername/schema-visualizer/issues)
2. **Suggest Features** - Have an idea? [Request a feature](https://github.com/yourusername/schema-visualizer/issues)
3. **Improve Documentation** - Help others understand the tool better
4. **Add Schema Types** - Expand support for more Schema.org types
5. **Share Examples** - Submit your own schema examples

### Contribution Process

```bash
# 1. Fork the repository
# 2. Create a new branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# 4. Commit your changes
git commit -m "Add amazing feature"

# 5. Push to your branch
git push origin feature/amazing-feature

# 6. Open a Pull Request
```

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge generously
- Give credit where it's due
- Have fun building cool stuff!

---

## 📊 Supported Schema Types

The visualizer supports **30+ Schema.org types** with smart color coding:

### Common Types
- Person, Organization, Place, LocalBusiness, Event, Product, Offer

### Content Types
- Article, BlogPosting, NewsArticle, WebPage, WebSite

### Creative Works
- Book, Movie, MusicRecording, VideoObject, ImageObject

### Reviews & Ratings
- Review, Rating, AggregateRating

### Actions
- Action, SearchAction

### Structured Values
- PostalAddress, GeoCoordinates, ContactPoint, OpeningHoursSpecification

### Lists & FAQs
- BreadcrumbList, ItemList, ListItem, FAQPage, Question, Answer

### How-To
- HowTo, HowToStep

**Don't see your type?** The visualizer automatically handles unknown types with fallback styling!

---

## 📈 Performance

| Schema Size | Nodes | Processing Time |
|-------------|-------|-----------------|
| Small | < 50 | Instant ⚡ |
| Medium | 50-200 | 1-2 seconds |
| Large | 200-500 | 2-5 seconds |
| Very Large | 500+ | 5-10 seconds |

**Tip:** For very large schemas, use `hierarchical` layout for better performance and readability.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can freely use, modify, and distribute this tool. Just keep the license notice!

---

## 🙏 Acknowledgments

### Built With

- [PyVis](https://pyvis.readthedocs.io/) - Python network visualization library
- [vis.js](https://visjs.org/) - Underlying JavaScript graph library
- [Schema.org](https://schema.org/) - Structured data vocabulary

### Special Thanks

- **Vibe Coders Community** - For inspiration and feedback
- **All Contributors** - For making this tool better
- **You** - For using this tool! 🎉

---

## 📞 Support & Contact

### Need Help?

1. **Check the [Troubleshooting](#-troubleshooting) section** above
2. **Browse existing [Issues](https://github.com/yourusername/schema-visualizer/issues)**
3. **Join [Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers)** and ask the community
4. **Open a new [Issue](https://github.com/yourusername/schema-visualizer/issues/new)** with details

### Stay Connected

- 🌐 [Vibe Coders Community](https://www.skool.com/ai-agent-vibe-engineers)
- 🐛 [Report Issues](https://github.com/yourusername/schema-visualizer/issues)
- 💡 [Request Features](https://github.com/yourusername/schema-visualizer/issues)

---

<div align="center">

### ⭐ If you find this tool helpful, please star the repository! ⭐

**Made with ❤️ by [Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers)**

*Empowering the next generation of AI engineers, one tool at a time.*

[⬆ Back to Top](#-schemaorg-visualizer---interactive-graph-generator)

</div>
