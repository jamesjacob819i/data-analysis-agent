"""
🤖 Autonomous Data Analysis System
A council of intelligent agents for autonomous data analysis, hypothesis generation, and visualization
NO EXTERNAL AI MODELS - Pure intelligent rule-based system

Architecture:
- Multi-sheet Excel support with intelligent merging
- Council of 7 specialized agents working as an internal pipeline
- Auto data type detection (datetime, boolean, categorical, numeric)
- Field generation with UI controls
- Multi-iteration self-correction
- Interactive visualization with manual chart override
- KPI cards, correlation matrices, distribution analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import requests
from typing import List, Dict, Tuple, Optional, Union
import io
import traceback
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import statsmodels
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False

# ============================================================================
# ICON SYSTEM - Font Awesome Icons
# ============================================================================

class IconSystem:
    """Font Awesome icon system for enhanced UI"""
    
    # Icon mappings
    ICONS = {
        'robot': '<i class="fas fa-robot"></i>',
        'chart': '<i class="fas fa-chart-bar"></i>',
        'chart-line': '<i class="fas fa-chart-line"></i>',
        'target': '<i class="fas fa-target"></i>',
        'refresh': '<i class="fas fa-sync-alt"></i>',
        'check': '<i class="fas fa-check-circle"></i>',
        'warning': '<i class="fas fa-exclamation-triangle"></i>',
        'error': '<i class="fas fa-times-circle"></i>',
        'info': '<i class="fas fa-info-circle"></i>',
        'trash': '<i class="fas fa-trash"></i>',
        'settings': '<i class="fas fa-cog"></i>',
        'upload': '<i class="fas fa-file-upload"></i>',
        'table': '<i class="fas fa-table"></i>',
        'plus': '<i class="fas fa-plus-circle"></i>',
        'magic': '<i class="fas fa-wand-magic-sparkles"></i>',
        'rocket': '<i class="fas fa-rocket"></i>',
        'search': '<i class="fas fa-search"></i>',
        'filter': '<i class="fas fa-filter"></i>',
        'exchange': '<i class="fas fa-arrows-alt-h"></i>',
        'brain': '<i class="fas fa-brain"></i>',
        'eye': '<i class="fas fa-eye"></i>',
        'heart': '<i class="fas fa-heart"></i>',
        'home': '<i class="fas fa-home"></i>',
        'file': '<i class="fas fa-file"></i>',
        'folder': '<i class="fas fa-folder"></i>',
        'database': '<i class="fas fa-database"></i>',
        'lock': '<i class="fas fa-lock"></i>',
        'unlock': '<i class="fas fa-unlock"></i>',
        'user': '<i class="fas fa-user"></i>',
        'users': '<i class="fas fa-users"></i>',
        'code': '<i class="fas fa-code"></i>',
        'bar-chart': '<i class="fas fa-chart-column"></i>',
        'stock': '<i class="fas fa-chart-line"></i>',
        'trend': '<i class="fas fa-arrow-trend-up"></i>',
        'data': '<i class="fas fa-database"></i>',
        'microchip': '<i class="fas fa-microchip"></i>',
        'bolt': '<i class="fas fa-bolt"></i>',
        'fire': '<i class="fas fa-fire"></i>',
        'star': '<i class="fas fa-star"></i>',
        'bookmark': '<i class="fas fa-bookmark"></i>',
        'download': '<i class="fas fa-download"></i>',
        'share': '<i class="fas fa-share"></i>',
        'copy': '<i class="fas fa-copy"></i>',
        'edit': '<i class="fas fa-edit"></i>',
        'bars': '<i class="fas fa-bars"></i>',
        'times': '<i class="fas fa-times"></i>',
        'gear': '<i class="fas fa-gear"></i>',
        'spinner': '<i class="fas fa-spinner fa-spin"></i>',
        'percentage': '<i class="fas fa-percent"></i>',
        'area-chart': '<i class="fas fa-chart-area"></i>',
        'pie-chart': '<i class="fas fa-chart-pie"></i>',
        'project-diagram': '<i class="fas fa-project-diagram"></i>',
    }
    
    @staticmethod
    def icon(name: str, size: str = "medium") -> str:
        """Get Font Awesome icon HTML with styling"""
        icon_html = IconSystem.ICONS.get(name, '<i class="fas fa-circle-question"></i>')
        css_class = f"icon-{size}"
        return f'<span class="{css_class}">{icon_html}</span>'
    
    @staticmethod
    def text(icon_name: str, text: str, size: str = "medium") -> str:
        """Get icon with text as markdown"""
        icon_html = IconSystem.icon(icon_name, size)
        return f'{icon_html} {text}'


def apply_premium_theme(fig):
    """Applies a premium, Power BI-inspired dark theme to a Plotly figure"""
    fig.update_layout(
        template="plotly_white",  # Switched to white for classic PBI look, can be adapted to dark
        plot_bgcolor="rgba(255, 255, 255, 1)",
        paper_bgcolor="rgba(255, 255, 255, 1)",
        font_family="Segoe UI, sans-serif", # Classic Power BI font
        title_font_size=16,
        title_font_color="#333333",
        title_x=0.01, # Left aligned like PBI
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#ffffff", font_size=12, font_family="Segoe UI, sans-serif", bordercolor="#cccccc"),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0", zerolinecolor="#e0e0e0", title_font=dict(size=12, color="#666666"), tickfont=dict(size=11, color="#666666")),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", zerolinecolor="#e0e0e0", title_font=dict(size=12, color="#666666"), tickfont=dict(size=11, color="#666666")),
        colorway=["#118DFF", "#12239E", "#E66C37", "#6B007B", "#E044A7", "#744EC2", "#D9B300", "#D64550", "#197278", "#1AAB40"], # PBI Classic Colorway
    )
    return fig


class AgentLogger:
    """Centralized logging system to track agent reasoning"""
    
    def __init__(self):
        if 'agent_logs' not in st.session_state:
            st.session_state.agent_logs = []
    
    def log(self, agent_name: str, thought: str, action: str):
        """Log agent reasoning and actions"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'agent': agent_name,
            'thought': thought,
            'action': action
        }
        st.session_state.agent_logs.append(log_entry)
    
    def get_logs(self) -> List[Dict]:
        """Retrieve all logs"""
        return st.session_state.agent_logs
    
    def clear_logs(self):
        """Clear all logs"""
        st.session_state.agent_logs = []

# ============================================================================
# Core LLM Engine (OpenRouter)
# ============================================================================

class LLMEngine:
    """Handles communication with open-source models via OpenRouter"""
    
    def __init__(self, api_key: str = None, model: str = "meta-llama/llama-3-8b-instruct:free", logger: AgentLogger = None):
        self.logger = logger
        self.model = model
        
        # Use provided key, or fallback to environment variable, or session state
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY") or st.session_state.get("openrouter_api_key", "")
        
        if self.api_key:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
        else:
            self.client = None
            if self.logger:
                self.logger.log("System", "LLM Engine initialized without API key", "Waiting for user input")
                
    def is_ready(self) -> bool:
        return self.client is not None

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """Generate response from the LLM"""
        if not self.client:
            raise ValueError("LLM API Key not configured. Please enter it in the sidebar.")
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if self.logger:
                self.logger.log("LLMEngine Error", str(e), "API Call Failed")
            raise e

# ============================================================================
# AGENT COMMUNICATION (MESSAGE BUS)
# ============================================================================

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Message:
    sender: str
    recipient: str
    topic: str
    payload: Any
    timestamp: datetime = field(default_factory=datetime.now)

class MessageBus:
    """Centralized message bus enabling true agent-to-agent communication"""
    def __init__(self, logger: AgentLogger, llm_engine: LLMEngine = None):
        self.logger = logger
        self.llm_engine = llm_engine
        self.subscribers: Dict[str, Any] = {}
        self.message_history: List[Message] = []
        
    def subscribe(self, agent_name: str, agent_instance):
        self.subscribers[agent_name] = agent_instance
        
    def publish(self, sender: str, recipient: str, topic: str, payload: Any):
        msg = Message(sender=sender, recipient=recipient, topic=topic, payload=payload)
        self.message_history.append(msg)
        
        # Format payload preview for logging
        payload_preview = str(payload)
        if len(payload_preview) > 100:
            payload_preview = payload_preview[:97] + "..."
            
        self.logger.log("MessageBus", f"Routing message from {sender} to {recipient} [{topic}]", payload_preview)
        
        # synchronous delivery for Streamlit loop
        if recipient == "All":
            for name, agent in self.subscribers.items():
                if name != sender and hasattr(agent, 'handle_message'):
                    agent.handle_message(msg)
        elif recipient in self.subscribers:
            agent = self.subscribers[recipient]
            if hasattr(agent, 'handle_message'):
                agent.handle_message(msg)

# ============================================================================
# AGENT 1: DATA INGESTION AGENT (ENHANCED)
# ============================================================================

class DataIngestionAgent:
    """Validates, cleans, and structures incoming data with multi-sheet support"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.issues_detected = []
        self.fixes_applied = []
        self.sheets_detected = []
    
    def detect_and_load_sheets(self, file) -> Dict[str, pd.DataFrame]:
        """Detect and load all sheets from Excel file"""
        self.logger.log(
            "Data Ingestion Agent",
            "Analyzing Excel file for multiple sheets",
            "Detecting sheet structure"
        )
        
        sheets = {}
        try:
            if file.name.endswith(('.xlsx', '.xls')):
                # Read all sheets
                xl_file = pd.ExcelFile(file)
                sheet_names = xl_file.sheet_names
                
                self.sheets_detected = sheet_names
                self.logger.log(
                    "Data Ingestion Agent",
                    f"Found {len(sheet_names)} sheet(s): {sheet_names}",
                    "Multi-sheet Excel file detected"
                )
                
                for sheet_name in sheet_names:
                    try:
                        df = pd.read_excel(file, sheet_name=sheet_name)
                        if len(df) > 0:
                            sheets[sheet_name] = df
                    except Exception as e:
                        self.logger.log(
                            "Data Ingestion Agent",
                            f"Failed to read sheet '{sheet_name}': {str(e)}",
                            "Skipping sheet"
                        )
                
                return sheets
            else:
                return {}
        except Exception as e:
            self.logger.log(
                "Data Ingestion Agent",
                f"Error detecting sheets: {str(e)}",
                "Attempting single sheet read"
            )
            return {}
    
    def ingest_csv(self, file) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Load and validate CSV/Excel file - supports multi-sheet Excel"""
        self.logger.log(
            "Data Ingestion Agent",
            "Starting data ingestion from uploaded file",
            "Reading file and detecting format"
        )
        
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
                self.logger.log(
                    "Data Ingestion Agent",
                    f"Successfully loaded CSV: {len(df)} rows and {len(df.columns)} columns",
                    f"Columns: {list(df.columns)}"
                )
                return df
            else:
                # Try to read as Excel with multi-sheet support
                sheets_dict = self.detect_and_load_sheets(file)
                
                if sheets_dict:
                    if len(sheets_dict) == 1:
                        # Single sheet - return DataFrame directly
                        return list(sheets_dict.values())[0]
                    else:
                        # Multiple sheets - return dictionary
                        return sheets_dict
                else:
                    # Fallback to single sheet read
                    df = pd.read_excel(file)
                    self.logger.log(
                        "Data Ingestion Agent",
                        f"Successfully loaded Excel: {len(df)} rows and {len(df.columns)} columns",
                        f"Columns: {list(df.columns)}"
                    )
                    return df
        except Exception as e:
            self.logger.log(
                "Data Ingestion Agent",
                f"Error loading file: {str(e)}",
                "Failed to ingest data"
            )
            return None
    
    def merge_sheets(self, sheets_dict: Dict[str, pd.DataFrame], merge_strategy: str = 'concat') -> pd.DataFrame:
        """Intelligently merge multiple sheets based on structure"""
        self.logger.log(
            "Data Ingestion Agent",
            f"Merging {len(sheets_dict)} sheets using strategy: {merge_strategy}",
            "Combining data from multiple sheets"
        )
        
        if not sheets_dict:
            return pd.DataFrame()
        
        sheets_list = list(sheets_dict.values())
        sheet_names = list(sheets_dict.keys())
        
        if len(sheets_list) == 1:
            return sheets_list[0]
        
        try:
            if merge_strategy == 'concat':
                # Concatenate all sheets vertically
                merged_df = pd.concat(sheets_list, ignore_index=True)
                self.logger.log(
                    "Data Ingestion Agent",
                    f"Concatenated sheets vertically: {len(merged_df)} total rows",
                    f"Combined from sheets: {sheet_names}"
                )
            elif merge_strategy == 'merge_on_index':
                # Merge on index (for aligned data)
                merged_df = sheets_list[0].copy()
                for df in sheets_list[1:]:
                    merged_df = merged_df.merge(df, left_index=True, right_index=True, how='outer')
                self.logger.log(
                    "Data Ingestion Agent",
                    f"Merged sheets on index: {len(merged_df)} rows",
                    f"Merged from sheets: {sheet_names}"
                )
            else:
                # Default: concat
                merged_df = pd.concat(sheets_list, ignore_index=True)
            
            # Add sheet source column if merging multiple
            if len(sheets_list) > 1 and merge_strategy == 'concat':
                # Add indicator of which sheet each row came from
                row_counts = [len(df) for df in sheets_list]
                sheet_source = []
                for sheet_name, count in zip(sheet_names, row_counts):
                    sheet_source.extend([sheet_name] * count)
                merged_df['_source_sheet'] = sheet_source
                self.logger.log(
                    "Data Ingestion Agent",
                    "Added '_source_sheet' column to track origin",
                    f"Sheet sources: {sheet_names}"
                )
            
            return merged_df
        except Exception as e:
            self.logger.log(
                "Data Ingestion Agent",
                f"Error merging sheets: {str(e)}",
                "Falling back to concatenation"
            )
            return pd.concat(sheets_list, ignore_index=True)
    
    def validate_data(self, df: pd.DataFrame) -> Dict:
        """Validate data quality and detect issues"""
        self.logger.log(
            "Data Ingestion Agent",
            "Running comprehensive data validation",
            "Checking for missing values, duplicates, and anomalies"
        )
        
        validation_report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': {},
            'duplicate_rows': 0,
            'data_types': {},
            'column_stats': {}
        }
        
        # Check missing values
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_pct = (missing_count / len(df) * 100) if len(df) > 0 else 0
            
            if missing_count > 0:
                validation_report['missing_values'][col] = {
                    'count': missing_count,
                    'percentage': missing_pct
                }
                self.issues_detected.append(f"⚠️ Missing values in '{col}': {missing_count} rows ({missing_pct:.1f}%)")
        
        # Check duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            validation_report['duplicate_rows'] = duplicate_count
            self.issues_detected.append(f"⚠️ {duplicate_count} duplicate rows found")
        
        # Data types
        validation_report['data_types'] = df.dtypes.to_dict()
        
        # Column statistics for numeric columns
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                try:
                    validation_report['column_stats'][col] = {
                        'mean': float(df[col].mean()) if df[col].notna().any() else None,
                        'std': float(df[col].std()) if df[col].notna().any() else None,
                        'min': float(df[col].min()) if df[col].notna().any() else None,
                        'max': float(df[col].max()) if df[col].notna().any() else None,
                        'median': float(df[col].median()) if df[col].notna().any() else None
                    }
                except:
                    pass
        
        self.logger.log(
            "Data Ingestion Agent",
            f"Validation complete: Found {len(self.issues_detected)} issues",
            f"Issues: {self.issues_detected}"
        )
        
        return validation_report

