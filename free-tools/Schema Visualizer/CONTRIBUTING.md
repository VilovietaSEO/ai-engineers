# Contributing to Schema Visualizer

First off, thank you for considering contributing to Schema Visualizer! 🎉

This project is made possible by the amazing [**Vibe Coders**](https://www.skool.com/ai-agent-vibe-engineers) community, and we welcome contributions from developers of all skill levels.

## Code of Conduct

### Our Standards

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Inclusive**: Welcome newcomers and help them learn
- **Be Collaborative**: Share knowledge and work together
- **Be Patient**: Remember that everyone is learning
- **Have Fun**: Building cool stuff should be enjoyable!

## How Can I Contribute?

### 1. Reporting Bugs

Found a bug? Help us fix it!

**Before submitting a bug report:**
- Check if the issue already exists in [Issues](https://github.com/yourusername/schema-visualizer/issues)
- Make sure you're using the latest version
- Test with the example schemas to isolate the problem

**When submitting a bug report, include:**
- Python version (`python --version`)
- Operating system (macOS, Windows, Linux)
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Error messages or screenshots
- Your schema file (if possible)

### 2. Suggesting Features

Have an idea for a new feature?

**Before suggesting a feature:**
- Check if it's already been suggested in [Issues](https://github.com/yourusername/schema-visualizer/issues)
- Make sure it aligns with the project's goals

**When suggesting a feature, include:**
- Clear description of the feature
- Why it would be useful
- How it might work
- Example use cases

### 3. Contributing Code

Ready to write some code? Awesome!

#### Getting Started

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/schema-visualizer.git
cd schema-visualizer

# 3. Create a new branch
git checkout -b feature/my-awesome-feature

# 4. Install dependencies
pip install -r requirements.txt

# 5. Make your changes

# 6. Test your changes
python schema_visualizer.py examples/person_schema.json
```

#### Code Style

- Use **4 spaces** for indentation (not tabs)
- Follow **PEP 8** Python style guide
- Write **clear, descriptive variable names**
- Add **docstrings** to functions and classes
- Keep functions **focused and small**
- Add **comments** for complex logic

Example:
```python
def parse_schema_node(node_data, parent_id=None):
    """
    Parse a single schema node and extract its properties.

    Args:
        node_data (dict): The schema node data to parse
        parent_id (str, optional): ID of the parent node

    Returns:
        dict: Parsed node with id, label, type, and relationships
    """
    # Implementation here
    pass
```

#### Commit Messages

Write clear, descriptive commit messages:

**Good commit messages:**
- ✅ `Add support for Recipe schema type`
- ✅ `Fix node color for Product schema`
- ✅ `Update README with macOS installation steps`

**Bad commit messages:**
- ❌ `Update code`
- ❌ `Fix bug`
- ❌ `Changes`

#### Pull Request Process

1. **Update documentation** if you changed functionality
2. **Add tests** if applicable
3. **Update README.md** if you added features
4. **Test thoroughly** with multiple schema types
5. **Submit your pull request**

**Pull Request Template:**
```markdown
## Description
Brief description of what this PR does

## Changes
- Change 1
- Change 2
- Change 3

## Testing
How did you test these changes?

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #123
```

### 4. Improving Documentation

Documentation is just as important as code!

**Ways to help:**
- Fix typos or unclear explanations
- Add more examples
- Improve installation instructions
- Translate to other languages
- Create video tutorials
- Write blog posts

### 5. Adding Schema Examples

Help others by adding more example schemas!

**Requirements:**
- Valid JSON-LD format
- Common, real-world use case
- Properly formatted
- Test with the visualizer first

**Where to add:**
1. Create your schema file in `examples/`
2. Name it descriptively (e.g., `recipe_schema.json`)
3. Update README.md with the new example
4. Submit a pull request

### 6. Adding Schema Type Support

Want to add support for a new Schema.org type?

**Steps:**
1. Open `schema_visualizer/config.py`
2. Add your schema type to `SCHEMA_COLORS`
3. Choose an appropriate color (check existing colors)
4. Test with a real schema of that type
5. Submit a pull request

Example:
```python
SCHEMA_COLORS = {
    # ... existing types ...
    'Recipe': '#FF6347',  # Tomato red
    'Restaurant': '#FFD700',  # Gold
}
```

## Development Setup

### Prerequisites

- Python 3.7+
- pip
- git

### Local Development

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/schema-visualizer.git
cd schema-visualizer

# Install dependencies
pip install -r requirements.txt

# Make changes and test
python schema_visualizer.py examples/person_schema.json

# Run with different options
python schema_visualizer.py examples/product_schema.json --theme light --layout hierarchical
```

## Project Structure

```
schema-visualizer/
├── schema_visualizer/        # Main package
│   ├── __init__.py          # Package initialization
│   ├── parser.py            # Schema parsing logic
│   ├── visualizer.py        # Visualization generation
│   └── config.py            # Configuration and constants
├── examples/                # Example schema files
│   ├── person_schema.json
│   ├── product_schema.json
│   └── ...
├── schema_visualizer.py     # CLI entry point
├── requirements.txt         # Python dependencies
├── README.md               # Main documentation
├── CONTRIBUTING.md         # This file
└── LICENSE                 # MIT License
```

## Questions?

- Join the discussion on [Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers)
- Open an [Issue](https://github.com/yourusername/schema-visualizer/issues)
- Ask in the community chat

## Recognition

All contributors will be:
- Listed in the project README
- Mentioned in release notes
- Celebrated in the Vibe Coders community

## Thank You!

Every contribution, no matter how small, makes a difference. Thank you for helping make Schema Visualizer better for everyone!

---

**Made with ❤️ by [Vibe Coders](https://www.skool.com/ai-agent-vibe-engineers)**

*Empowering the next generation of AI engineers, one contribution at a time.*
