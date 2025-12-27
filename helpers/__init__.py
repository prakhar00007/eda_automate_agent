"""
helpers package - Collection of helper modules for EDA analysis
Exposes all helper functions for clean imports in main app
"""

# Import from eda_helpers
from helpers.eda_helpers import (
    load_data,
    get_dataset_info,
    get_numerical_stats,
    detect_outliers_iqr,
    create_correlation_heatmap,
    create_histogram,
    create_boxplot,
    create_barplot,
    create_scatterplot
)

# Import from ai_helpers
from helpers.ai_helpers import (
    get_euri_insights
)

# Import from export_helpers
from helpers.export_helpers import (
    generate_html_report,
    generate_word_report,
    download_csv_report,
    create_download_button
)

__all__ = [
    # EDA Functions
    'load_data',
    'get_dataset_info',
    'get_numerical_stats',
    'detect_outliers_iqr',
    'create_correlation_heatmap',
    'create_histogram',
    'create_boxplot',
    'create_barplot',
    'create_scatterplot',
    # AI Functions
    'get_euri_insights',
    # Export Functions
    'generate_html_report',
    'generate_word_report',
    'download_csv_report',
    'create_download_button'
]