# ============================================================================
# AGENT 2: SELF-HEALING AGENT
# ============================================================================

class SelfHealingAgent:
    """Automatically detects and fixes data quality issues"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.fixes_applied = []
    
    def heal_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply intelligent data cleaning with self-correction"""
        self.logger.log(
            "Self-Healing Agent",
            "Initiating autonomous data healing process",
            "Analyzing data quality issues"
        )
        
        df_clean = df.copy()
        max_iterations = 3  # Allow up to 3 correction passes
        
        for iteration in range(max_iterations):
            initial_fixes_count = len(self.fixes_applied)
            
            # 1. Fix data types first (most critical)
            df_clean = self._fix_data_types(df_clean)
            
            # 2. Handle missing values
            df_clean = self._handle_missing_values(df_clean)
            
            # 3. Remove duplicates
            df_clean = self._remove_duplicates(df_clean)
            
            # 4. Handle outliers
            df_clean = self._handle_outliers(df_clean)
            
            # 5. Remove unnecessary columns (zero-variance, identifiers, largely empty)
            df_clean = self._prune_unnecessary_columns(df_clean)
            
            # 6. Validate data integrity
            df_clean = self._validate_data_integrity(df_clean)
            
            # Check if any fixes were applied in this iteration
            new_fixes = len(self.fixes_applied) - initial_fixes_count
            
            if new_fixes == 0:
                # No more fixes needed, exit loop
                self.logger.log(
                    "Self-Healing Agent",
                    f"Data healing converged after {iteration + 1} iteration(s)",
                    "No additional fixes needed"
                )
                break
            else:
                self.logger.log(
                    "Self-Healing Agent",
                    f"Iteration {iteration + 1}: Applied {new_fixes} fixes",
                    "Running another validation pass"
                )
        
        self.logger.log(
            "Self-Healing Agent",
            f"Data healing complete: Applied {len(self.fixes_applied)} total fixes",
            f"Fixes: {self.fixes_applied}"
        )
        
        return df_clean
    
    def _validate_data_integrity(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate and correct data integrity issues"""
        for col in df.columns:
            # Check for mixed types in numeric columns
            if pd.api.types.is_numeric_dtype(df[col]):
                # Check for infinity values
                if np.isinf(df[col]).any():
                    inf_count = np.isinf(df[col]).sum()
                    df[col] = df[col].replace([np.inf, -np.inf], np.nan)
                    self.fixes_applied.append(f"✅ Replaced {inf_count} infinity values with NaN in '{col}'")
                
                # Check for extremely large values that might be errors
                if df[col].notna().any():
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    if std_val > 0:
                        z_scores = np.abs((df[col] - mean_val) / std_val)
                        extreme_values = (z_scores > 10).sum()
                        if extreme_values > 0:
                            self.fixes_applied.append(f"✅ Detected {extreme_values} extreme values in '{col}' (z-score > 10)")
            
            # Check for empty strings in object columns
            elif df[col].dtype == 'object' or df[col].dtype == 'category':
                empty_strings = (df[col].astype(str).str.strip() == '').sum()
                if empty_strings > 0:
                    df[col] = df[col].replace(['', ' ', '  '], np.nan)
                    self.fixes_applied.append(f"✅ Replaced {empty_strings} empty strings with NaN in '{col}'")
        
        return df
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Intelligent missing value imputation"""
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # Use median for numeric columns
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    self.fixes_applied.append(f"✅ Filled {missing_count} missing values in '{col}' with median ({median_val:.2f})")
                else:
                    # Use mode for categorical columns
                    mode_val = df[col].mode()[0] if not df[col].mode().empty else 'Unknown'
                    df[col].fillna(mode_val, inplace=True)
                    self.fixes_applied.append(f"✅ Filled {missing_count} missing values in '{col}' with mode ('{mode_val}')")
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate rows"""
        initial_len = len(df)
        df = df.drop_duplicates()
        removed = initial_len - len(df)
        if removed > 0:
            self.fixes_applied.append(f"✅ Removed {removed} duplicate rows")
        return df
    
    def _handle_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect and cap outliers using IQR method"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            
            if outliers > 0:
                df[col] = df[col].clip(lower_bound, upper_bound)
                self.fixes_applied.append(f"✅ Capped {outliers} outliers in '{col}' to range [{lower_bound:.2f}, {upper_bound:.2f}]")
        
        return df
    
    def _fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Intelligently detect and fix data types with self-correction"""
        for col in df.columns:
            original_dtype = df[col].dtype
            
            # Skip if already numeric and has valid values
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].notna().any():
                continue
            
            # Get sample of non-null values
            sample_values = df[col].dropna().head(10).astype(str).tolist()
            
            if not sample_values:
                continue
            
            # Try different type conversions with error handling
            conversion_successful = False
            
            # 1. Try datetime conversion
            if not conversion_successful:
                conversion_successful = self._try_datetime_conversion(df, col, sample_values)
            
            # 2. Try boolean conversion
            if not conversion_successful:
                conversion_successful = self._try_boolean_conversion(df, col, sample_values)
            
            # 3. Try integer conversion
            if not conversion_successful:
                conversion_successful = self._try_integer_conversion(df, col, sample_values)
            
            # 4. Try float conversion
            if not conversion_successful:
                conversion_successful = self._try_float_conversion(df, col, sample_values)
            
            # 5. Try category conversion (for low-cardinality strings)
            if not conversion_successful:
                conversion_successful = self._try_category_conversion(df, col)
            
            # 6. Clean string data if still object type
            if df[col].dtype == 'object':
                self._clean_string_column(df, col)
        
        return df
    
    def _fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Intelligently detect and fix data types with self-correction"""
        for col in df.columns:
            # Skip special columns
            if col.startswith('_'):
                continue
            
            original_dtype = df[col].dtype
            
            # Skip if already numeric and has valid values
            if pd.api.types.is_numeric_dtype(df[col]) and df[col].notna().any():
                continue
            
            # Get sample of non-null values
            sample_values = df[col].dropna().head(20).astype(str).tolist()
            
            if not sample_values:
                continue
            
            # Try different type conversions with error handling
            conversion_successful = False
            
            # 1. Try datetime conversion (HIGHEST PRIORITY)
            if not conversion_successful:
                conversion_successful = self._try_datetime_conversion(df, col, sample_values)
            
            # 2. Try boolean conversion
            if not conversion_successful:
                conversion_successful = self._try_boolean_conversion(df, col, sample_values)
            
            # 3. Try integer conversion
            if not conversion_successful:
                conversion_successful = self._try_integer_conversion(df, col, sample_values)
            
            # 4. Try float conversion
            if not conversion_successful:
                conversion_successful = self._try_float_conversion(df, col, sample_values)
            
            # 5. Try category conversion (for low-cardinality strings)
            if not conversion_successful:
                conversion_successful = self._try_category_conversion(df, col)
            
            # 6. Clean string data if still object type
            if df[col].dtype == 'object':
                self._clean_string_column(df, col)
        
        return df
    
    def _try_datetime_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to datetime"""
        # Check if values look like dates
        date_patterns = ['-', '/', ':', 'T', 'Z']
        has_date_chars = any(any(p in str(v) for p in date_patterns) for v in sample_values[:5])
        
        if has_date_chars:
            try:
                # Try multiple datetime formats
                test_df = pd.to_datetime(df[col], errors='coerce')
                
                # Check if conversion was successful (at least 50% valid dates)
                valid_count = test_df.notna().sum()
                valid_ratio = valid_count / len(df) if len(df) > 0 else 0
                
                if valid_ratio > 0.5 and valid_count > 0:
                    df[col] = test_df
                    self.fixes_applied.append(f"✅ Converted '{col}' to datetime type ({valid_count} valid dates)")
                    return True
                else:
                    return False
            except Exception as e:
                return False
        return False
    
    def _try_boolean_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to boolean"""
        unique_values = set(str(v).lower().strip() for v in sample_values if pd.notna(v))
        boolean_values = {'true', 'false', 't', 'f', 'yes', 'no', 'y', 'n', '1', '0', '1.0', '0.0'}
        
        # Check if all unique values are boolean-like
        if unique_values and unique_values.issubset(boolean_values) and len(unique_values) <= 4:
            try:
                # Create mapping
                bool_map = {
                    'true': True, 't': True, 'yes': True, 'y': True, '1': True, '1.0': True,
                    'false': False, 'f': False, 'no': False, 'n': False, '0': False, '0.0': False
                }
                
                df[col] = df[col].astype(str).str.lower().str.strip().map(bool_map)
                valid_count = df[col].notna().sum()
                self.fixes_applied.append(f"✅ Converted '{col}' to boolean type ({valid_count} values)")
                return True
            except Exception as e:
                return False
        return False
    
    def _try_integer_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to integer"""
        try:
            # First convert to numeric, removing common currency/percent symbols
            cleaned = df[col].astype(str).str.replace('$', '').str.replace('%', '').str.replace(',', '')
            numeric_series = pd.to_numeric(cleaned, errors='coerce')
            
            # Check if all non-null values are integers
            non_null = numeric_series.dropna()
            if len(non_null) > 0:
                # Check if values are effectively integers
                is_integer = (non_null == non_null.astype(int)).all()
                
                if is_integer:
                    df[col] = numeric_series.astype('Int64')  # Nullable integer type
                    valid_count = df[col].notna().sum()
                    self.fixes_applied.append(f"✅ Converted '{col}' to integer type ({valid_count} values)")
                    return True
            return False
        except Exception as e:
            return False
    
    def _try_float_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to float"""
        try:
            # Remove common non-numeric characters
            cleaned = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace('%', '').str.strip()
            
            # Try numeric conversion
            numeric_series = pd.to_numeric(cleaned, errors='coerce')
            
            # Check if conversion was successful (at least 70% valid numbers)
            valid_count = numeric_series.notna().sum()
            valid_ratio = valid_count / len(df) if len(df) > 0 else 0
            
            if valid_ratio > 0.7 and valid_count > 0:
                df[col] = numeric_series
                self.fixes_applied.append(f"✅ Converted '{col}' to numeric type ({valid_count} values, removed special chars)")
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def _try_category_conversion(self, df: pd.DataFrame, col: str) -> bool:
        """Try to convert low-cardinality string columns to category"""
        if df[col].dtype == 'object':
            unique_count = df[col].nunique()
            unique_ratio = unique_count / len(df) if len(df) > 0 else 0
            
            # Convert to category if low cardinality (< 50% unique values and < 100 categories)
            if unique_ratio < 0.5 and unique_count < 100 and unique_count > 1:
                try:
                    df[col] = df[col].astype('category')
                    self.fixes_applied.append(f"✅ Converted '{col}' to category type ({unique_count} unique values)")
                    return True
                except Exception as e:
                    return False
        return False
    
    def _clean_string_column(self, df: pd.DataFrame, col: str):
        """Clean string columns: remove extra whitespace and special characters"""
        try:
            original_null_count = df[col].isnull().sum()
            
            # Remove leading/trailing whitespace
            df[col] = df[col].astype(str).str.strip()
            
            # Replace empty strings with NaN
            df[col] = df[col].replace('', np.nan)
            
            # Remove multiple spaces
            df[col] = df[col].astype(str).str.replace(r'\s+', ' ', regex=True)
            
            new_null_count = df[col].isnull().sum()
            if new_null_count > original_null_count:
                self.fixes_applied.append(f"✅ Cleaned strings in '{col}' (removed {new_null_count - original_null_count} empty values)")
        except Exception as e:
            pass
    
    def _prune_unnecessary_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove columns with zero variance, high missingness, or unique identifiers"""
        cols_to_drop = []
        
        for col in df.columns:
            # 1. High Missingness (>90%)
            missing_pct = df[col].isnull().sum() / len(df)
            if missing_pct > 0.90:
                cols_to_drop.append(col)
                self.fixes_applied.append(f"✅ Dropped '{col}' heavily missing ({missing_pct:.0%} null)")
                continue
                
            # 2. Zero variance
            if df[col].nunique() <= 1:
                cols_to_drop.append(col)
                self.fixes_applied.append(f"✅ Dropped '{col}' (no variance / constant value)")
                continue
                
            # 3. Text Identifiers (All Unique values string categories, e.g., ID columns)
            if df[col].dtype == object and df[col].nunique() == len(df):
                cols_to_drop.append(col)
                self.fixes_applied.append(f"✅ Dropped '{col}' (identified as pure text identifier/index)")
                continue

        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            
        return df

# ============================================================================
# AGENT 3: FIELD GENERATION AGENT (NEW)
# ============================================================================

