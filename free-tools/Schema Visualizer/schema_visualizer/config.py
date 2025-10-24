"""
Configuration and color schemes for schema visualization
"""

class VisualizerConfig:
    """Configuration class for schema visualizer"""

    # Extended color map for Schema.org types
    SCHEMA_TYPE_COLORS = {
        # Common types
        "Person": {"color": "#FF6B6B", "size": 20},
        "Organization": {"color": "#4ECDC4", "size": 20},
        "Place": {"color": "#95E1D3", "size": 18},
        "LocalBusiness": {"color": "#45B7D1", "size": 18},
        "Event": {"color": "#F38181", "size": 18},
        "Product": {"color": "#FFA07A", "size": 18},
        "Offer": {"color": "#FFD700", "size": 15},

        # Content types
        "Article": {"color": "#9B59B6", "size": 18},
        "BlogPosting": {"color": "#8E44AD", "size": 18},
        "NewsArticle": {"color": "#7D3C98", "size": 18},
        "WebPage": {"color": "#BB8FCE", "size": 16},
        "WebSite": {"color": "#D2B4DE", "size": 16},

        # Creative works
        "Book": {"color": "#3498DB", "size": 16},
        "Movie": {"color": "#2980B9", "size": 16},
        "MusicRecording": {"color": "#5DADE2", "size": 16},
        "VideoObject": {"color": "#85C1E2", "size": 16},
        "ImageObject": {"color": "#AED6F1", "size": 14},

        # Reviews and ratings
        "Review": {"color": "#F39C12", "size": 15},
        "Rating": {"color": "#E67E22", "size": 12},
        "AggregateRating": {"color": "#D35400", "size": 15},

        # Actions
        "Action": {"color": "#16A085", "size": 14},
        "SearchAction": {"color": "#1ABC9C", "size": 14},

        # Structured values
        "PostalAddress": {"color": "#7FB3D5", "size": 12},
        "GeoCoordinates": {"color": "#76D7C4", "size": 12},
        "ContactPoint": {"color": "#73C6B6", "size": 12},
        "OpeningHoursSpecification": {"color": "#A9DFBF", "size": 12},

        # Other types
        "BreadcrumbList": {"color": "#F8B739", "size": 16},
        "ItemList": {"color": "#EB984E", "size": 16},
        "ListItem": {"color": "#DC7633", "size": 14},
        "FAQPage": {"color": "#AF7AC5", "size": 18},
        "Question": {"color": "#BB8FCE", "size": 14},
        "Answer": {"color": "#D2B4DE", "size": 14},
        "HowTo": {"color": "#48C9B0", "size": 18},
        "HowToStep": {"color": "#76D7C4", "size": 14},

        # Fallbacks
        "property": {"color": "#BDC3C7", "size": 10},
        "type": {"color": "#E74C3C", "size": 15},
    }

    # Layout options for PyVis
    LAYOUTS = {
        "force_directed": {
            "physics": True,
            "solver": "barnesHut",
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 95,
                "springConstant": 0.04,
                "damping": 0.09,
                "avoidOverlap": 0.1
            }
        },
        "hierarchical": {
            "physics": False,
            "hierarchical": {
                "enabled": True,
                "levelSeparation": 150,
                "nodeSpacing": 100,
                "treeSpacing": 200,
                "blockShifting": True,
                "edgeMinimization": True,
                "parentCentralization": True,
                "direction": "UD",  # Up-Down
                "sortMethod": "directed"
            }
        },
        "circular": {
            "physics": False,
            "layout": {
                "randomSeed": 2,
                "improvedLayout": True
            }
        }
    }

    # Theme options
    THEMES = {
        "dark": {
            "bgcolor": "#222222",
            "font_color": "white",
            "edge_color": "white"
        },
        "light": {
            "bgcolor": "#FFFFFF",
            "font_color": "black",
            "edge_color": "#999999"
        },
        "blue": {
            "bgcolor": "#0A1929",
            "font_color": "#B2BAC2",
            "edge_color": "#3E5060"
        }
    }

    # Default settings
    DEFAULT_LAYOUT = "force_directed"
    DEFAULT_THEME = "dark"
    DEFAULT_WIDTH = "100%"
    DEFAULT_HEIGHT = "1000px"

    @classmethod
    def get_node_style(cls, node_type):
        """Get color and size for a given node type"""
        # Try exact match first
        if node_type in cls.SCHEMA_TYPE_COLORS:
            return cls.SCHEMA_TYPE_COLORS[node_type]

        # Try to extract base type (e.g., "Person_path" -> "Person")
        base_type = node_type.split('_')[0] if '_' in node_type else node_type
        if base_type in cls.SCHEMA_TYPE_COLORS:
            return cls.SCHEMA_TYPE_COLORS[base_type]

        # Return default for types
        return cls.SCHEMA_TYPE_COLORS.get("type", {"color": "#E74C3C", "size": 15})

    @classmethod
    def get_property_style(cls):
        """Get style for property nodes"""
        return cls.SCHEMA_TYPE_COLORS["property"]
