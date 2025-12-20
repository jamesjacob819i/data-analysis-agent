🤖 Autonomous Data Analysis System

## Problem Statement
Organizations struggle to convert data into actionable insights due to dependence on specialized teams, causing delays and missed opportunities.

## Solution
An autonomous council of AI agents that collaboratively analyze data, generate hypotheses, detect issues, and explain findings in simple language—all with minimal human intervention.

## 🏗️ Architecture

### Council of Agents
1. **Data Ingestion Agent** - Validates, cleans, and structures data
2. **Self-Healing Agent** - Automatic detection and fixing of data quality issues
3. **Field Generation Agent** - Creates derived fields on-demand from existing data
4. **Hypothesis Generation Agent** - Discovers testable patterns and relationships
5. **Analysis Agent** - Performs statistical tests and calculations
6. **Visualization Agent** - Autonomously selects optimal chart types
7. **Explanation Agent** - Translates technical findings to plain English

### Self-Healing Capabilities
- Automatic detection of missing values, duplicates, outliers
- **Intelligent data type detection and conversion:**
  - ✅ Auto-detects datetime formats
  - ✅ Recognizes boolean values (true/false, yes/no, 1/0)
  - ✅ Converts integers and floats intelligently
  - ✅ Optimizes categorical data (low-cardinality strings)
  - ✅ Cleans string data (whitespace, special characters)
  - ✅ Handles infinity and extreme values
  - ✅ Self-correcting with multiple validation passes
- Intelligent data cleaning (median/mode imputation)
- Zero-variance column removal
- Anomaly detection using IQR method
- **Multi-iteration self-correction** - Runs up to 3 passes until data is clean

### 🆕 On-Demand Field Generation
The Field Generation Agent can automatically create new variables:
- **Ratios** - Automatically compute ratios between numeric fields
- **Differences** - Calculate differences and deltas
- **Aggregations** - Sum, average, and other statistical aggregations
- **Transformations** - Percent change, moving averages, normalization
- **Advanced** - Cumulative sums, logarithms, squared values
- **Custom** - Specify any derivation type needed

**Key Features:**
- ✨ Auto-suggests derivable fields based on your data
- 📝 Logs all derivation logic clearly
- 🔄 Generated fields instantly available for analysis
- 🤖 Fully autonomous - no manual calculations needed

## 🎯 Key Features

### ✅ Delivered Features
- ✅ **Autonomous Hypothesis Generation** - AI discovers patterns without prompting
- ✅ **Council of Agents** - 7 specialized agents working collaboratively
- ✅ **Self-Healing** - Automatic data quality fixes
- ✅ **On-Demand Field Generation** - Create derived variables automatically
- ✅ **Dynamic Dashboard** - Updates automatically with new fields
- ✅ **Thinking Logs** - Real-time visibility into agent reasoning
- ✅ **Autonomous Visualization** - AI chooses best chart types
- ✅ **Field Comparison Tool** - Compare any two variables dynamically
- ✅ **KPI Cards** - Automatic metric summaries
- ✅ **Stock/Crypto Analysis** - Real-time financial data analysis
- ✅ **Report Analysis** - CSV/Excel file processing
- ✅ **Explainability** - Plain-English insights for non-technical users
- ✅ **Error Awareness** - Proactive issue detection with no silent failures
- ✅ **No External AI Models** - Pure statistical and rule-based intelligence

## 🎨 Visualization Types (Agent-Selected)
- Line charts (time series)
- Bar charts (comparisons)
- Scatter plots (correlations)
- Box plots (distributions)
- Histograms (frequencies)
- Heatmaps (correlation matrices)
- KPI cards (metric summaries)
- Multi-line comparisons
- Distribution overlays
🚀 Quick Start
Installation
bash
# Clone repository
git clone <your-repo>
cd autonomous-analyst

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Configuration
Get your Anthropic API key from console.anthropic.com
Run the application:
bash
streamlit run app.py
Enter API key in sidebar
Choose analysis mode: Stock Analysis or Report Analysis
## 📊 Usage Examples

### Stock Analysis Mode
1. Enter stock symbol (e.g., AAPL, TSLA, BTC-USD)
2. Select time period (1 month to 5 years)
3. Choose features: Price trends, volatility, moving averages, etc.
4. Click "Analyze Stock"
5. View autonomous insights and visualizations