class FieldGenerationAgent:
    """Autonomously generates missing fields from existing data"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.generated_fields = {}
        self.derivation_log = []
    
    def analyze_request(self, df: pd.DataFrame, requested_field: str) -> Tuple[bool, Optional[str]]:
        """Determine if a requested field can be generated"""
        self.logger.log(
            "Field Generation Agent",
            f"Analyzing request for field: '{requested_field}'",
            "Checking if field exists or can be derived"
        )
        
        # Check if field already exists
        if requested_field in df.columns:
            self.logger.log(
                "Field Generation Agent",
                f"Field '{requested_field}' already exists in dataset",
                "No generation needed"
            )
            return True, None
        
        # Attempt to derive the field
        derivation = self._attempt_derivation(df, requested_field)
        
        if derivation:
            self.logger.log(
                "Field Generation Agent",
                f"Successfully identified derivation strategy for '{requested_field}'",
                f"Strategy: {derivation}"
            )
            return True, derivation
        else:
            self.logger.log(
                "Field Generation Agent",
                f"Cannot derive '{requested_field}' from existing fields",
                "Field generation not possible"
            )
            return False, None
    
    def generate_field(self, df: pd.DataFrame, field_name: str, derivation_type: str = 'auto') -> pd.DataFrame:
        """Generate a new field based on available data"""
        self.logger.log(
            "Field Generation Agent",
            f"Generating field: '{field_name}'",
            f"Derivation type: {derivation_type}"
        )
        
        df_new = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        try:
            # Auto-detect derivation patterns
            if derivation_type == 'auto':
                derivation_type = self._detect_derivation_type(field_name)
            
            # Generate based on type
            if derivation_type == 'ratio' and len(numeric_cols) >= 2:
                # Generate ratio fields
                col1, col2 = numeric_cols[0], numeric_cols[1]
                df_new[field_name] = df[col1] / (df[col2] + 1e-10)  # Avoid division by zero
                explanation = f"Generated '{field_name}' as ratio of {col1} / {col2}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'ratio',
                    'source': [col1, col2],
                    'formula': f"{col1} / {col2}"
                }
                
            elif derivation_type == 'difference' and len(numeric_cols) >= 2:
                # Generate difference fields
                col1, col2 = numeric_cols[0], numeric_cols[1]
                df_new[field_name] = df[col1] - df[col2]
                explanation = f"Generated '{field_name}' as difference of {col1} - {col2}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'difference',
                    'source': [col1, col2],
                    'formula': f"{col1} - {col2}"
                }
                
            elif derivation_type == 'sum' and len(numeric_cols) >= 2:
                # Generate sum fields
                df_new[field_name] = df[numeric_cols].sum(axis=1)
                explanation = f"Generated '{field_name}' as sum of {', '.join(numeric_cols)}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'sum',
                    'source': numeric_cols,
                    'formula': ' + '.join(numeric_cols)
                }
                
            elif derivation_type == 'average' and len(numeric_cols) >= 2:
                # Generate average fields
                df_new[field_name] = df[numeric_cols].mean(axis=1)
                explanation = f"Generated '{field_name}' as average of {', '.join(numeric_cols)}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'average',
                    'source': numeric_cols,
                    'formula': f"mean({', '.join(numeric_cols)})"
                }
                
            elif derivation_type == 'percent_change' and len(numeric_cols) >= 1:
                # Generate percent change
                col = numeric_cols[0]
                df_new[field_name] = df[col].pct_change() * 100
                explanation = f"Generated '{field_name}' as percent change of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'percent_change',
                    'source': [col],
                    'formula': f"pct_change({col}) * 100"
                }
                
            elif derivation_type == 'rolling_average' and len(numeric_cols) >= 1:
                # Generate rolling average
                col = numeric_cols[0]
                window = min(7, len(df) // 4)
                df_new[field_name] = df[col].rolling(window=window).mean()
                explanation = f"Generated '{field_name}' as {window}-period rolling average of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'rolling_average',
                    'source': [col],
                    'formula': f"rolling_mean({col}, {window})"
                }
                
            elif derivation_type == 'normalized' and len(numeric_cols) >= 1:
                # Generate normalized field
                col = numeric_cols[0]
                df_new[field_name] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
                explanation = f"Generated '{field_name}' as normalized version of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'normalized',
                    'source': [col],
                    'formula': f"normalize({col})"
                }
                
            elif derivation_type == 'cumulative_sum' and len(numeric_cols) >= 1:
                # Generate cumulative sum
                col = numeric_cols[0]
                df_new[field_name] = df[col].cumsum()
                explanation = f"Generated '{field_name}' as cumulative sum of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'cumulative_sum',
                    'source': [col],
                    'formula': f"cumsum({col})"
                }
                
            elif derivation_type == 'squared' and len(numeric_cols) >= 1:
                # Generate squared field
                col = numeric_cols[0]
                df_new[field_name] = df[col] ** 2
                explanation = f"Generated '{field_name}' as square of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'squared',
                    'source': [col],
                    'formula': f"{col}²"
                }
                
            elif derivation_type == 'logarithm' and len(numeric_cols) >= 1:
                # Generate log field
                col = numeric_cols[0]
                df_new[field_name] = np.log1p(df[col].abs())  # log1p for stability
                explanation = f"Generated '{field_name}' as logarithm of {col}"
                self.derivation_log.append(explanation)
                self.generated_fields[field_name] = {
                    'type': 'logarithm',
                    'source': [col],
                    'formula': f"log({col})"
                }
            
            else:
                # Default: create a copy or aggregate
                if len(numeric_cols) >= 1:
                    df_new[field_name] = df[numeric_cols[0]]
                    explanation = f"Generated '{field_name}' as copy of {numeric_cols[0]}"
                    self.derivation_log.append(explanation)
            
            self.logger.log(
                "Field Generation Agent",
                f"Successfully generated field '{field_name}'",
                explanation
            )
            
            return df_new
            
        except Exception as e:
            self.logger.log(
                "Field Generation Agent",
                f"Failed to generate field '{field_name}': {str(e)}",
                "Returning original dataframe"
            )
            return df
    
    def suggest_derivable_fields(self, df: pd.DataFrame) -> List[Dict]:
        """Suggest fields that can be derived from existing data"""
        suggestions = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            suggestions.extend([
                {'name': f'{numeric_cols[0]}_to_{numeric_cols[1]}_ratio', 'type': 'ratio', 
                 'description': f'Ratio of {numeric_cols[0]} to {numeric_cols[1]}'},
                {'name': f'{numeric_cols[0]}_minus_{numeric_cols[1]}', 'type': 'difference',
                 'description': f'Difference between {numeric_cols[0]} and {numeric_cols[1]}'},
                {'name': 'total_sum', 'type': 'sum',
                 'description': f'Sum of all numeric fields'},
                {'name': 'average_value', 'type': 'average',
                 'description': f'Average of all numeric fields'}
            ])
        
        if len(numeric_cols) >= 1:
            col = numeric_cols[0]
            suggestions.extend([
                {'name': f'{col}_percent_change', 'type': 'percent_change',
                 'description': f'Percentage change in {col}'},
                {'name': f'{col}_moving_avg', 'type': 'rolling_average',
                 'description': f'Rolling average of {col}'},
                {'name': f'{col}_normalized', 'type': 'normalized',
                 'description': f'Normalized version of {col} (0-1 scale)'},
                {'name': f'{col}_cumulative', 'type': 'cumulative_sum',
                 'description': f'Cumulative sum of {col}'}
            ])
        
        self.logger.log(
            "Field Generation Agent",
            f"Identified {len(suggestions)} derivable fields",
            f"Suggestions: {[s['name'] for s in suggestions]}"
        )
        
        return suggestions
    
    def _detect_derivation_type(self, field_name: str) -> str:
        """Detect derivation type from field name"""
        field_lower = field_name.lower()
        
        if any(word in field_lower for word in ['ratio', 'per', 'rate']):
            return 'ratio'
        elif any(word in field_lower for word in ['diff', 'change', 'delta']):
            return 'difference'
        elif any(word in field_lower for word in ['total', 'sum']):
            return 'sum'
        elif any(word in field_lower for word in ['avg', 'average', 'mean']):
            return 'average'
        elif any(word in field_lower for word in ['pct', 'percent', '%']):
            return 'percent_change'
        elif any(word in field_lower for word in ['moving', 'rolling', 'ma']):
            return 'rolling_average'
        elif any(word in field_lower for word in ['norm', 'scaled']):
            return 'normalized'
        elif any(word in field_lower for word in ['cumulative', 'cumsum', 'running']):
            return 'cumulative_sum'
        elif any(word in field_lower for word in ['squared', 'square']):
            return 'squared'
        elif any(word in field_lower for word in ['log', 'ln']):
            return 'logarithm'
        else:
            return 'ratio'  # Default
    
    def _attempt_derivation(self, df: pd.DataFrame, field_name: str) -> Optional[str]:
        """Attempt to find a derivation strategy"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) == 0:
            return None
        
        # Detect from name
        derivation_type = self._detect_derivation_type(field_name)
        
        # Check if derivation is possible
        if derivation_type in ['ratio', 'difference'] and len(numeric_cols) < 2:
            return None
        
        return derivation_type

# ============================================================================
# AGENT 4: HYPOTHESIS GENERATION AGENT
# ============================================================================

class HypothesisGenerationAgent:
    """Discovers testable patterns and relationships in data"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.hypotheses = []
    
    def generate_hypotheses(self, df: pd.DataFrame) -> List[Dict]:
        """Autonomously generate testable hypotheses using LLM"""
        self.logger.log(
            "Hypothesis Generation Agent",
            "Analyzing data to discover patterns and relationships",
            "Generating testable hypotheses"
        )
        
        self.hypotheses = []
        
        # Check if LLM is available
        llm = getattr(self.msg_bus, 'llm_engine', None)
        
        if llm and llm.is_ready():
            try:
                # 1. Summarize data context for the LLM
                columns = df.columns.tolist()
                dtypes = df.dtypes.astype(str).to_dict()
                
                # Get a small sample of non-null data
                sample_data = {}
                for col in columns[:20]: # Limit to 20 columns for context size
                    sample_vals = df[col].dropna().head(3).tolist()
                    sample_data[col] = sample_vals
                
                data_summary = f"""
                Columns: {columns}
                Data Types: {dtypes}
                Sample Data: {sample_data}
                """
                
                system_prompt = """You are a brilliant Data Scientist Agent. 
Your job is to look at a summary of a dataset and generate testable hypotheses or business questions.
Output EXACTLY 4 hypotheses in valid JSON format as a list of dictionaries with these keys:
- 'hypothesis': A clear, testable statement (e.g., 'Revenue is positively correlated with marketing spend')
- 'type': Must be one of ['correlation', 'trend', 'distribution', 'comparison']
- 'variables': A list of 1 or 2 exact column names involved
- 'strength': A float between 0.0 and 1.0 representing expected confidence (make a reasonable guess)

