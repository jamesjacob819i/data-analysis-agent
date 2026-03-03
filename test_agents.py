import sys
from unittest.mock import MagicMock
import pandas as pd
import numpy as np

# Mock Streamlit to avoid session_state errors when running as a standalone script
class DummySessionState(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        raise AttributeError(key)
    def __setattr__(self, key, value):
        self[key] = value

st_mock = MagicMock()
st_mock.session_state = DummySessionState()
sys.modules['streamlit'] = st_mock

# Mock yfinance to prevent python 3.9 type hint errors
yf_mock = MagicMock()
# Give it a return value for the .history() method
dummy_stock_df = pd.DataFrame({
    'Close': np.random.normal(150, 5, 60),
    'Volume': np.random.randint(1000000, 5000000, 60),
})
yf_mock.Ticker.return_value.history.return_value = dummy_stock_df
sys.modules['yfinance'] = yf_mock

# Now we can safely import app
import app

def create_sample_df():
    # Create a dataframe with intentional issues for testing
    data = {
        'id': range(1, 101),
        'date': pd.date_range(start='2023-01-01', periods=100).astype(str).tolist(),
        'sales': np.random.normal(1000, 200, 100).tolist(),
        'category': np.random.choice(['A', 'B', 'C', ' '], 100).tolist(),
        'is_active': np.random.choice(['yes', 'no', '1', '0'], 100).tolist(),
        'zero_var': [5] * 100
    }
    
    # Introduce some missing values and outliers
    data['sales'][10] = 999999  # Outlier
    data['sales'][20] = np.nan  # Missing value
    
    # Introduce messy strings
    data['category'][5] = ' A '
    
    df = pd.DataFrame(data)
    
    # Add a duplicate row
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    return df

def test_pipeline():
    logger = app.AgentLogger()
    
    print("\n" + "="*60)
    print("1. DATA INGESTION AGENT")
    print("="*60)
    ingestion_agent = app.DataIngestionAgent(logger)
    df = create_sample_df()
    print(f"Original shape: {df.shape}")
    
    validation_report = ingestion_agent.validate_data(df)
    print(f"Issues detected: {ingestion_agent.issues_detected}")
    
    print("\n" + "="*60)
    print("2. SELF-HEALING AGENT")
    print("="*60)
    healing_agent = app.SelfHealingAgent(logger)
    clean_df = healing_agent.heal_data(df)
    print(f"Cleaned shape: {clean_df.shape}")
    print(f"Fixes applied ({len(healing_agent.fixes_applied)}):")
    for fix in healing_agent.fixes_applied[:5]:
        print(f"  - {fix}")
    if len(healing_agent.fixes_applied) > 5:
        print(f"  - ... ({len(healing_agent.fixes_applied) - 5} more)")
        
    print("\n" + "="*60)
    print("3. FIELD GENERATION AGENT")
    print("="*60)
    field_agent = app.FieldGenerationAgent(logger)
    can_derive, strategy = field_agent.analyze_request(clean_df, "sales_ratio")
    if can_derive:
        clean_df = field_agent.generate_field(clean_df, "sales_ratio", "ratio")
        print(f"Generated field: 'sales_ratio'. New shape: {clean_df.shape}")
        
    print("\n" + "="*60)
    print("4. HYPOTHESIS GENERATION AGENT")
    print("="*60)
    hypothesis_agent = app.HypothesisGenerationAgent(logger)
    hypotheses = hypothesis_agent.generate_hypotheses(clean_df)
    print(f"Generated {len(hypotheses)} hypotheses.")
    for h in hypotheses[:3]:
        print(f"  - Hypothesis: {h['hypothesis']} (Type: {h['type']})")
        
    print("\n" + "="*60)
    print("5. ANALYSIS AGENT")
    print("="*60)
    analysis_agent = app.AnalysisAgent(logger)
    analysis_results = analysis_agent.analyze_data(clean_df, hypotheses)
    print(f"Tested {len(analysis_results['hypothesis_tests'])} hypotheses.")
    if 'sales' in analysis_results['descriptive_stats']:
        stats = analysis_results['descriptive_stats']['sales']
        print(f"Descriptive stats sample (sales): Mean={stats['mean']:.2f}, Std={stats['std']:.2f}, Max={stats['max']:.2f}")
    
    print("\n" + "="*60)
    print("6. VISUALIZATION AGENT")
    print("="*60)
    viz_agent = app.VisualizationAgent(logger)
    visualizations = viz_agent.create_visualizations(clean_df, hypotheses)
    print(f"Created {len(visualizations)} visualizations autonomously.")
    if visualizations:
        for v in visualizations[:2]:
            print(f"  - Chart: {v['chart_type']} | Reasoning: {v.get('reasoning', 'None')}")
            
    print("\n" + "="*60)
    print("7. EXPLANATION AGENT")
    print("="*60)
    explanation_agent = app.ExplanationAgent(logger)
    explanations = explanation_agent.explain_findings(clean_df, hypotheses, analysis_results)
    print(f"Generated {len(explanations)} explanations.")
    if explanations:
        print("\nSample Explanation:")
        print("-" * 40)
        print(explanations[0])
        print("-" * 40)
    
    print("\n" + "="*60)
    print("8. STOCK ANALYSIS AGENT (Optional Extension)")
    print("="*60)
    stock_agent = app.StockAnalysisAgent(logger)
    
    # Test Symbol Search
    print("Testing auto symbol lookup for 'Microsoft'...")
    resolved_sym = stock_agent.search_ticker_symbol("Microsoft")
    print(f"  -> Resolved 'Microsoft' to: {resolved_sym}")
    
    stock_df = stock_agent.fetch_stock_data("AAPL", "1mo")
    if stock_df is not None:
        print(f"Fetched AAPL data: {stock_df.shape}")
        stock_analysis = stock_agent.analyze_stock(stock_df, ["price_trend", "volatility", "moving_averages", "rsi"])
        print("\nStock insights:")
        for insight in stock_analysis['insights']:
            print(f"  - {insight}")
    else:
        print("Failed to fetch stock data (this requires internet connection and yfinance).")
        
    print("\n" + "="*60)
    print("PIPELINE LOGGER AUDIT")
    print("="*60)
    logs = logger.get_logs()
    print(f"Total agent actions logged: {len(logs)}")
    for log in logs[:5]:
        print(f"[{log['timestamp']}] {log['agent']}: {log['action']} ({log['thought']})")
    print("...\n")

if __name__ == "__main__":
    test_pipeline()
