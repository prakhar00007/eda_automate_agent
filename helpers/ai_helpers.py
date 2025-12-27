"""
ai_helpers.py - AI and LLM helper functions
Contains functions for EURI API integration and AI-powered insights with streaming support
"""

import requests
import streamlit as st
import pandas as pd
import numpy as np
import json
from helpers.eda_helpers import get_numerical_stats


def get_euri_insights(df, dataset_info, analysis_type, euri_api_key):
    """Get AI insights from EURI API with streaming support"""
    if not euri_api_key:
        return "EURI API key not configured"

    try:
        if analysis_type == "summary":
            prompt = f"""
            Analyze this dataset and provide a comprehensive summary in plain English:

            Dataset Information:
            - Shape: {dataset_info['shape']} rows, {dataset_info['shape'][1]} columns
            - Columns: {', '.join(dataset_info['columns'])}
            - Data types: {dataset_info['dtypes']}
            - Missing values: {sum(dataset_info['missing_values'].values())} total
            - Duplicate rows: {dataset_info['duplicates']}

            Sample data (first 5 rows):
            {df.head().to_string()}

            Please provide:
            1. Overall description of the dataset
            2. Key characteristics of the data
            3. Potential use cases or domain
            """

        elif analysis_type == "data_quality":
            prompt = f"""
            Analyze data quality issues in this dataset:

            Dataset Information:
            - Shape: {dataset_info['shape']}
            - Missing values by column: {dataset_info['missing_values']}
            - Missing percentages: {dataset_info['missing_percentage']}
            - Duplicate rows: {dataset_info['duplicates']}

            Numerical columns descriptive stats:
            {get_numerical_stats(df).to_string() if get_numerical_stats(df) is not None else 'No numerical columns'}

            Please identify:
            1. Data quality issues (missing values, duplicates, etc.)
            2. Potential data integrity problems
            3. Recommendations for data cleaning
            """

        elif analysis_type == "insights":
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            corr_info = ""
            if len(numerical_cols) > 1:
                corr_matrix = df[numerical_cols].corr()
                strong_corr = []
                for i in range(len(numerical_cols)):
                    for j in range(i+1, len(numerical_cols)):
                        corr_val = corr_matrix.iloc[i, j]
                        if abs(corr_val) > 0.5:
                            strong_corr.append(f"{numerical_cols[i]} and {numerical_cols[j]}: {corr_val:.2f}")
                corr_info = "Strong correlations: " + ", ".join(strong_corr) if strong_corr else "No strong correlations found"

            prompt = f"""
            Provide insights and analysis of this dataset:

            Dataset Overview:
            - {dataset_info['shape'][0]} rows, {dataset_info['shape'][1]} columns
            - Numerical columns: {len(df.select_dtypes(include=[np.number]).columns)}
            - Categorical columns: {len(df.select_dtypes(include=['object']).columns)}

            Correlation Analysis:
            {corr_info}

            Sample data:
            {df.head().to_string()}

            Please provide:
            1. Key trends and patterns in the data
            2. Important correlations and relationships
            3. Notable outliers or unusual patterns
            4. Business insights or observations
            """

        elif analysis_type == "recommendations":
            prompt = f"""
            Based on this dataset analysis, provide recommendations for next steps:

            Dataset Info:
            - Shape: {dataset_info['shape']}
            - Missing data: {sum(dataset_info['missing_values'].values())} total missing values
            - Duplicates: {dataset_info['duplicates']} duplicate rows

            Column types: {dataset_info['dtypes']}

            Please suggest:
            1. Data preprocessing steps needed
            2. Feature engineering opportunities
            3. Potential modeling approaches
            4. Additional analysis that would be valuable
            """

        url = "https://api.euron.one/api/v1/euri/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {euri_api_key}"
        }
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "gemini-2.5-flash",
            "stream": True
        }

        # Use streaming response
        response = requests.post(url, json=payload, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        # Create a container for streaming output
        output_container = st.empty()
        full_response = ""
        
        # Process streaming response
        for line in response.iter_lines():
            if line:
                try:
                    # Handle SSE format (data: {json})
                    line_str = line.decode('utf-8') if isinstance(line, bytes) else line
                    if line_str.startswith('data: '):
                        json_str = line_str[6:]  # Remove 'data: ' prefix
                        if json_str.strip():
                            data = json.loads(json_str)
                            if 'choices' in data and len(data['choices']) > 0:
                                choice = data['choices'][0]
                                if 'delta' in choice and 'content' in choice['delta']:
                                    chunk = choice['delta']['content']
                                    full_response += chunk
                                    output_container.markdown(full_response)
                except (json.JSONDecodeError, KeyError, AttributeError):
                    continue
        
        return full_response if full_response else "Unable to generate insights from EURI API"

    except requests.exceptions.RequestException as e:
        return f"Error calling EURI API: {str(e)}"
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"
