"""
Schema Visualizer - A tool for visualizing Schema.org markup as interactive graphs
"""

__version__ = "1.0.0"
__author__ = "MapPackSEO Toolbox"

from .parser import SchemaParser
from .visualizer import SchemaVisualizer
from .config import VisualizerConfig

__all__ = ['SchemaParser', 'SchemaVisualizer', 'VisualizerConfig']
