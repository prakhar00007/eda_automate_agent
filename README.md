# 🔍 Automated EDA + LLM Insights Analyzer

A complete Streamlit application for automated Exploratory Data Analysis (EDA) with AI-powered insights using EURI API.

## 📋 Features

✅ **CSV Upload & Validation**
- Upload CSV files directly
- Preview data (first/last rows)
- Validate file structure

✅ **Automated EDA (Code-based)**
- Dataset shape & dimensions
- Column data types
- Missing values (count & percentage)
- Duplicate row detection
- Descriptive statistics
- Outlier detection (IQR method)
- Correlation heatmap

✅ **Visual Analysis**
- Histograms & KDE plots for numeric columns
- Boxplots for outlier visualization
- Bar charts for categorical columns
- Scatter plots for relationships

✅ **LLM-Powered Insights (EURI API with Streaming)**
- Real-time streaming responses for instant feedback
- Natural language dataset summary
- Data quality issue identification
- Trend & correlation analysis
- Actionable recommendations for cleaning & feature engineering
- Powered by Google Gemini Flash 2.5 for faster responses

## 🌐 Live Demo

**Try the app online:**
👉 [https://eda-automate-agent-prakhar.streamlit.app/](https://eda-automate-agent-prakhar.streamlit.app/)

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Environment Setup
Your `.env` file already contains:
```
EURI_API_KEY="euri-d78735c3a2019f4a408dc5b8b1c91a7af390ad970535b4dffcf24fda928150c5"
```

The app will automatically load this key from `.env` file.

### 3️⃣ Run the App
```bash
streamlit run app.py
```

**Note**: On Windows PowerShell, if you get permission errors, use:
```powershell
python -m streamlit run app.py
```

### 4️⃣ Access the App
After running the command, Streamlit will automatically open your browser at:
```
http://localhost:8501
```

## 📖 How to Use

1. **Upload CSV** - Use the sidebar file uploader to select your CSV file
2. **View Overview** - See dataset summary, missing values, statistics
3. **Visual Analysis** - Explore histograms, boxplots, correlations
4. **Get LLM Insights** - Get AI-powered analysis and recommendations

## 📁 Project Structure
```
eda-analyaser-automate/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # API keys (keep this private!)
└── README.md             # This file
```

## 🛠️ Tech Stack
- **Streamlit** - Web app framework
- **Pandas & NumPy** - Data processing
- **Matplotlib & Seaborn** - Data visualization
- **EURI API** - LLM for insights
- **Python 3.8+** - Language

## ⚙️ Configuration

**EURI API Model** (default: `gemini-2.5-flash`)
- Uses Google's Gemini Flash 2.5 model for fast, accurate insights
- Supports streaming responses for real-time output
- Optimized for data analysis tasks

**LLM Backend**
The app uses EURI API with streaming enabled for real-time response generation. This provides:
- Faster perceived latency (responses appear immediately)
- Word-by-word display as the model generates content
- Improved user experience on slower connections

## 🔒 Security
- ✅ API keys stored in `.env` (never in code)
- ✅ `.env` should be in `.gitignore` before pushing to GitHub
- ✅ Keep your EURI_API_KEY private

## 📝 Example Usage

```bash
# Terminal 1: Start the app
cd c:\Users\PRAKHAR KR SINGH\OneDrive\Desktop\eda-analyaser-automate
pip install -r requirements.txt
streamlit run app.py

# Open http://localhost:8501 in your browser
# Upload a CSV file and explore!
```

## 🐛 Troubleshooting

**Issue**: "Module not found: streamlit"
```bash
pip install -r requirements.txt --upgrade
```

**Issue**: "EURI API key not set"
- Verify `.env` file exists in project root
- Check `.env` contains: `EURI_API_KEY="your_key_here"`

**Issue**: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

**Issue**: Slow LLM response
- Streaming responses may take 3-5 seconds (text appears as it's generated)
- Ensure stable internet connection
- Model: `gemini-2.5-flash` is optimized for speed
- Check EURI API status at api.euron.one

## 🎯 Next Steps (Enhancement Ideas)
- Add downloadable EDA report (PDF/HTML export)
- Cache LLM responses to avoid repeat calls
- Add data cleaning wizard
- Support Excel files (.xlsx)
- Add unit tests for functions

## 📞 Support
If you encounter issues:
1. Check that `.env` file is in the project root directory
2. Verify API key is correct and has access
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
4. Check internet connection for API calls

---
Made with ❤️ for automated data analysis
