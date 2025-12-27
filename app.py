import pandas as pd
import numpy as np
import os
import streamlit as st
import base64
from datetime import datetime
from dotenv import load_dotenv

# Import helper functions
from helpers import (
    load_data, get_dataset_info, get_numerical_stats, detect_outliers_iqr,
    create_correlation_heatmap, create_histogram, create_boxplot, create_barplot, create_scatterplot,
    get_euri_insights, generate_html_report, generate_word_report, download_csv_report
)

# Load environment variables from .env file
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Automated EDA with AI",
    page_icon="bar_chart",
    layout="wide"
)

# Configure EURI API
EURI_API_KEY = os.getenv("EURI_API_KEY")
if not EURI_API_KEY:
    st.error("Please set EURI_API_KEY environment variable")

def main():
    st.title("Automated Exploratory Data Analysis")
    st.markdown("Upload a CSV file to perform comprehensive data analysis with AI-powered insights")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    sections = ["Upload Data", "Dataset Overview", "Data Quality", "Statistical Analysis",
               "Visualizations", "AI Insights", "Recommendations", "Export Report"]
    choice = st.sidebar.radio("Go to", sections)

    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
        st.session_state.info = None

    # File upload section (always visible)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=['csv'])
    st.sidebar.info("Tip: Maximum file size is 50MB")

    if uploaded_file is not None:
        if st.sidebar.button("Load Data"):
            with st.spinner("Loading data..."):
                df = load_data(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.info = get_dataset_info(df)
                    st.sidebar.success(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")

    # Main content based on navigation
    if choice == "Upload Data":
        st.header("Upload Your Dataset")
        st.markdown("""
        **Instructions:**
        1. Click on the file uploader in the sidebar
        2. Select a CSV file from your computer
        3. Click "Load Data" to process the file
        4. Navigate through different sections using the sidebar menu
        
        **Supported Formats:** CSV files with UTF-8, Latin1, or CP1252 encoding
        
        **File Size Limit:** 50 MB maximum
        """)

        if st.session_state.df is not None:
            st.success("Data loaded successfully!")
            st.markdown(f"**Dataset Shape:** {st.session_state.info['shape'][0]} rows × {st.session_state.info['shape'][1]} columns")
        else:
            st.info("Please upload a CSV file to get started")

    elif st.session_state.df is None:
        st.warning("Please upload a CSV file first")

    else:
        df = st.session_state.df
        info = st.session_state.info

        if choice == "Dataset Overview":
            st.header("Dataset Overview")
            st.info("This section shows basic information about your dataset including shape, data types, and a preview of the data.")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Basic Information")
                st.metric("Rows", info['shape'][0])
                st.metric("Columns", info['shape'][1])
                st.metric("Duplicate Rows", info['duplicates'])
                st.metric("Memory Usage", f"{info['memory_usage']:.2f} MB")

            with col2:
                st.subheader("Data Types")
                dtypes_df = pd.DataFrame(list(info['dtypes'].items()),
                                       columns=['Column', 'Data Type'])
                st.dataframe(dtypes_df, use_container_width=True)

            st.subheader("Data Preview")
            st.dataframe(df.head(10), use_container_width=True)

            st.subheader("Column Names")
            st.write(list(df.columns))

        elif choice == "Data Quality":
            st.header("Data Quality Analysis")
            st.info("Analyze missing values, duplicates, and outliers in your dataset.")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Missing Values")
                missing_df = pd.DataFrame({
                    'Column': list(info['missing_values'].keys()),
                    'Missing Count': list(info['missing_values'].values()),
                    'Missing %': list(info['missing_percentage'].values())
                })
                missing_df = missing_df[missing_df['Missing Count'] > 0]
                if not missing_df.empty:
                    st.dataframe(missing_df, use_container_width=True)
                else:
                    st.success("✅ No missing values found!")

            with col2:
                st.subheader("Duplicate Analysis")
                st.metric("Duplicate Rows", info['duplicates'])
                if info['duplicates'] > 0:
                    st.warning(f"Found {info['duplicates']} duplicate rows")
                else:
                    st.success("✅ No duplicate rows found!")

            # Outlier detection for numerical columns
            st.subheader("Outlier Detection (IQR Method)")
            numerical_cols = df.select_dtypes(include=[np.number]).columns

            if len(numerical_cols) > 0:
                outlier_data = []
                for col in numerical_cols:
                    outlier_count, lower, upper = detect_outliers_iqr(df, col)
                    if outlier_count > 0:
                        outlier_data.append({
                            'Column': col,
                            'Outliers': outlier_count,
                            'Lower Bound': round(lower, 2),
                            'Upper Bound': round(upper, 2)
                        })

                if outlier_data:
                    outlier_df = pd.DataFrame(outlier_data)
                    st.dataframe(outlier_df, use_container_width=True)
                else:
                    st.success("✅ No outliers detected in numerical columns!")
            else:
                st.info("No numerical columns for outlier detection")

        elif choice == "Statistical Analysis":
            st.header("Statistical Analysis")
            st.info("View descriptive statistics and correlation analysis for numerical columns.")

            numerical_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols = df.select_dtypes(include=['object']).columns

            if len(numerical_cols) > 0:
                st.subheader("Numerical Columns Statistics")
                stats_df = get_numerical_stats(df)
                st.dataframe(stats_df, use_container_width=True)

                # Correlation heatmap
                st.subheader("Correlation Analysis")
                heatmap_fig = create_correlation_heatmap(df)
                if heatmap_fig:
                    st.pyplot(heatmap_fig)
                else:
                    st.info("Need at least 2 numerical columns for correlation analysis")
            else:
                st.info("No numerical columns found")

            if len(categorical_cols) > 0:
                st.subheader("Categorical Columns Summary")
                cat_summary = []
                for col in categorical_cols:
                    unique_count = df[col].nunique()
                    most_common = df[col].mode().iloc[0] if not df[col].mode().empty else "N/A"
                    cat_summary.append({
                        'Column': col,
                        'Unique Values': unique_count,
                        'Most Common': most_common
                    })

                cat_df = pd.DataFrame(cat_summary)
                st.dataframe(cat_df, use_container_width=True)

        elif choice == "Visualizations":
            st.header("Data Visualizations")
            st.info("Explore distributions and relationships in your data through interactive visualizations.")

            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

            # Numerical visualizations
            if numerical_cols:
                st.subheader("Numerical Columns")

                col1, col2 = st.columns(2)
                with col1:
                    selected_num_col = st.selectbox("Select column for histogram",
                                                  numerical_cols, key="hist")
                    if selected_num_col:
                        hist_fig = create_histogram(df, selected_num_col)
                        st.pyplot(hist_fig)

                with col2:
                    selected_box_col = st.selectbox("Select column for boxplot",
                                                   numerical_cols, key="box")
                    if selected_box_col:
                        box_fig = create_boxplot(df, selected_box_col)
                        st.pyplot(box_fig)

                # Scatter plot
                if len(numerical_cols) >= 2:
                    st.subheader("Relationships between Numerical Variables")
                    col3, col4 = st.columns(2)
                    with col3:
                        x_col = st.selectbox("X-axis", numerical_cols, key="scatter_x")
                    with col4:
                        y_col = st.selectbox("Y-axis", numerical_cols, key="scatter_y")

                    if x_col and y_col and x_col != y_col:
                        scatter_fig = create_scatterplot(df, x_col, y_col)
                        st.pyplot(scatter_fig)

            # Categorical visualizations
            if categorical_cols:
                st.subheader("Categorical Columns")
                selected_cat_col = st.selectbox("Select categorical column",
                                              categorical_cols, key="bar")
                if selected_cat_col:
                    bar_fig = create_barplot(df, selected_cat_col)
                    st.pyplot(bar_fig)

        elif choice == "AI Insights":
            st.header("AI-Powered Insights")
            st.info("Generate AI-powered analysis and insights about your dataset using EURI API.")

            if not EURI_API_KEY:
                st.error("EURI API key not configured. Please set EURI_API_KEY environment variable.")
            else:
                with st.spinner("Generating AI insights..."):
                    summary = get_euri_insights(df, info, "summary", EURI_API_KEY)
                    quality = get_euri_insights(df, info, "data_quality", EURI_API_KEY)
                    insights = get_euri_insights(df, info, "insights", EURI_API_KEY)

                tab1, tab2, tab3 = st.tabs(["📝 Dataset Summary", "🔍 Data Quality", "💡 Key Insights"])

                with tab1:
                    st.markdown(summary)

                with tab2:
                    st.markdown(quality)

                with tab3:
                    st.markdown(insights)

        elif choice == "Recommendations":
            st.header("AI Recommendations")
            st.info("Get AI-powered recommendations for data preprocessing, feature engineering, and modeling.")

            if not EURI_API_KEY:
                st.error("EURI API key not configured. Please set EURI_API_KEY environment variable.")
            else:
                with st.spinner("Generating recommendations..."):
                    recommendations = get_euri_insights(df, info, "recommendations", EURI_API_KEY)

                st.markdown(recommendations)
        
        elif choice == "Export Report":
            st.header("Export EDA Report")
            st.info("Generate and download a comprehensive report of your exploratory data analysis.")
            
            if df is not None:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Generate HTML Report"):
                        with st.spinner("Generating HTML report..."):
                            html_report = generate_html_report(df, info)
                            st.success("HTML report generated successfully!")
                            
                            # Create download button
                            b64 = base64.b64encode(html_report.encode()).decode()
                            href = f'<a href="data:text/html;base64,{b64}" download="EDA_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html">Download HTML Report</a>'
                            st.markdown(href, unsafe_allow_html=True)
                
                with col2:
                    if st.button("Generate Word Report"):
                        with st.spinner("Generating Word document..."):
                            doc = generate_word_report(df, info)
                            if doc:
                                st.success("Word report generated successfully!")
                                
                                # Get bytes from document
                                from io import BytesIO
                                doc_bytes = BytesIO()
                                doc.save(doc_bytes)
                                doc_bytes.seek(0)
                                word_content = doc_bytes.getvalue()
                                
                                # Create download button
                                b64 = base64.b64encode(word_content).decode()
                                href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="EDA_Report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.docx">Download Word Report</a>'
                                st.markdown(href, unsafe_allow_html=True)
                
                with col3:
                    if st.button("Export Data Summary as CSV"):
                        # Create summary CSV
                        summary_data = {
                            'Metric': ['Total Rows', 'Total Columns', 'Duplicate Rows', 'Memory Usage (MB)'],
                            'Value': [info['shape'][0], info['shape'][1], info['duplicates'], f"{info['memory_usage']:.2f}"]
                        }
                        summary_df = pd.DataFrame(summary_data)
                        csv = summary_df.to_csv(index=False)
                        
                        st.success("CSV summary generated successfully!")
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="EDA_Summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv">Download Summary CSV</a>'
                        st.markdown(href, unsafe_allow_html=True)
            else:
                st.warning("Please upload a CSV file first to generate reports.")

if __name__ == "__main__":
    main()