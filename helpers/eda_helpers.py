"""
eda_helpers.py - Exploratory Data Analysis helper functions
Contains data loading, analysis, and visualization functions
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import StringIO


# ================== DATA LOADING ==================

def load_data(uploaded_file):
    """Load CSV data with error handling and validation"""
    try:
        # Check file size (max 50MB)
        if uploaded_file.size > 50 * 1024 * 1024:
            st.error("File too large. Maximum size is 50MB.")
            return None
            
        # Read CSV with multiple encoding attempts
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                string_data = StringIO(uploaded_file.getvalue().decode(encoding))
                df = pd.read_csv(string_data)
                
                # Validate dataframe is not empty
                if df.empty:
                    st.error("CSV file is empty. Please upload a file with data.")
                    return None
                    
                if len(df.columns) == 0:
                    st.error("CSV file has no columns. Please check your file format.")
                    return None
                    
                return df
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("Could not decode file with any encoding")
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None


# ================== DATA ANALYSIS ==================

def get_dataset_info(df):
    """Get basic dataset information"""
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
    }
    return info


def get_numerical_stats(df):
    """Get descriptive statistics for numerical columns"""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 0:
        return df[numerical_cols].describe().round(2)
    return None


def detect_outliers_iqr(df, column):
    """Detect outliers using IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return len(outliers), lower_bound, upper_bound


# ================== VISUALIZATIONS ==================

def create_correlation_heatmap(df):
    """Create correlation heatmap for numerical columns"""
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) > 1:
        fig, ax = plt.subplots(figsize=(10, 8))
        corr_matrix = df[numerical_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm',
                   fmt='.2f', ax=ax, cbar_kws={'shrink': 0.8})
        ax.set_title('Correlation Heatmap', fontsize=16, pad=20)
        plt.tight_layout()
        return fig
    return None


def create_histogram(df, column):
    """Create histogram for numerical column"""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(data=df, x=column, kde=True, ax=ax)
    ax.set_title(f'Distribution of {column}', fontsize=14)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    return fig


def create_boxplot(df, column):
    """Create boxplot for numerical column"""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(data=df, y=column, ax=ax)
    ax.set_title(f'Boxplot of {column}', fontsize=14)
    ax.set_ylabel(column)
    plt.tight_layout()
    return fig


def create_barplot(df, column):
    """Create bar chart for categorical column"""
    fig, ax = plt.subplots(figsize=(10, 6))
    value_counts = df[column].value_counts().head(20)  # Top 20 categories
    sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
    ax.set_title(f'Distribution of {column}', fontsize=14)
    ax.set_xlabel(column)
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def create_scatterplot(df, col1, col2):
    """Create scatter plot for two numerical columns"""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x=col1, y=col2, ax=ax, alpha=0.6)
    ax.set_title(f'{col1} vs {col2}', fontsize=14)
    ax.set_xlabel(col1)
    ax.set_ylabel(col2)
    plt.tight_layout()
    return fig