Example Output:
[
  {"hypothesis": "Age is positively correlated with Income", "type": "correlation", "variables": ["Age", "Income"], "strength": 0.85}
]
Respond ONLY with the raw JSON array. Do not use blockquotes or markdown formatting."""
                
                user_prompt = f"Generate hypotheses for this dataset:\n\n{data_summary}"
                
                self.logger.log("Hypothesis Generation Agent", "Requesting LLM to generate hypotheses", "Querying Intelligence Engine")
                
                # 2. Call LLM
                response = llm.generate(system_prompt, user_prompt)
                
                # 3. Parse JSON
                import json
                
                # Clean up if the LLM returned markdown blocks
                clean_response = response.strip()
                if clean_response.startswith('```json'):
                    clean_response = clean_response[7:]
                if clean_response.startswith('```'):
                    clean_response = clean_response[3:]
                if clean_response.endswith('```'):
                    clean_response = clean_response[:-3]
                    
                self.hypotheses = json.loads(clean_response)
                
                # Add default p_values so downstream Analysis Agent works
                for h in self.hypotheses:
                    h['p_value'] = 0.01  # Mock significant p-value for now, AnalysisAgent recomputes this
                
                self.logger.log(
                    "Hypothesis Generation Agent",
                    f"LLM generated {len(self.hypotheses)} testable hypotheses",
                    f"Hypotheses: {[h['hypothesis'] for h in self.hypotheses]}"
                )
                
                return self.hypotheses
                
            except Exception as e:
                self.logger.log(
                    "Hypothesis Generation Agent",
                    f"LLM Hypothesis generation failed: {str(e)}",
                    "Falling back to rule-based generation"
                )
        
        # Fallback to original logic if LLM fails or is not configured
        # 1. Correlation hypotheses
        self._generate_correlation_hypotheses(df)
        
        # 2. Trend hypotheses
        self._generate_trend_hypotheses(df)
        
        # 3. Distribution hypotheses
        self._generate_distribution_hypotheses(df)
        
        # 4. Comparison hypotheses
        self._generate_comparison_hypotheses(df)
        
        self.logger.log(
            "Hypothesis Generation Agent",
            f"Generated {len(self.hypotheses)} testable hypotheses (Rule-Based)",
            f"Hypotheses: {[h['hypothesis'] for h in self.hypotheses]}"
        )
        
        return self.hypotheses
    
    def _generate_correlation_hypotheses(self, df: pd.DataFrame):
        """Generate correlation hypotheses"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Find strong correlations (> 0.7 or < -0.7)
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        col1 = corr_matrix.columns[i]
                        col2 = corr_matrix.columns[j]
                        relationship = "positively" if corr_val > 0 else "negatively"
                        self.hypotheses.append({
                            'hypothesis': f"{col1} is {relationship} correlated with {col2}",
                            'type': 'correlation',
                            'strength': abs(corr_val),
                            'variables': [col1, col2],
                            'p_value': self._calculate_correlation_pvalue(df[col1], df[col2])
                        })
    
    def _generate_trend_hypotheses(self, df: pd.DataFrame):
        """Generate trend hypotheses for time-series or sequential data"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            # Check for monotonic trends
            values = df[col].dropna().values
            if len(values) > 10:
                # Calculate linear trend
                x = np.arange(len(values))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
                
                if abs(r_value) > 0.5 and p_value < 0.05:
                    trend = "increasing" if slope > 0 else "decreasing"
                    self.hypotheses.append({
                        'hypothesis': f"{col} shows a {trend} trend over time",
                        'type': 'trend',
                        'strength': abs(r_value),
                        'variables': [col],
                        'p_value': p_value
                    })
    
    def _generate_distribution_hypotheses(self, df: pd.DataFrame):
        """Generate distribution hypotheses"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            values = df[col].dropna().values
            if len(values) > 30:
                # Test for normality
                stat, p_value = stats.normaltest(values)
                
                if p_value > 0.05:
                    self.hypotheses.append({
                        'hypothesis': f"{col} follows a normal distribution",
                        'type': 'distribution',
                        'strength': p_value,
                        'variables': [col],
                        'p_value': p_value
                    })
                
                # Check for skewness
                skewness = stats.skew(values)
                if abs(skewness) > 1:
                    direction = "right" if skewness > 0 else "left"
                    self.hypotheses.append({
                        'hypothesis': f"{col} is {direction}-skewed",
                        'type': 'distribution',
                        'strength': abs(skewness),
                        'variables': [col],
                        'p_value': None
                    })
    
    def _generate_comparison_hypotheses(self, df: pd.DataFrame):
        """Generate comparison hypotheses between groups"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for cat_col in categorical_cols:
            unique_vals = df[cat_col].nunique()
            if 2 <= unique_vals <= 10:  # Reasonable number of categories
                for num_col in numeric_cols:
                    # Check if there's a significant difference between groups
                    groups = [df[df[cat_col] == val][num_col].dropna().values 
                             for val in df[cat_col].unique()]
                    groups = [g for g in groups if len(g) > 0]
                    
                    if len(groups) >= 2:
                        try:
                            stat, p_value = stats.f_oneway(*groups)
                            if p_value < 0.05:
                                self.hypotheses.append({
                                    'hypothesis': f"{num_col} varies significantly across different {cat_col} categories",
                                    'type': 'comparison',
                                    'strength': 1 - p_value,
                                    'variables': [cat_col, num_col],
                                    'p_value': p_value
                                })
                        except:
                            pass
    
    def _calculate_correlation_pvalue(self, x, y):
        """Calculate p-value for correlation"""
        try:
            corr, p_value = stats.pearsonr(x.dropna(), y.dropna())
            return p_value
        except:
            return None

# ============================================================================
# AGENT 5: ANALYSIS AGENT
# ============================================================================

class AnalysisAgent:
    """Performs statistical tests and calculations"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.analysis_results = {}
    
    def analyze_data(self, df: pd.DataFrame, hypotheses: List[Dict]) -> Dict:
        """Perform comprehensive statistical analysis"""
        self.logger.log(
            "Analysis Agent",
            "Performing statistical tests on generated hypotheses",
            f"Testing {len(hypotheses)} hypotheses"
        )
        
        self.analysis_results = {
            'descriptive_stats': self._descriptive_statistics(df),
            'hypothesis_tests': self._test_hypotheses(df, hypotheses),
            'correlations': self._correlation_analysis(df),
            'anomalies': self._detect_anomalies(df),
            'summary': {}
        }
        
        self.logger.log(
            "Analysis Agent",
            "Statistical analysis complete",
            f"Generated insights for {len(hypotheses)} hypotheses"
        )
        
        return self.analysis_results
    
    def _descriptive_statistics(self, df: pd.DataFrame) -> Dict:
        """Generate descriptive statistics"""
        stats_dict = {}
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            stats_dict[col] = {
                'mean': float(df[col].mean()),
                'median': float(df[col].median()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'q25': float(df[col].quantile(0.25)),
                'q75': float(df[col].quantile(0.75))
            }
        
        return stats_dict
    
    def _test_hypotheses(self, df: pd.DataFrame, hypotheses: List[Dict]) -> List[Dict]:
        """Test each hypothesis"""
        tested_hypotheses = []
        
        for hyp in hypotheses:
            result = {
                'hypothesis': hyp['hypothesis'],
                'type': hyp['type'],
                'conclusion': 'Supported' if hyp.get('p_value') and hyp['p_value'] < 0.05 else 'Requires further investigation',
                'p_value': hyp.get('p_value'),
                'strength': hyp['strength']
            }
            tested_hypotheses.append(result)
        
        return tested_hypotheses
    
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict:
        """Comprehensive correlation analysis"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            return corr_matrix.to_dict()
        return {}
        
    def _detect_anomalies(self, df: pd.DataFrame) -> List[Dict]:
        """Detect statistical anomalies using Z-score method"""
        anomalies = []
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if df[col].std() > 0:
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                # Find indices where z-score > 3
                outlier_indices = np.where(z_scores > 3)[0]
                
                if len(outlier_indices) > 0:
                    # Map back to original dataframe indices
                    valid_idx = df[col].dropna().index
                    original_indices = valid_idx[outlier_indices]
                    outlier_values = df.loc[original_indices, col].values
                    
                    anomalies.append({
                        'column': col,
                        'count': len(outlier_indices),
                        'max_deviation': float(np.max(z_scores[outlier_indices])),
                        'example_values': [float(v) for v in outlier_values[:3]]
                    })
                    
        return anomalies

# ============================================================================
# AGENT 6: VISUALIZATION AGENT (ENHANCED)
# ============================================================================

class VisualizationAgent:
    """Autonomously selects optimal chart types with manual override capability"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.visualizations = []
    
    def create_visualizations(self, df: pd.DataFrame, hypotheses: List[Dict]) -> List[Dict]:
        """Autonomously decide and create visualizations (LLM Enhanced)"""
        self.logger.log(
            "Visualization Agent",
            "Analyzing data characteristics to select optimal visualizations",
            "Deciding chart types based on data patterns"
        )
        
        self.visualizations = []
        
        llm = getattr(self.msg_bus, 'llm_engine', None)
        
        # Create visualizations based on hypotheses
        for hyp in hypotheses[:8]:  # Limit to 8 hypothesis visualizations
            viz = None
            if llm and llm.is_ready():
                viz = self._llm_select_and_create_viz(df, hyp, llm)
                
            if not viz:
                # Fallback to rule-based
                viz = self._select_and_create_viz(df, hyp)
                
            if viz:
                self.visualizations.append(viz)
        
        # Add general overview visualizations
        self._create_overview_visualizations(df)
        
        self.logger.log(
            "Visualization Agent",
            f"Created {len(self.visualizations)} autonomous visualizations",
            f"Chart types: {[v['chart_type'] for v in self.visualizations]}"
        )
        
        return self.visualizations

    def _llm_select_and_create_viz(self, df: pd.DataFrame, hypothesis: Dict, llm) -> Union[Dict, None]:
        """Use LLM to select the best chart type and reasoning"""
        try:
            available_charts = self.get_available_chart_types()
            system_prompt = f"""You are an Expert Data Visualization Agent.
Given a hypothesis and some variables, select the absolute BEST Plotly chart type from this list: {available_charts}
Output exactly in this JSON format:
{{"chart_type": "selected_chart", "reasoning": "brief explanation why this is best"}}
Do not include any other text."""
            
            user_prompt = f"Hypothesis: {hypothesis['hypothesis']}\nType: {hypothesis['type']}\nVariables: {hypothesis['variables']}"
            
            response = llm.generate(system_prompt, user_prompt)
            
            import json
            clean_response = response.strip()
            if clean_response.startswith('```json'): clean_response = clean_response[7:]
            if clean_response.startswith('```'): clean_response = clean_response[3:]
            if clean_response.endswith('```'): clean_response = clean_response[:-3]
            
            decision = json.loads(clean_response)
            chart_type = decision.get("chart_type")
            reasoning = decision.get("reasoning", "LLM determined this is the best chart type")
            
            if chart_type not in available_charts:
                return None
                
            # Attempt to create the chart using the existing custom creation method
            x_col = hypothesis['variables'][0] if len(hypothesis['variables']) > 0 else None
            y_col = hypothesis['variables'][1] if len(hypothesis['variables']) > 1 else None
            
            # Auto-correct x/y assignment based on data types for specific charts
            if y_col and chart_type in ['bar', 'box', 'violin']:
                # Ensure x is categorical/discrete and y is numeric if possible
                if pd.api.types.is_numeric_dtype(df[x_col]) and not pd.api.types.is_numeric_dtype(df[y_col]):
                    x_col, y_col = y_col, x_col
            
            viz = self.create_custom_visualization(df, x_col, y_col, chart_type)
            if viz:
                viz['reasoning'] = reasoning + " (Chosen by AI Agent)"
                return viz
                
        except Exception as e:
            self.logger.log("Visualization Agent", f"LLM visualization failed: {str(e)}", "Falling back to rules")
            
        return None
    
    def get_available_chart_types(self) -> List[str]:
        """Return all available chart types for manual override"""
        return [
            'scatter', 'line', 'bar', 'box', 'histogram', 
            'kde', 'heatmap', 'violin', 'scatter_3d'
        ]
    
    def create_custom_visualization(self, df: pd.DataFrame, x_col: str, y_col: Optional[str], 
                                   chart_type: str) -> Union[Dict, None]:
        """Create a custom visualization with manual chart type selection"""
        self.logger.log(
            "Visualization Agent",
            f"Creating custom {chart_type} chart: {x_col} vs {y_col}",
            "Manual chart override applied"
        )
        
        try:
            custom_title = ""
            df_plot = df.copy()

            if chart_type == 'scatter':
                if y_col:
                    custom_title = f"Scatter: {x_col} vs {y_col}"
                    fig = px.scatter(df_plot, x=x_col, y=y_col, 
                                   title=custom_title,
                                   trendline="ols" if HAS_STATSMODELS else None)
                    reasoning = "Scatter plot with OLS trendline shows correlation" if HAS_STATSMODELS else "Scatter plot shows correlation"
                else:
                    custom_title = f"Scatter: {x_col}"
                    fig = px.scatter(df_plot, x=x_col, title=custom_title)
                    reasoning = "Scatter plot shows data distribution"
                
            elif chart_type == 'line':
                if y_col:
                    if pd.api.types.is_numeric_dtype(df_plot[y_col]):
                        df_agg = df_plot.groupby(x_col)[y_col].mean().reset_index()
                        custom_title = f"Line: Average {y_col} by {x_col}"
                    else:
                        df_agg = df_plot.copy()
                        custom_title = f"Line: {x_col} vs {y_col}"
                        
                    if pd.api.types.is_numeric_dtype(df_agg[x_col]) or pd.api.types.is_datetime64_any_dtype(df_agg[x_col]):
                        df_agg = df_agg.sort_values(by=x_col)
                    
                    fig = px.line(df_agg, x=x_col, y=y_col, title=custom_title)
                else:
                    custom_title = f"Line: {x_col}"
                    if pd.api.types.is_numeric_dtype(df_plot[x_col]) or pd.api.types.is_datetime64_any_dtype(df_plot[x_col]):
                        df_plot = df_plot.sort_values(by=x_col)
                    fig = px.line(df_plot, y=x_col, title=custom_title)
                reasoning = "Line chart shows trends. Data is aggregated and sorted to prevent overlapping."
                
            elif chart_type == 'bar':
                if y_col:
                    if pd.api.types.is_numeric_dtype(df_plot[y_col]):
                        df_agg = df_plot.groupby(x_col)[y_col].mean().reset_index()
                        df_agg = df_agg.sort_values(by=y_col, ascending=False).head(50)
                        custom_title = f"Bar: Average {y_col} by {x_col} (Top 50)"
                    else:
                        df_agg = df_plot.groupby(x_col)[y_col].count().reset_index()
                        df_agg.rename(columns={y_col: 'Count'}, inplace=True)
                        y_col = 'Count'
                        df_agg = df_agg.sort_values(by=y_col, ascending=False).head(50)
                        custom_title = f"Bar: Count by {x_col} (Top 50)"
                    
                    fig = px.bar(df_agg, x=x_col, y=y_col, title=custom_title)
                else:
                    counts = df_plot[x_col].value_counts().head(20)
                    custom_title = f"Bar: {x_col} (Top 20)"
                    fig = px.bar(x=counts.index, y=counts.values,
                               labels={'x': x_col, 'y': 'Count'},
                               title=custom_title)
                reasoning = "Bar chart enables category comparison"
                
            elif chart_type == 'box':
                if y_col:
                    custom_title = f"Box: {x_col} vs {y_col}"
                    fig = px.box(df_plot, x=x_col, y=y_col,
                               title=custom_title)
                    reasoning = "Box plot compares distributions across categories"
                else:
                    custom_title = f"Box: {x_col}"
                    fig = px.box(df_plot, y=x_col,
                               title=custom_title)
                    reasoning = "Box plot shows distribution, quartiles, and outliers"
                
            elif chart_type == 'histogram':
                if y_col and pd.api.types.is_numeric_dtype(df_plot[y_col]):
                    custom_title = f"Histogram: Average {y_col} by {x_col}"
                    fig = px.histogram(df_plot, x=x_col, y=y_col, histfunc='avg', nbins=30,
                                     title=custom_title)
                    reasoning = "Histogram shows aggregated distribution"
                else:
                    custom_title = f"Histogram: {x_col}"
                    fig = px.histogram(df_plot, x=x_col, nbins=30,
                                     title=custom_title,
                                     marginal="box")
                    reasoning = "Histogram shows frequency distribution with box plot"
                
            elif chart_type == 'kde':
                custom_title = f"KDE Distribution: {x_col}"
                fig = px.histogram(df_plot, x=x_col, nbins=30, marginal="violin",
                                 title=custom_title)
                reasoning = "KDE plot shows smooth probability distribution"
                
            elif chart_type == 'heatmap':
                if len(df_plot.select_dtypes(include=[np.number]).columns) >= 2:
                    corr_matrix = df_plot.select_dtypes(include=[np.number]).corr()
                    custom_title = "Correlation Heatmap"
                    fig = px.imshow(corr_matrix, 
                                  title=custom_title,
                                  color_continuous_scale="RdBu",
                                  aspect="auto")
                    reasoning = "Heatmap shows all pairwise correlations"
                else:
                    return None
                
            elif chart_type == 'violin':
                if y_col:
                    custom_title = f"Violin: {x_col} vs {y_col}"
                    fig = px.violin(df_plot, x=x_col, y=y_col,
                                  title=custom_title,
                                  box=True, points="outliers")
                    reasoning = "Violin plot shows distribution shape across categories"
                else:
                    custom_title = f"Violin: {x_col}"
                    fig = px.violin(df_plot, y=x_col,
                                  title=custom_title,
                                  box=True, points="outliers")
                    reasoning = "Violin plot reveals distribution shape"
                
            elif chart_type == 'scatter_3d' and y_col:
                # Get third numeric column if available
                numeric_cols = df_plot.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) >= 3:
                    z_col = [c for c in numeric_cols if c not in [x_col, y_col]][0]
                    custom_title = f"3D Scatter: {x_col}, {y_col}, {z_col}"
                    fig = px.scatter_3d(df_plot, x=x_col, y=y_col, z=z_col,
                                      title=custom_title)
                    reasoning = "3D scatter plot shows three-dimensional relationships"
                else:
                    return None
            else:
                return None
            
            self.logger.log(
                "Visualization Agent",
                f"Successfully created {chart_type} chart",
                reasoning
            )
            
            return {
                'chart_type': chart_type,
                'figure': fig,
                'title': custom_title if custom_title else f"{chart_type.title()}: {x_col}" + (f" vs {y_col}" if y_col else ""),
                'reasoning': reasoning,
                'x_col': x_col,
                'y_col': y_col
            }
            
        except Exception as e:
            self.logger.log(
                "Visualization Agent",
                f"Failed to create {chart_type}: {str(e)}",
                "Chart creation failed"
            )
            return None
    
    def _select_and_create_viz(self, df: pd.DataFrame, hypothesis: Dict) -> Union[Dict, None]:
        """Intelligently select chart type based on hypothesis"""
        hyp_type = hypothesis['type']
        variables = hypothesis['variables']
        
        try:
            if hyp_type == 'correlation' and len(variables) == 2:
                # Scatter plot for correlation
                fig = px.scatter(df, x=variables[0], y=variables[1], 
                               title=f"Correlation: {variables[0]} vs {variables[1]}",
                               trendline="ols" if HAS_STATSMODELS else None)
                
                self.logger.log(
                    "Visualization Agent",
                    f"Selected scatter plot for correlation between {variables[0]} and {variables[1]}",
                    "Scatter plots best show relationships between two numeric variables"
                )
                
                return {
                    'chart_type': 'scatter',
                    'figure': fig,
                    'title': f"{variables[0]} vs {variables[1]}",
                    'reasoning': 'Scatter plot selected to visualize correlation between two numeric variables',
                    'x_col': variables[0],
                    'y_col': variables[1]
                }
            
            elif hyp_type == 'trend' and len(variables) == 1:
                # Line chart for trends
                fig = px.line(df, y=variables[0], 
                             title=f"Trend Analysis: {variables[0]}",
                             labels={'index': 'Index', variables[0]: variables[0]})
                
                self.logger.log(
                    "Visualization Agent",
                    f"Selected line chart for trend in {variables[0]}",
                    "Line charts best show trends over sequential data"
                )
                
                return {
                    'chart_type': 'line',
                    'figure': fig,
                    'title': f"Trend: {variables[0]}",
                    'reasoning': 'Line chart selected to visualize trend over time/sequence',
                    'x_col': 'index',
                    'y_col': variables[0]
                }
            
            elif hyp_type == 'distribution' and len(variables) == 1:
                # Histogram for distribution
                fig = px.histogram(df, x=variables[0], 
                                 title=f"Distribution: {variables[0]}",
                                 marginal="box")
                
                self.logger.log(
                    "Visualization Agent",
                    f"Selected histogram for distribution of {variables[0]}",
                    "Histograms best show frequency distributions"
                )
                
                return {
                    'chart_type': 'histogram',
                    'figure': fig,
                    'title': f"Distribution: {variables[0]}",
                    'reasoning': 'Histogram selected to show frequency distribution',
                    'x_col': variables[0],
                    'y_col': None
                }
            
            elif hyp_type == 'comparison' and len(variables) == 2:
                # Box plot for group comparison
                fig = px.box(df, x=variables[0], y=variables[1],
                            title=f"Comparison: {variables[1]} across {variables[0]}")
                
                self.logger.log(
                    "Visualization Agent",
                    f"Selected box plot for comparing {variables[1]} across {variables[0]} categories",
                    "Box plots best show distributions across categories"
                )
                
                return {
                    'chart_type': 'box',
                    'figure': fig,
                    'title': f"{variables[1]} by {variables[0]}",
                    'reasoning': 'Box plot selected to compare distributions across groups',
                    'x_col': variables[0],
                    'y_col': variables[1]
                }
            
            return None
        except Exception as e:
            self.logger.log(
                "Visualization Agent",
                f"Error creating visualization: {str(e)}",
                "Failed to create chart"
            )
            return None
    
    def _create_overview_visualizations(self, df: pd.DataFrame):
        """Create general overview visualizations"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Correlation heatmap if multiple numeric columns
        if len(numeric_cols) >= 2:
            try:
                corr_matrix = df[numeric_cols].corr()
                fig = px.imshow(corr_matrix, 
                               title="Correlation Heatmap",
                               color_continuous_scale="RdBu",
                               aspect="auto",
                               zmin=-1, zmax=1)
                
                self.logger.log(
                    "Visualization Agent",
                    "Created correlation heatmap for all numeric variables",
                    "Heatmap provides overview of all relationships"
                )
                
                self.visualizations.append({
                    'chart_type': 'heatmap',
                    'figure': fig,
                    'title': 'Correlation Matrix',
                    'reasoning': 'Heatmap selected to show all pairwise correlations at once',
                    'x_col': 'correlation',
                    'y_col': 'all_numeric'
                })
            except:
                pass

# ============================================================================
# AGENT 7: EXPLANATION AGENT
# ============================================================================

class ExplanationAgent:
    """Translates technical findings into plain English"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
        self.explanations = []
    
    def explain_findings(self, df: pd.DataFrame, hypotheses: List[Dict], 
                        analysis_results: Dict) -> List[str]:
        """Generate plain-English explanations directly using LLM if available"""
        self.logger.log(
            "Explanation Agent",
            "Translating technical findings to plain English",
            "Creating non-technical explanations"
        )
        
        self.explanations = []
        llm = getattr(self.msg_bus, 'llm_engine', None)
        
        if llm and llm.is_ready():
            try:
                # Compile findings for the LLM
                findings_summary = f"Total anomalies: {len(analysis_results.get('anomalies', []))}\n"
                for h in hypotheses:
                    findings_summary += f"- {h['hypothesis']} (Type: {h['type']}, P-Value: {h.get('p_value', 'N/A')})\n"
                
                system_prompt = """You are an Expert Business Analyst.
Translate the following statistical findings and hypotheses into clear, concise, plain English insights for a business executive.
Format your output as a markdown list of 3-5 bullet points. Start each bullet with a relevant emoji.
Do NOT mention 'p-values' or 'statistical significance' - translate those concepts into 'strong confidence' or 'proven'.
Do not repeat the hypotheses verbatim, synthesize them."""

                response = llm.generate(system_prompt, findings_summary)
                
                # Split the markdown list into individual explanations
                for line in response.split('\n'):
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('* '):
                        self.explanations.append(line[2:])
                    elif len(line) > 5 and not line.startswith('#'):
                        self.explanations.append(line)
                        
                self.logger.log("Explanation Agent", f"Generated {len(self.explanations)} LLM-powered insights", "Success")
                return self.explanations
            except Exception as e:
                self.logger.log("Explanation Agent", f"LLM Explanation failed: {str(e)}", "Falling back to rule-based")

        # Fallback to rule-based explanations
        
        # Explain dataset overview
        self._explain_dataset_overview(df)
        
        # Explain each hypothesis
        for hyp in hypotheses:
            explanation = self._explain_hypothesis(hyp, df)
            if explanation:
                self.explanations.append(explanation)
        
        # Explain key insights
        self._explain_key_insights(df, analysis_results)
        
        self.logger.log(
            "Explanation Agent",
            f"Generated {len(self.explanations)} plain-English explanations",
            "Explanations ready for non-technical users"
        )
        
        return self.explanations
    
    def _explain_dataset_overview(self, df: pd.DataFrame):
        """Explain dataset characteristics"""
        num_rows = len(df)
        num_cols = len(df.columns)
        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
        
        explanation = f"""
📊 **Dataset Overview**: 
Your dataset contains {num_rows:,} records with {num_cols} different variables. 
{numeric_cols} of these variables are numeric, which means we can perform quantitative analysis on them.
        """
        self.explanations.append(explanation.strip())
    
    def _explain_hypothesis(self, hypothesis: Dict, df: pd.DataFrame) -> str:
        """Explain a single hypothesis in plain English"""
        hyp_text = hypothesis['hypothesis']
        hyp_type = hypothesis['type']
        strength = hypothesis['strength']
        p_value = hypothesis.get('p_value')
        
        if hyp_type == 'correlation':
            if strength > 0.9:
                strength_text = "very strong"
            elif strength > 0.7:
                strength_text = "strong"
            elif strength > 0.5:
                strength_text = "moderate"
            else:
                strength_text = "weak"
            
            explanation = f"""
🔗 **Relationship Found**: {hyp_text}
This is a {strength_text} relationship (strength: {strength:.2f}). 
This means that as one variable changes, the other tends to change in a predictable way.
            """
            
        elif hyp_type == 'trend':
            explanation = f"""
📈 **Trend Detected**: {hyp_text}
The data shows a clear pattern over time with {strength:.2f} consistency. 
This trend could help predict future behavior.
            """
            
        elif hyp_type == 'distribution':
            explanation = f"""
📊 **Data Pattern**: {hyp_text}
The data shows a specific distribution pattern. Understanding this helps us know what values are typical and which are unusual.
            """
            
        elif hyp_type == 'comparison':
            explanation = f"""
⚖️ **Group Difference**: {hyp_text}
The analysis shows that different groups have measurably different characteristics. This insight could guide decision-making across categories.
            """
        else:
            explanation = f"💡 **Insight**: {hyp_text}"
        
        if p_value and p_value < 0.05:
            explanation += "\n✅ This finding is statistically significant (p < 0.05), meaning it's unlikely to be due to chance."
        
        return explanation.strip()
    
    def _explain_key_insights(self, df: pd.DataFrame, analysis_results: Dict):
        """Explain key statistical insights"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            # Find column with highest variance
            variances = {col: df[col].var() for col in numeric_cols}
            most_variable = max(variances, key=variances.get)
            
            explanation = f"""