### Report Analysis Mode
1. Upload CSV/Excel file or use sample data
2. System automatically validates and cleans data
3. Select variables to analyze
4. **🆕 Generate derived fields** - Create new variables like ratios, moving averages, etc.
5. Agents generate hypotheses and select visualizations
6. **🆕 Compare any two fields** dynamically
7. View statistical summaries and plain-English insights
8. **🆕 See KPI cards** with key metrics

### 🆕 Field Generation Examples

**Automatic Suggestions:**
- The agent will suggest fields like:
  - `profit_margin` (revenue/cost ratio)
  - `growth_rate` (percent change over time)
  - `moving_average` (smoothed trends)
  - `normalized_score` (0-1 scaled values)

**Custom Field Creation:**
- Name your field (e.g., "efficiency_ratio")
- Select derivation type (ratio, difference, sum, etc.)
- Agent automatically creates it from existing data
- Instantly available for all analysis and visualizations

**What Can Be Generated:**
- ✅ Ratios and percentages
- ✅ Mathematical transformations
- ✅ Rolling/moving statistics
- ✅ Normalized values
- ✅ Cumulative calculations
- ✅ Custom aggregations
🧠 Agent Thinking Process
The Agent Logs tab shows real-time reasoning:
[10:23:45] Data Ingestion Agent
Thought: Starting data validation...
Action: Analyzed 100 rows, 5 columns

[10:23:47] Hypothesis Generation Agent
Thought: Generating testable hypotheses...
Action: ["Sales correlate with seasonality", "Profit margins vary by region"]

[10:23:50] Visualization Agent
Thought: Deciding best chart type for Sales vs Date...
Action: Selected 'line' chart for time series data

[10:23:52] Explanation Agent
Thought: Translating findings to plain English...
Action: "Sales show a 23% increase over the quarter..."
🔧 Self-Healing Examples
Detected Issues
⚠️ Missing values in 'Sales' column (12 rows)
⚠️ 5 duplicate rows found
⚠️ 3 outliers detected in 'Profit'
Applied Fixes
✅ Filled 12 missing values with median ($3,250)
✅ Removed 5 duplicate rows
✅ Capped 3 outliers to valid range
📈 Technical Details
Tech Stack
Frontend: Streamlit (Python)
AI Engine: Claude (Anthropic API)
Data Processing: pandas, numpy
Visualization: Plotly
Financial Data: yfinance
AI Model
Model: claude-sonnet-4-20250514
Purpose: Powers all 5 agents
Reasoning: Long-context understanding, complex analysis
Data Flow
User Input → Data Ingestion Agent → Self-Healing Agent
    ↓
Hypothesis Generation Agent
    ↓
Analysis Agent → Visualization Agent → Explanation Agent
    ↓
Dashboard + Insights
🏆 Hackathon Deliverables
✅ Completed
Source Code - Full Python application with modular agent system
Working Prototype - Deployable Streamlit app
Documentation - README, code comments, usage guide
Agent Logs - Real-time thinking transparency
Self-Healing - Automatic error detection and correction
Autonomous Visualization - AI-driven chart selection
🎥 Demo Highlights
Upload dataset → Automatic hypothesis generation → Autonomous visualization → Plain-English insights
Stock analysis with real-time data
Self-healing in action (before/after data quality)
Agent thinking logs showing collaborative reasoning
🔮 Future Enhancements
 Multi-agent debate for controversial findings
 Automated report generation (PDF/Word)
 Time series forecasting
 Natural language querying ("Show me sales trends")
 Integration with business intelligence tools
👥 Team
[Your Name] - Lead Developer, AI Integration
[Team Members] - Data Processing, UI/UX
📄 License
MIT License - Feel free to use and modify
🙏 Acknowledgments
Anthropic Claude API for powering the agent system
Streamlit for rapid prototyping
yfinance for financial data access

ARCHITECTURE
Frontend (Streamlit - fastest option)
    ↓
Agent Orchestrator (LangChain)
    ↓
Council of Agents:
├── 1. Data Ingestion Agent (cleans, validates)
├── 2. Hypothesis Generation Agent (finds patterns)
├── 3. Analysis Agent (statistical tests)
├── 4. Visualization Agent (picks best charts)
└── 5. Explanation Agent (translates to English)
    ↓
Logging System (shows "agent thinking")
    ↓
Dynamic Dashboard (Plotly)