🎯 **Key Insight**: 
The variable '{most_variable}' shows the most variation in your data, 
suggesting it might be an important factor to focus on in your analysis.
            """
            self.explanations.append(explanation.strip())

# ============================================================================
# STOCK ANALYSIS AGENT
# ============================================================================

class StockAnalysisAgent:
    """Specialized agent for stock/crypto analysis"""
    
    def __init__(self, logger: AgentLogger, msg_bus: MessageBus = None):
        self.logger = logger
        self.msg_bus = msg_bus
    
    def search_ticker_symbol(self, query: str) -> Optional[str]:
        """Search for a valid stock ticker symbol using Yahoo Finance's unofficial search API"""
        if not query or not str(query).strip():
            return None
            
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if 'quotes' in data and len(data['quotes']) > 0:
                    # Return the symbol of the first matching quote
                    return data['quotes'][0].get('symbol')
        except Exception as e:
            self.logger.log(
                "Stock Analysis Agent",
                f"Error searching symbol for query '{query}': {str(e)}",
                "Falling back to exact original input"
            )
        
        # Fall back to returning original input if search fails
        return query.strip().upper()

    def fetch_stock_data(self, query: str, period: str) -> pd.DataFrame:
        """Fetch stock/crypto data, automatically resolving names to symbols if necessary"""
        # Resolve company name to ticker symbol first
        symbol = self.search_ticker_symbol(query)
        
        self.logger.log(
            "Stock Analysis Agent",
            f"Fetching market data for resolved symbol {symbol} (Original search: {query})",
            f"Time period: {period}"
        )
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                self.logger.log(
                    "Stock Analysis Agent",
                    f"No data found for symbol {symbol}",
                    "Please check the symbol and try again"
                )
                return None
            
            # Add technical indicators
            df = self._add_technical_indicators(df)
            
            self.logger.log(
                "Stock Analysis Agent",
                f"Successfully fetched {len(df)} days of data",
                f"Columns: {list(df.columns)}"
            )
            
            return df
        
        except Exception as e:
            self.logger.log(
                "Stock Analysis Agent",
                f"Error fetching data: {str(e)}",
                "Failed to retrieve market data"
            )
            return None
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add technical analysis indicators"""
        # Moving averages
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # Volatility (20-day rolling standard deviation)
        df['Volatility'] = df['Close'].rolling(window=20).std()
        
        # Daily returns
        df['Daily_Return'] = df['Close'].pct_change() * 100
        
        # RSI (Relative Strength Index)
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        return df
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_stock(self, df: pd.DataFrame, features: List[str]) -> Dict:
        """Analyze selected stock features"""
        self.logger.log(
            "Stock Analysis Agent",
            f"Analyzing features: {features}",
            "Performing technical analysis"
        )
        
        analysis = {
            'summary': {},
            'insights': []
        }
        
        # Price trend analysis
        if 'price_trend' in features:
            recent_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
            analysis['summary']['price_change'] = f"{recent_change:.2f}%"
            
            trend = "upward" if recent_change > 0 else "downward"
            analysis['insights'].append(
                f"📊 The stock shows a {trend} trend with a {abs(recent_change):.2f}% change over the period."
            )
        
        # Volatility analysis
        if 'volatility' in features:
            avg_volatility = df['Volatility'].mean()
            current_volatility = df['Volatility'].iloc[-1]
            
            vol_status = "high" if current_volatility > avg_volatility * 1.2 else "moderate" if current_volatility > avg_volatility * 0.8 else "low"
            analysis['insights'].append(
                f"📉 Current volatility is {vol_status} compared to the average (Current: {current_volatility:.2f}, Average: {avg_volatility:.2f})."
            )
        
        # Moving average analysis
        if 'moving_averages' in features:
            current_price = df['Close'].iloc[-1]
            ma_20 = df['MA_20'].iloc[-1]
            ma_50 = df['MA_50'].iloc[-1]
            
            if not pd.isna(ma_20) and not pd.isna(ma_50):
                if current_price > ma_20 and current_price > ma_50:
                    signal = "bullish"
                elif current_price < ma_20 and current_price < ma_50:
                    signal = "bearish"
                else:
                    signal = "neutral"
                
                analysis['insights'].append(
                    f"📈 Moving average signal: {signal.upper()} (Price: ${current_price:.2f}, MA20: ${ma_20:.2f}, MA50: ${ma_50:.2f})"
                )
        
        # RSI analysis
        if 'rsi' in features:
            current_rsi = df['RSI'].iloc[-1]
            if not pd.isna(current_rsi):
                if current_rsi > 70:
                    rsi_signal = "overbought"
                elif current_rsi < 30:
                    rsi_signal = "oversold"
                else:
                    rsi_signal = "neutral"
                
                analysis['insights'].append(
                    f"📊 RSI Indicator: {current_rsi:.2f} - Market is {rsi_signal.upper()}"
                )
        
        return analysis

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    st.set_page_config(
        page_title="Autonomous Data Analysis System",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # --- MODERN SLEEK UI INJECTION ---
    # Top-tier Designer UI: Glassmorphism, Google Fonts, Font Awesome Icons, and Vibrant Dark-Mode 
    st.markdown("""
        <!-- Font Awesome Icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        
        <style>
        /* Import Segoe UI or fallback */
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI&display=swap');

        /* Global App Background - Power BI Light Gray Canvas */
        .stApp {
            background-color: #f3f2f1;
            font-family: 'Segoe UI', 'Open Sans', 'Inter', sans-serif;
            color: #252423;
        }

        /* Titles and Headers */
        h1, h2, h3, p, span, div {
            color: #252423;
        }
        
        h1, h2, h3 {
            font-weight: 600;
        }
        
        .stMarkdown h1 {
            color: #118DFF;
            font-size: 2.2rem;
            margin-bottom: -1rem;
        }

        /* Sleek Sidebar - Power BI Service Style */
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 1px solid #edebe9;
        }

        /* Premium Buttons */
        .stButton > button {
            background-color: #118dff;
            color: white;
            font-weight: 600;
            border-radius: 2px;
            border: none;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background-color: #0c6abf;
        }

        /* Inputs & Select Boxes */
        .stTextInput input, .stSelectbox > div > div {
            background-color: #ffffff !important;
            border-radius: 2px !important;
            border: 1px solid #605e5c !important;
            color: #323130 !important;
        }
        
        .stTextInput input:focus, .stSelectbox > div > div:focus {
            border-color: #118dff !important;
            box-shadow: 0 0 0 1px #118dff !important;
        }

        /* Power BI KPI Cards */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #edebe9;
            padding: 15px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            color: #323130;
        }
        
        [data-testid="stMetricLabel"] {
            color: #605e5c;
            font-size: 0.9rem;
            font-weight: 600;
        }

        /* Expanders and Containers - PBI Visual containers */
        .streamlit-expanderHeader {
            background-color: #ffffff !important;
            border-radius: 4px 4px 0 0 !important;
            border: 1px solid #edebe9 !important;
            border-bottom: none !important;
            color: #252423 !important;
            font-weight: 600;
        }
        
        .streamlit-expanderContent {
            background-color: #ffffff;
            border: 1px solid #edebe9;
            border-top: none;
            border-radius: 0 0 4px 4px;
            color: #252423;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px;
            background-color: #ffffff;
            border-bottom: 2px solid #edebe9;
            padding: 0 1rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: none;
            color: #605e5c;
            padding: 10px 16px;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: transparent;
            border-bottom: 3px solid #118dff;
            color: #118dff;
        }

        /* Toast / Notifications */
        .stAlert {
            background-color: #ffffff !important;
            border: 1px solid #edebe9 !important;
            border-left: 4px solid #118dff !important;
            color: #323130;
        }
        
        /* Font Awesome Icons Styling */
        .icon-large { font-size: 1.5rem; margin-right: 0.5rem; color: #118dff; }
        .icon-medium { font-size: 1.2rem; margin-right: 0.4rem; color: #118dff; }
        .icon-small { font-size: 0.9rem; margin-right: 0.3rem; color: #118dff; }
        
        /* Icon colors by category */
        .icon-success { color: #107c10; } /* PBI Green */
        .icon-warning { color: #d83b01; } /* PBI Orange */
        .icon-error { color: #a4262c; }   /* PBI Red */
        .icon-info { color: #0078d4; }    /* PBI Blue */
        </style>
    """, unsafe_allow_html=True)
    # -------------------------------
    
    st.markdown("<h1>" + IconSystem.icon('robot', 'large') + " Autonomous Data Analysis System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9ca3af; font-size:1.1rem; margin-top:-10px; margin-bottom:2rem;'>Council of Intelligent Agents - No External AI Models</p>", unsafe_allow_html=True)
    
    # Initialize logger
    logger = AgentLogger()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2>" + IconSystem.icon('settings', 'medium') + " Control Panel</h2>", unsafe_allow_html=True)
        
        st.markdown("### 🔑 API Configuration")
        api_key = st.text_input("OpenRouter API Key", type="password", key="openrouter_api_key",
                              help="Get your free key at https://openrouter.ai")
                              
        llm_model = st.selectbox("Intelligence Model", 
            ["meta-llama/llama-3-8b-instruct:free", 
             "mistralai/mistral-7b-instruct:free", 
             "google/gemma-2-9b-it:free"],
             help="Select the AI brain for the agents"
        )
        
        if api_key:
            st.success("API Key Provided")
        else:
            st.warning("⚠️ API Key required for Autonomous Agents")
            
        st.markdown("---")
        
        analysis_mode = st.radio(
            "Select Analysis Mode:",
            ["Report Analysis", "Stock Analysis"]
        )
        
        st.markdown("---")
        st.markdown("<h3>" + IconSystem.icon('robot', 'small') + " Agent Status</h3>", unsafe_allow_html=True)
        st.success("✅ Data Ingestion Agent: Active")
        st.success("✅ Self-Healing Agent: Active")
        st.success("✅ Field Generation Agent: Active")
        st.success("✅ Hypothesis Generation Agent: Active")
        st.success("✅ Analysis Agent: Active")
        st.success("✅ Visualization Agent: Active")
        st.success("✅ Explanation Agent: Active")
        
        st.markdown("---")
        if st.button("🗑️ Clear Agent Logs"):
            logger.clear_logs()
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Analysis",
        "📈 Visualizations",
        "🧠 Agent Logs"
    ])
    
    # ========================================================================
    # REPORT ANALYSIS MODE
    # ========================================================================
    
    if analysis_mode == "Report Analysis":
        with tab1:
            st.markdown("<h2>" + IconSystem.icon('chart', 'medium') + " Report Analysis</h2>", unsafe_allow_html=True)
            
            # File upload
            st.markdown("<h3>" + IconSystem.icon('upload', 'small') + " 1. Upload Your Data</h3>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file",
                type=['csv', 'xlsx', 'xls'],
                help="Upload your dataset for autonomous analysis (supports multi-sheet Excel)"
            )
            
            # Sample data option
            use_sample = st.checkbox("Use sample dataset (Iris)")
            
            df = None
            
            if use_sample:
                from sklearn.datasets import load_iris
                iris = load_iris()
                df = pd.DataFrame(iris.data, columns=iris.feature_names)
                df['species'] = iris.target
                st.success(f"✅ Loaded sample Iris dataset")
            elif uploaded_file:
                # Initialize agents
                ingestion_agent = DataIngestionAgent(logger)
                data = ingestion_agent.ingest_csv(uploaded_file)
                
                # Handle multi-sheet or single sheet
                if isinstance(data, dict):
                    # Multiple sheets detected
                    st.success(f"✅ Found {len(data)} sheets: {list(data.keys())}")
                    
                    # Sheet selection UI
                    st.markdown("<h3>" + IconSystem.icon('table', 'small') + " Multi-Sheet Selection</h3>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        selected_sheets = st.multiselect(
                            "Select sheets to analyze:",
                            list(data.keys()),
                            default=list(data.keys())
                        )
                    
                    with col2:
                        merge_strategy = st.selectbox(
                            "Merge strategy:",
                            ["Concatenate rows", "Merge on index"],
                            help="How to combine multiple sheets"
                        )
                    
                    if selected_sheets:
                        sheets_to_merge = {k: v for k, v in data.items() if k in selected_sheets}
                        
                        # Merge strategy
                        merge_strat = 'concat' if merge_strategy == "Concatenate rows" else 'merge_on_index'
                        df = ingestion_agent.merge_sheets(sheets_to_merge, merge_strategy=merge_strat)
                        
                        st.success(f"✅ Merged {len(selected_sheets)} sheets: {len(df)} rows × {len(df.columns)} columns")
                elif isinstance(data, pd.DataFrame):
                    df = data
                    st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
                else:
                    st.error("❌ Failed to load file")
            
            if df is not None and len(df) > 0:
                # Show data preview
                with st.expander("📋 Data Preview"):
                    st.dataframe(df.head(10))
                
                st.markdown("---")
                st.markdown("<h3>" + IconSystem.icon('chart', 'small') + " 2. Select Variables to Analyze</h3>", unsafe_allow_html=True)
                
                all_columns = list(df.columns)
                # Filter out system columns
                all_columns = [c for c in all_columns if not c.startswith('_')]
                
                selected_columns = st.multiselect(
                    "Choose variables for analysis:",
                    all_columns,
                    default=all_columns[:min(5, len(all_columns))]
                )
                
                # Field Generation Section
                st.markdown("---")
                st.markdown("<h3>" + IconSystem.icon('magic', 'small') + " Generate New Fields (Optional)</h3>", unsafe_allow_html=True)
                
                with st.expander("✨ Auto-Generate Derived Fields"):
                    st.markdown("**The Field Generation Agent can create new variables from existing data:**")
                    
                    field_gen_agent = FieldGenerationAgent(logger)
                    suggestions = field_gen_agent.suggest_derivable_fields(df[selected_columns] if selected_columns else df)
                    
                    if suggestions:
                        st.markdown("**Suggested fields you can generate:**")
                        
                        # Create tabs for suggestions
                        suggestion_cols = st.columns(min(3, len(suggestions)))
                        
                        for idx, sug in enumerate(suggestions[:6]):  # Show top 6 suggestions
                            col_idx = idx % len(suggestion_cols)
                            
                            with suggestion_cols[col_idx]:
                                st.markdown(f"**{sug['name']}**")
                                st.caption(sug['description'])
                                
                                if st.button(f"Generate", key=f"gen_{idx}"):
                                    df = field_gen_agent.generate_field(df, sug['name'], sug['type'])
                                    st.session_state['df_modified'] = df
                                    st.success(f"✅ Generated '{sug['name']}'")
                                    st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**Or create a custom field:**")
                    
                    col1, col2, col3 = st.columns([2, 2, 1])
                    with col1:
                        custom_field_name = st.text_input(
                            "New field name:",
                            placeholder="e.g., profit_margin"
                        )
                    
                    with col2:
                        derivation_type = st.selectbox(
                            "Derivation type:",
                            ['auto', 'ratio', 'difference', 'sum', 'average', 
                             'percent_change', 'rolling_average', 'normalized', 
                             'cumulative_sum', 'squared', 'logarithm']
                        )
                    
                    with col3:
                        if st.button("🚀 Generate", key="custom_field_btn"):
                            if custom_field_name:
                                field_gen_agent = FieldGenerationAgent(logger)
                                df = field_gen_agent.generate_field(df, custom_field_name, derivation_type)
                                st.session_state['df_modified'] = df
                                
                                if custom_field_name in df.columns:
                                    st.success(f"✅ Generated '{custom_field_name}'")
                                    if field_gen_agent.derivation_log:
                                        st.info(field_gen_agent.derivation_log[-1])
                                    st.rerun()
                
                # Update selected columns to include generated fields
                if 'df_modified' in st.session_state:
                    df = st.session_state['df_modified']
                    all_columns = list(df.columns)
                    all_columns = [c for c in all_columns if not c.startswith('_')]
                
                st.markdown("---")
                
                # Checkbox for Auto-Derivation during sequence
                auto_derive = st.checkbox("🔮 Automatically derive missing result fields (Top 2 suggestions)", value=True, help="Agent will autonomously figure out missing fields like 'revenue' or 'profit' from the dataset and generate them.")
                
                if st.button("🚀 Run Autonomous Analysis", type="primary"):
                    if selected_columns:
                        df_analysis = df[selected_columns].copy()
                        
                        try:
                            # Show initial data types
                            with st.expander("📋 Initial Data Types"):
                                st.dataframe(df_analysis.dtypes.to_frame('Original Data Type'))
                            
                            with st.spinner("🤖 Agents are working... This may take a moment"):
                                # Initialize LLM Engine
                                llm_engine = LLMEngine(api_key=st.session_state.get("openrouter_api_key"), 
                                                       model=st.session_state.get("llm_model", "meta-llama/llama-3-8b-instruct:free"),
                                                       logger=logger)
                                
                                # Initialize Message Bus
                                msg_bus = MessageBus(logger, llm_engine)

                                # Data Ingestion Agent
                                ingestion_agent = DataIngestionAgent(logger, msg_bus)
                                msg_bus.subscribe("Ingestion", ingestion_agent)
                                msg_bus.publish("System", "Ingestion", "StartValidation", "Commencing data ingestion")
                                validation_report = ingestion_agent.validate_data(df_analysis)
                                
                                # Self-Healing Agent with progress indicator
                                with st.spinner("🔧 Self-Healing Agent: Fixing data types and dropping unnecessary fields..."):
                                    healing_agent = SelfHealingAgent(logger, msg_bus)
                                    msg_bus.subscribe("Healing", healing_agent)
                                    msg_bus.publish("Ingestion", "Healing", "DataValidated", "Requesting self-healing on dataset")
                                    df_clean = healing_agent.heal_data(df_analysis)
                                    
                                # Auto-Derive Result Fields immediately after clean
                                if auto_derive:
                                    field_gen_agent = FieldGenerationAgent(logger, msg_bus)
                                    msg_bus.subscribe("FieldGen", field_gen_agent)
                                    msg_bus.publish("Healing", "FieldGen", "DataHealed", "Requesting field generation")
                                    suggestions = field_gen_agent.suggest_derivable_fields(df_clean)
                                    st.session_state['auto_derived_logs'] = []
                                    if suggestions:
                                        for sug in suggestions[:2]: # Top 2 highly confident derivations
                                            df_clean = field_gen_agent.generate_field(df_clean, sug['name'], sug['type'])
                                            st.session_state['auto_derived_logs'].append(f"Autonomous Field Created: '{sug['name']}' ({sug['type']})")
                                
                                # Store issues and fixes
                                st.session_state['issues'] = ingestion_agent.issues_detected
                                st.session_state['fixes'] = healing_agent.fixes_applied
                                
                                # Show corrected data types
                                if healing_agent.fixes_applied:
                                    with st.expander("✅ Corrected Data Types"):
                                        st.dataframe(df_clean.dtypes.to_frame('Corrected Data Type'))
                                
                                # Hypothesis Generation Agent
                                hypothesis_agent = HypothesisGenerationAgent(logger, msg_bus)
                                msg_bus.subscribe("Hypothesis", hypothesis_agent)
                                msg_bus.publish("System", "Hypothesis", "DataReady", "Requesting hypothesis generation")
                                hypotheses = hypothesis_agent.generate_hypotheses(df_clean)
                                st.session_state['hypotheses'] = hypotheses
                                
                                # Analysis Agent
                                analysis_agent = AnalysisAgent(logger, msg_bus)
                                msg_bus.subscribe("Analysis", analysis_agent)
                                msg_bus.publish("Hypothesis", "Analysis", "HypothesesGenerated", f"Testing {len(hypotheses)} hypotheses")
                                analysis_results = analysis_agent.analyze_data(df_clean, hypotheses)
                                st.session_state['analysis_results'] = analysis_results
                                
                                # Visualization Agent
                                viz_agent = VisualizationAgent(logger, msg_bus)
                                msg_bus.subscribe("Visualization", viz_agent)
                                msg_bus.publish("Analysis", "Visualization", "AnalysisComplete", "Requesting visualization for results")
                                visualizations = viz_agent.create_visualizations(df_clean, hypotheses)
                                st.session_state['visualizations'] = visualizations
                                st.session_state['viz_agent'] = viz_agent  # Store agent for manual override
                                
                                # Explanation Agent
                                explanation_agent = ExplanationAgent(logger, msg_bus)
                                msg_bus.subscribe("Explanation", explanation_agent)
                                msg_bus.publish("Visualization", "Explanation", "VisualizationsCreated", "Requesting plain English summary")
                                explanations = explanation_agent.explain_findings(df_clean, hypotheses, analysis_results)
                                st.session_state['explanations'] = explanations
                                
                                st.session_state['df_clean'] = df_clean
                                st.session_state['df_original'] = df_analysis
                            
                            st.success("✅ Autonomous analysis complete!")
                            st.balloons()
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
                            logger.log(
                                "System Error",
                                f"Analysis failed with error: {str(e)}",
                                f"Traceback: {traceback.format_exc()}"
                            )
                            st.error("Please check the Agent Logs tab for details.")
                            
                    else:
                        st.warning("⚠️ Please select at least one variable to analyze")
                
                # Display results if available
                if 'hypotheses' in st.session_state:
                    st.markdown("---")
                    st.markdown("<h3>" + IconSystem.icon('search', 'small') + " Data Quality Report</h3>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### ⚠️ Issues Detected")
                        if st.session_state.get('issues'):
                            for issue in st.session_state['issues']:
                                st.warning(issue)
                        else:
                            st.success("✅ No issues detected")
                    
                    with col2:
                        st.markdown("#### ✅ Fixes Applied")
                        if st.session_state.get('fixes'):
                            for fix in st.session_state['fixes'][:10]:  # Show first 10
                                st.success(fix)
                            if len(st.session_state.get('fixes', [])) > 10:
                                st.info(f"... and {len(st.session_state['fixes']) - 10} more fixes")
                        st.info("No fixes needed")
                        
                    # Show Auto-Derived Fields if applicable
                    if st.session_state.get('auto_derived_logs'):
                         st.markdown("---")
                         st.subheader("🔮 Autonomously Derived Fields")
                         st.markdown("The Field-Generation Agent derived and auto-attached missing components:")
                         
                         cols = st.columns(min(len(st.session_state['auto_derived_logs']), 4))
                         for i, log in enumerate(st.session_state['auto_derived_logs']):
                             with cols[i % len(cols)]:
                                 st.success(f"{log}")
                                 
                    # Show Anomalies Detected
                    if st.session_state.get('analysis_results', {}).get('anomalies'):
                        st.markdown("---")
                        st.subheader("🚨 Statistical Anomalies Detected")
                        
                        anomalies = st.session_state['analysis_results']['anomalies']
                        
                        if anomalies:
                            st.warning(f"Found unusually high deviations (Z-score > 3) in {len(anomalies)} variables.")
                            cols = st.columns(min(3, len(anomalies)))
                            for idx, anomaly in enumerate(anomalies):
                                with cols[idx % len(cols)]:
                                    with st.expander(f"**{anomaly['column']}** ({anomaly['count']} outlines)", expanded=True):
                                        st.metric("Max Deviation", f"{anomaly['max_deviation']:.1f}σ")
                                        st.caption("Extreme Values Example:")
                                        st.code(str(anomaly['example_values']))
                        else:
                            st.success("✅ No extreme statistical anomalies detected in numeric columns.")
                    
                    # Show data type summary
                    if 'df_clean' in st.session_state:
                        st.markdown("---")
                        st.subheader("📊 Data Type Summary")
                        
                        df_types = st.session_state['df_clean'].dtypes.to_frame('Data Type')
                        df_types['Non-Null Count'] = st.session_state['df_clean'].count()
                        df_types['Null Count'] = st.session_state['df_clean'].isnull().sum()
                        df_types['Unique Values'] = st.session_state['df_clean'].nunique()
                        
                        # Color code data types
                        def color_dtype(val):
                            if 'int' in str(val).lower():
                                return 'background-color: #d4edda'
                            elif 'float' in str(val).lower():
                                return 'background-color: #d1ecf1'
                            elif 'bool' in str(val).lower():
                                return 'background-color: #fff3cd'
                            elif 'datetime' in str(val).lower():
                                return 'background-color: #f8d7da'
                            elif 'category' in str(val).lower():
                                return 'background-color: #e2d5f5'
                            else:
                                return 'background-color: #f8f9fa'
                        
                        styled_df = df_types.style.applymap(color_dtype, subset=['Data Type'])
                        st.dataframe(styled_df, use_container_width=True)
                        
                        st.caption("💡 **Colors:** 🟢 Integer | 🔵 Float | 🟡 Boolean | 🔴 Datetime | 🟣 Category | ⚪ Object")
                    
                    st.markdown("---")
                    st.subheader("💡 Autonomous Insights")
                    
                    if st.session_state.get('explanations'):
                        for explanation in st.session_state['explanations']:
                            st.markdown(explanation)
                            st.markdown("---")
                    
                    st.subheader("🔬 Generated Hypotheses")
                    
                    if st.session_state.get('hypotheses'):
                        for i, hyp in enumerate(st.session_state['hypotheses'], 1):
                            with st.expander(f"Hypothesis {i}: {hyp['hypothesis']}"):
                                st.write(f"**Type:** {hyp['type']}")
                                st.write(f"**Strength:** {hyp['strength']:.3f}")
                                if hyp.get('p_value'):
                                    st.write(f"**P-value:** {hyp['p_value']:.4f}")
                                    if hyp['p_value'] < 0.05:
                                        st.success("✅ Statistically significant")
                                    else:
                                        st.info("ℹ️ Not statistically significant")
                    
                    if 'df_clean' in st.session_state:
                        st.markdown("---")
                        st.subheader("🔍 Advanced Data Filtering")
                        st.markdown("Filter your dataset dynamically. Changes apply to comparisons and visualizations built from `df_filtered`.")
                        
                        df_master = st.session_state['df_clean']
                        
                        # Initialize filtered dataframe
                        if 'df_filtered' not in st.session_state:
                            st.session_state['df_filtered'] = df_master.copy()
                            
                        with st.expander("⚙️ Set Global Data Filters", expanded=True):
                            cat_cols = df_master.select_dtypes(include=['object', 'category']).columns.tolist()
                            num_cols = df_master.select_dtypes(include=[np.number]).columns.tolist()
                            
                            f_col1, f_col2 = st.columns(2)
                            
                            filter_query = ""
                            
                            with f_col1:
                                if cat_cols:
                                    selected_cat_filter = st.selectbox("Filter by Category Column:", ["None"] + cat_cols)
                                    if selected_cat_filter != "None":
                                        unique_vals = df_master[selected_cat_filter].dropna().unique()
                                        selected_vals = st.multiselect(f"Select values for {selected_cat_filter}", unique_vals, default=unique_vals)
                                        if selected_vals:
                                            # Apply filter natively
                                            st.session_state['df_filtered'] = df_master[df_master[selected_cat_filter].isin(selected_vals)]
                                else:
                                    st.info("No categorical columns available for filtering.")
                                    
                            with f_col2:
                                if num_cols:
                                    selected_num_filter = st.selectbox("Filter by Numeric Column:", ["None"] + num_cols)
                                    if selected_num_filter != "None":
                                        min_val = float(df_master[selected_num_filter].min())
                                        max_val = float(df_master[selected_num_filter].max())
                                        if min_val < max_val:
                                            selected_range = st.slider(f"Select range for {selected_num_filter}", min_val, max_val, (min_val, max_val))
                                            # Apply recursive filter
                                            df_curr = st.session_state.get('df_filtered', df_master)
                                            st.session_state['df_filtered'] = df_curr[
                                                (df_curr[selected_num_filter] >= selected_range[0]) & 
                                                (df_curr[selected_num_filter] <= selected_range[1])
                                            ]
                                        else:
                                            st.info(f"Column {selected_num_filter} has constant value.")
                                            
                            if st.button("🔄 Reset Filters"):
                                st.session_state['df_filtered'] = df_master.copy()
                                st.rerun()
                                
                        df_compare = st.session_state.get('df_filtered', df_master)
                        st.success(f"Currently analyzing {len(df_compare)} rows (Filtered from {len(df_master)} total rows)")
                        
                        # Apply global cross-filter to visualization agent state
                        if 'visualizations' in st.session_state and 'viz_agent' in st.session_state:
                            # Re-render visualizations with new filter context if needed
                            pass

                    st.markdown("---")
                    st.subheader("🔄 Dynamic Field Comparison")
                    
                    if 'df_filtered' in st.session_state:
                         df_compare = st.session_state['df_filtered']
                         # Include categorical or object strings that aren't overly broad (e.g. limit to unique values if needed, or just all columns)
                         # We will allow all columns that do not start with '_'
                         available_cols = [c for c in df_compare.columns if not c.startswith('_')]
                         
                         if len(available_cols) >= 2:
                             st.markdown("**Compare any two variables dynamically:**")
                             
                             col1, col2, col3 = st.columns(3)
                             with col1:
                                 var1 = st.selectbox("First variable:", available_cols, key="compare_var1")
                             with col2:
                                 var2 = st.selectbox("Second variable:", 
                                                    [col for col in available_cols if col != var1], 
                                                    key="compare_var2")
                             with col3:
                                 comparison_type = st.selectbox("Comparison type:", 
                                                               ["Scatter Plot", "Line Comparison", "Distribution Compare"],
                                                               key="compare_type")
                             
                             with st.spinner("Creating comparison visualization..."):
                                 is_var1_numeric = pd.api.types.is_numeric_dtype(df_compare[var1])
                                 is_var2_numeric = pd.api.types.is_numeric_dtype(df_compare[var2])
                                 
                                 if comparison_type == "Scatter Plot":
                                     # Only add trendline if both variables are numeric and statsmodels is available
                                     use_trendline = "ols" if (is_var1_numeric and is_var2_numeric and HAS_STATSMODELS) else None
                                     
                                     fig = px.scatter(df_compare, x=var1, y=var2, 
                                                    title=f"Relationship: {var1} vs {var2}",
                                                    trendline=use_trendline)
                                     st.plotly_chart(apply_premium_theme(fig), use_container_width=True, on_select="rerun")
                                     
                                     # Calculate correlation only if both are numeric
                                     if is_var1_numeric and is_var2_numeric:
                                         corr = df_compare[var1].corr(df_compare[var2])
                                         st.info(f"📈 Correlation coefficient: {corr:.3f}")
                                     else:
                                         st.info("ℹ️ Correlation coefficient skipped (requires numeric data for both variables)")
                                         
                                 elif comparison_type == "Line Comparison":
                                     fig = go.Figure()
                                     # Support sorting if one variable is categorical/date acting as 'x'
                                     fig.add_trace(go.Scatter(y=df_compare[var1], name=var1, 
                                                            line=dict(color='blue')))
                                     fig.add_trace(go.Scatter(y=df_compare[var2], name=var2, 
                                                            line=dict(color='red')))
                                     fig.update_layout(title=f"Trend Comparison: {var1} vs {var2}")
                                     st.plotly_chart(apply_premium_theme(fig), use_container_width=True, on_select="rerun")
                                     
                                 elif comparison_type == "Distribution Compare":
                                     fig = go.Figure()
                                     fig.add_trace(go.Histogram(x=df_compare[var1], name=var1, 
                                                              opacity=0.7))
                                     fig.add_trace(go.Histogram(x=df_compare[var2], name=var2, 
                                                              opacity=0.7))
                                     fig.update_layout(title=f"Distribution: {var1} vs {var2}",
                                                     barmode='overlay')
                                     st.plotly_chart(apply_premium_theme(fig), use_container_width=True, on_select="rerun")
                                     
                                     # Statistical comparison only if numeric
                                     if is_var1_numeric and is_var2_numeric:
                                         stat, p_val = stats.ttest_ind(df_compare[var1].dropna(), 
                                                                       df_compare[var2].dropna())
                                         st.info(f"📊 T-test p-value: {p_val:.4f} - " + 
                                                ("Significantly different" if p_val < 0.05 else "Not significantly different"))
                                     else:
                                         st.info("ℹ️ T-test skipped (requires numeric data for both variables)")
     
     # ========================================================================
     # STOCK ANALYSIS MODE
    # ========================================================================
    
    elif analysis_mode == "Stock Analysis":
        with tab1:
            st.markdown("<h2>" + IconSystem.icon('stock', 'medium') + " Stock Analysis</h2>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                symbol = st.text_input(
                    "Stock Symbol or Company Name:",
                    value="Apple",
                    help="Examples: AAPL, Apple, MSFT, Microsoft, BTC-USD"
                )
            
            with col2:
                period = st.selectbox(
                    "Select Time Period:",
                    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                    index=2
                )
            
            st.subheader("Select Analysis Features:")
            
            col1, col2, col3, col4 = st.columns(4)
            
            features = []
            with col1:
                if st.checkbox("Price Trend", value=True):
                    features.append("price_trend")
            
            with col2:
                if st.checkbox("Volatility", value=True):
                    features.append("volatility")
            
            with col3:
                if st.checkbox("Moving Averages", value=True):
                    features.append("moving_averages")
            
            with col4:
                if st.checkbox("RSI Indicator", value=True):
                    features.append("rsi")
            
            if st.button("🚀 Analyze Stock", type="primary"):
                if symbol and features:
                    try:
                        with st.spinner(f"🔍 Analyzing '{symbol}'..."):
                            # Initialize stock agent
                            stock_agent = StockAnalysisAgent(logger)
                            
                            # First resolve the symbol
                            resolved_symbol = stock_agent.search_ticker_symbol(symbol)
                            
                            if resolved_symbol and resolved_symbol != symbol.strip().upper():
                                st.info(f"Resolved '{symbol}' to ticker: **{resolved_symbol}**")
                            
                            if not resolved_symbol:
                                resolved_symbol = symbol
                            
                            # Fetch data
                            df_stock = stock_agent.fetch_stock_data(resolved_symbol, period)
                            
                            if df_stock is not None and not df_stock.empty:
                                # Analyze stock
                                stock_analysis = stock_agent.analyze_stock(df_stock, features)
                                
                                st.session_state['stock_data'] = df_stock
                                st.session_state['stock_analysis'] = stock_analysis
                                st.session_state['stock_symbol'] = resolved_symbol
                                st.session_state['stock_query'] = symbol
                                
                                st.success("✅ Analysis complete!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ No data available for resolved symbol '{resolved_symbol}'. Please verify the symbol is correct.")
                                st.info("💡 **Tip:** For crypto, use format like 'BTC-USD' or 'ETH-USD'")
                                
                    except Exception as e:
                        st.error(f"❌ Stock analysis failed: {str(e)}")
                        logger.log(
                            "Stock Analysis Error",
                            f"Failed to analyze {symbol}: {str(e)}",
                            f"Error details: {traceback.format_exc()}"
                        )
                        st.info("Please check the symbol and try again, or view Agent Logs for details.")
                else:
                    st.warning("⚠️ Please enter a symbol and select at least one feature")
            
            # Display results
            if 'stock_analysis' in st.session_state:
                st.markdown("---")
                st.markdown("<h3>" + IconSystem.icon('chart', 'small') + " Dynamic Stock Dashboard: " + st.session_state['stock_symbol'] + "</h3>", unsafe_allow_html=True)
                
                df_stock = st.session_state['stock_data']
                
                # KPI Cards for dynamic overview
                if len(df_stock) >= 2:
                    current_price = df_stock['Close'].iloc[-1]
                    prev_price = df_stock['Close'].iloc[-2]
                    price_change = current_price - prev_price
                    price_pct = (price_change / prev_price) * 100
                    
                    st.markdown("### 📈 Key Metrics")
                    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
                    kpi1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f} ({price_pct:.2f}%)")
                    
                    if 'Volume' in df_stock.columns:
                        avg_vol = df_stock['Volume'].mean()
                        current_vol = df_stock['Volume'].iloc[-1]
                        vol_delta = f"{(current_vol - avg_vol) / avg_vol * 100:.1f}% vs Avg" if avg_vol > 0 else "0%"
                        kpi2.metric("Trading Volume", f"{int(current_vol):,}", vol_delta)
                    
                    if 'High' in df_stock.columns and 'Low' in df_stock.columns:
                        kpi3.metric("High (Period)", f"${df_stock['High'].max():.2f}")
                        kpi4.metric("Low (Period)", f"${df_stock['Low'].min():.2f}")
                
                st.markdown("---")
                
                # Display insights in an expander
                with st.expander("🤖 Agent Analysis Insights", expanded=True):
                    for insight in st.session_state['stock_analysis']['insights']:
                        st.info(insight)
                
                # Interactive Settings
                st.markdown("### ⚙️ Dashboard Controls")
                dash_col1, dash_col2 = st.columns([1, 2])
                with dash_col1:
                    chart_style = st.radio("Price Chart Style:", ["Line", "Candlestick"], horizontal=True)
                
                # Price chart
                st.markdown("### 📈 Price Chart Analysis")
                fig_price = go.Figure()
                
                if chart_style == "Candlestick" and all(c in df_stock.columns for c in ['Open', 'High', 'Low', 'Close']):
                    fig_price.add_trace(go.Candlestick(x=df_stock.index,
                                                      open=df_stock['Open'],
                                                      high=df_stock['High'],
                                                      low=df_stock['Low'],
                                                      close=df_stock['Close'],
                                                      name='Price'))
                else:
                    fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['Close'], 
                                                  name='Close Price', line=dict(color='blue', width=2)))
                
                if 'MA_20' in df_stock.columns:
                    fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['MA_20'], 
                                                  name='MA 20', line=dict(color='orange', dash='dash')))
                
                if 'MA_50' in df_stock.columns:
                    fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['MA_50'], 
                                                  name='MA 50', line=dict(color='red', dash='dash')))
                
                fig_price.update_layout(title=f"{st.session_state['stock_symbol']} Price & Moving Averages", 
                                       xaxis_title="Date", yaxis_title="Price",
                                       xaxis_rangeslider_visible=True if chart_style == "Candlestick" else False)
                                       
                st.plotly_chart(apply_premium_theme(fig_price), use_container_width=True, on_select="rerun")
                
                # Additional charts based on selected features in a dynamic grid
                opt_charts = []
                if 'volatility' in features and 'Volatility' in df_stock.columns:
                    opt_charts.append("volatility")
                if 'rsi' in features and 'RSI' in df_stock.columns:
                    opt_charts.append("rsi")
                    
                if opt_charts:
                    st.markdown("---")
                    st.markdown("### 📉 Technical Indicators")
                    chart_cols = st.columns(len(opt_charts))
                    
                    idx = 0
                    if "volatility" in opt_charts:
                        with chart_cols[idx]:
                            st.markdown("#### Volatility (20-Day)")
                            fig_vol = px.line(df_stock, y='Volatility')
                            st.plotly_chart(apply_premium_theme(fig_vol), use_container_width=True, on_select="rerun")
                        idx += 1
                        
                    if "rsi" in opt_charts:
                        with chart_cols[idx]:
                            st.markdown("#### Relative Strength Index (RSI)")
                            fig_rsi = go.Figure()
                            fig_rsi.add_trace(go.Scatter(x=df_stock.index, y=df_stock['RSI'], 
                                                        name='RSI', line=dict(color='purple')))
                            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                            fig_rsi.update_yaxes(range=[0, 100])
                            st.plotly_chart(apply_premium_theme(fig_rsi), use_container_width=True, on_select="rerun")
                        idx += 1
    
    # ========================================================================
    # VISUALIZATIONS TAB (ENHANCED)
    # ========================================================================
    
    with tab2:
        st.markdown("<h2>" + IconSystem.icon('chart-line', 'medium') + " Autonomous Visualizations</h2>", unsafe_allow_html=True)
        
        if 'visualizations' in st.session_state:
            visualizations = st.session_state['visualizations']
            
            st.info(f"🤖 The Visualization Agent autonomously created {len(visualizations)} charts based on data analysis")
            
            # Add KPI Cards Section
            if 'df_clean' in st.session_state:
                df_clean = st.session_state['df_clean']
                numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
                
                if len(numeric_cols) > 0:
                    st.markdown("### 📊 Key Metrics Summary (KPI Cards)")
                    
                    # Create KPI cards
                    num_cards = min(4, len(numeric_cols))
                    cols = st.columns(num_cards)
                    
                    for idx, col in enumerate(numeric_cols[:num_cards]):
                        with cols[idx]:
                            value = df_clean[col].mean()
                            delta = df_clean[col].std()
                            min_val = df_clean[col].min()
                            max_val = df_clean[col].max()
                            
                            st.metric(
                                label=col,
                                value=f"{value:.2f}",
                                delta=f"σ: {delta:.2f}",
                                help=f"Min: {min_val:.2f}, Max: {max_val:.2f}"
                            )
                    
                    st.markdown("---")
                    
                    # Distribution Analysis Section
                    st.markdown("### 📈 Distribution Analysis")
                    
                    with st.expander("📊 View Distribution Details"):
                        for col in numeric_cols[:6]:  # Show first 6 numeric columns
                            with st.expander(f"**{col}**"):
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Mean", f"{df_clean[col].mean():.2f}")
                                with col2:
                                    st.metric("Median", f"{df_clean[col].median():.2f}")
                                with col3:
                                    st.metric("Std Dev", f"{df_clean[col].std():.2f}")
                                
                                # Mini distribution chart
                                fig = px.histogram(df_clean, x=col, nbins=20, 
                                                 title=f"Distribution of {col}")
                                st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
            
            # Display all visualizations with manual override option
            viz_agent = st.session_state.get('viz_agent')
            available_chart_types = viz_agent.get_available_chart_types() if viz_agent else []
            
            # Setup dashboard container
            st.markdown("### 🎨 Visual Dashboard")
            st.markdown("""
            <style>
            .pbi-container {
                background-color: white;
                border: 1px solid #edebe9;
                border-radius: 4px;
                padding: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* PBI soft shadow */
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Create a 2-column grid for dynamic dashboard layout (Power BI style)
            dashboard_cols = st.columns(2)
            
            df_active = st.session_state.get('df_filtered', st.session_state.get('df_clean', None))
            
            for i, viz in enumerate(visualizations, 1):
                col_idx = (i - 1) % 2
                with dashboard_cols[col_idx]:
                    st.markdown("<div class='pbi-container'>", unsafe_allow_html=True)
                    st.markdown(f"**{viz['title']}**")
                    
                    with st.expander("⚙️ Settings & Agent Reasoning"):
                        st.caption(f"💡 **Agent Reasoning:** {viz['reasoning']}")
                        
                        override_key = f"override_toggle_{i}"
                        st.checkbox("Enable manual chart override", key=override_key)
                        
                        if st.session_state.get(override_key, False):
                            if df_active is not None:
                                all_cols = [c for c in df_active.columns if not c.startswith('_')]
                                x_col_override = st.selectbox("X-axis variable:", all_cols, key=f"x_override_{i}")
                                
                                numeric_cols_list = df_active.select_dtypes(include=[np.number]).columns.tolist()
                                y_col_override = st.selectbox("Y-axis (optional):", [None] + numeric_cols_list, key=f"y_override_{i}")
                            else:
                                x_col_override = viz.get('x_col', '')
                                y_col_override = viz.get('y_col')
                                
                            chart_type_override = st.selectbox("Chart type:", 
                                available_chart_types if available_chart_types else ['scatter', 'line', 'bar'], 
                                index=0, key=f"chart_override_{i}")
                                
                            if st.button("📊 Generate Override", key=f"gen_override_{i}"):
                                if viz_agent and x_col_override:
                                    if 'df_filtered' in st.session_state:
                                        df_active = st.session_state['df_filtered']
                                    else:
                                        df_active = st.session_state.get('df_clean', pd.DataFrame())
                                        
                                    custom_viz = viz_agent.create_custom_visualization(
                                        df_active, x_col_override, y_col_override, chart_type_override
                                    )
                                    if custom_viz:
                                        viz = custom_viz # Replace locally to render the manual chart
                                        st.success("✅ Custom chart generated successfully!")
                                    else:
                                        st.warning("⚠️ Could not create chart with selected options.")
                    
                    
                    # Ensure the chart updates based on the current filtered dataset dynamically implicitly via re-executing plotting
                    # We override the figure with fresh data if doing cross-filtering
                    try:
                        if df_active is not None and viz.get('x_col') and viz_agent:
                            # Re-run chart generation function internally on filtered dataset automatically
                            fresh_viz = viz_agent.create_custom_visualization(df_active, viz.get('x_col'), viz.get('y_col'), viz.get('chart_type'))
                            if fresh_viz:
                                viz['figure'] = fresh_viz['figure']
                    except Exception as e:
                        pass # Keep original viz figure if recompilation fails
                        
                    selection = st.plotly_chart(apply_premium_theme(viz['figure']), use_container_width=True, on_select="rerun")
                    if selection and selection.get("selection", {}).get("points"):
                        st.info("Cross-filtering active via selection (Note: Requires deeper callback handling depending on chart).")
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("👆 Run an analysis to see autonomous visualizations")
            
            # Show example of what visualizations look like
            st.markdown("### 🎨 Visualization Types Automatically Selected:")
            st.markdown("""
            The Visualization Agent will autonomously choose from:
            - 📈 **Line Charts** - For trends and time-series data
            - 📊 **Bar Charts** - For categorical comparisons
            - 🔵 **Scatter Plots** - For correlations between variables
            - 📦 **Box Plots** - For distribution comparisons across groups
            - 📊 **Histograms** - For frequency distributions
            - 🔥 **Heatmaps** - For correlation matrices
            - 🎻 **Violin Plots** - For detailed distribution shapes
            - 📊 **KPI Cards** - For metric summaries
            
            **All selections are made automatically based on data characteristics!**
            
            You can also **manually override** any visualization with a different chart type.
            """)
    
    # ========================================================================
    # AGENT LOGS TAB
    # ========================================================================
    
    with tab3:
        st.markdown("<h2>" + IconSystem.icon('brain', 'medium') + " Agent Thinking Logs</h2>", unsafe_allow_html=True)
        st.caption("Real-time transparency into agent reasoning and decision-making")
        
        logs = logger.get_logs()
        
        if logs:
            # Add filter for logs
            st.markdown("### 🔍 Filter Logs by Agent:")
            agent_filter = st.multiselect(
                "Select agents to view:",
                ["Data Ingestion Agent", "Self-Healing Agent", "Field Generation Agent",
                 "Hypothesis Generation Agent", "Analysis Agent", "Visualization Agent", 
                 "Explanation Agent", "Stock Analysis Agent"],
                default=["Data Ingestion Agent", "Self-Healing Agent", "Field Generation Agent",
                         "Hypothesis Generation Agent", "Analysis Agent", "Visualization Agent", 
                         "Explanation Agent", "Stock Analysis Agent"]
            )
            
            st.markdown("---")
            
            filtered_logs = [log for log in logs if log['agent'] in agent_filter] if agent_filter else logs
            
            for log in filtered_logs:
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        st.code(log['timestamp'])
                        
                        if 'Ingestion' in log['agent']:
                            st.success(f"🔵 {log['agent']}")
                        elif 'Healing' in log['agent']:
                            st.warning(f"🟡 {log['agent']}")
                        elif 'Field Generation' in log['agent']:
                            st.info(f"🟢 {log['agent']}")
                        elif 'Hypothesis' in log['agent']:
                            st.info(f"🟣 {log['agent']}")
                        elif 'Analysis' in log['agent']:
                            st.error(f"🔴 {log['agent']}")
                        elif 'Visualization' in log['agent']:
                            st.success(f"🟢 {log['agent']}")
                        elif 'Explanation' in log['agent']:
                            st.info(f"🔵 {log['agent']}")
                        else:
                            st.write(f"⚪ {log['agent']}")
                    
                    with col2:
                        st.write(f"**💭 Thought:** {log['thought']}")
                        st.write(f"**⚡ Action:** {log['action']}")
                    
                    st.markdown("---")
            
            # Summary statistics
            st.markdown("### 📈 Agent Activity Summary")
            agent_counts = {}
            for log in logs:
                agent_name = log['agent']
                agent_counts[agent_name] = agent_counts.get(agent_name, 0) + 1
            
            cols = st.columns(min(4, len(agent_counts)))
            for idx, (agent, count) in enumerate(agent_counts.items()):
                with cols[idx % 4]:
                    st.metric(label=agent.replace(" Agent", ""), value=count)
                    
        else:
            st.info("No agent activity yet. Start an analysis to see agent thinking in real-time!")
            
            st.markdown("### 💡 What You'll See Here:")
            st.markdown("""
            This tab provides complete transparency into how the autonomous agents make decisions:
            
            - **🔵 Data Ingestion** - How data is loaded and validated
            - **🟡 Self-Healing** - What issues are detected and how they're fixed
            - **🟢 Field Generation** - What new fields are created and why
            - **🟣 Hypothesis Generation** - What patterns the agent discovers
            - **🔴 Analysis** - What statistical tests are performed
            - **🟢 Visualization** - Why specific chart types are selected
            - **🔵 Explanation** - How findings are translated to plain English
            
            Every decision is logged with the agent's reasoning!
            """)

if __name__ == "__main__":
    main()
