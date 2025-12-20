"""
🤖 Autonomous Data Analysis System
A council of intelligent agents for autonomous data analysis, hypothesis generation, and visualization
NO EXTERNAL AI MODELS - Pure intelligent rule-based system
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
from typing import List, Dict, Tuple, Optional
import io
import traceback
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOGGING SYSTEM - Agent Thinking Transparency
# ============================================================================

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
# AGENT 1: DATA INGESTION AGENT
# ============================================================================

class DataIngestionAgent:
    """Validates, cleans, and structures incoming data"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.issues_detected = []
        self.fixes_applied = []
    
    def ingest_csv(self, file) -> pd.DataFrame:
        """Load and validate CSV/Excel file"""
        self.logger.log(
            "Data Ingestion Agent",
            "Starting data ingestion from uploaded file",
            "Reading file and detecting format"
        )
        
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            self.logger.log(
                "Data Ingestion Agent",
                f"Successfully loaded {len(df)} rows and {len(df.columns)} columns",
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
            if missing_count > 0:
                validation_report['missing_values'][col] = missing_count
                self.issues_detected.append(f"⚠️ Missing values in '{col}' column ({missing_count} rows)")
        
        # Check duplicates
        duplicate_count = df.duplicated().sum()
        if duplicate_count > 0:
            validation_report['duplicate_rows'] = duplicate_count
            self.issues_detected.append(f"⚠️ {duplicate_count} duplicate rows found")
        
        # Data types
        validation_report['data_types'] = df.dtypes.to_dict()
        
        # Column statistics
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                validation_report['column_stats'][col] = {
                    'mean': df[col].mean(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'median': df[col].median()
                }
        
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
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
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
            
            # 5. Remove zero-variance columns
            df_clean = self._remove_zero_variance(df_clean)
            
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
    
    def _try_datetime_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to datetime"""
        # Check if values look like dates
        date_patterns = ['-', '/', ':', 'T', 'Z']
        has_date_chars = any(any(p in str(v) for p in date_patterns) for v in sample_values[:3])
        
        if has_date_chars:
            try:
                # Try multiple datetime formats
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
                # Check if conversion was successful (at least 50% valid dates)
                valid_ratio = df[col].notna().sum() / len(df)
                if valid_ratio > 0.5:
                    self.fixes_applied.append(f"✅ Converted '{col}' to datetime type")
                    return True
                else:
                    # Revert if conversion failed
                    df[col] = df[col].astype(str)
                    return False
            except:
                return False
        return False
    
    def _try_boolean_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to boolean"""
        unique_values = set(str(v).lower().strip() for v in sample_values)
        boolean_values = {'true', 'false', 't', 'f', 'yes', 'no', 'y', 'n', '1', '0', '1.0', '0.0'}
        
        if unique_values.issubset(boolean_values) and len(unique_values) <= 4:
            try:
                # Create mapping
                bool_map = {
                    'true': True, 't': True, 'yes': True, 'y': True, '1': True, '1.0': True,
                    'false': False, 'f': False, 'no': False, 'n': False, '0': False, '0.0': False
                }
                
                df[col] = df[col].astype(str).str.lower().str.strip().map(bool_map)
                self.fixes_applied.append(f"✅ Converted '{col}' to boolean type")
                return True
            except:
                return False
        return False
    
    def _try_integer_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to integer"""
        try:
            # First convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Check if all non-null values are integers
            non_null = df[col].dropna()
            if len(non_null) > 0 and (non_null == non_null.astype(int)).all():
                df[col] = df[col].astype('Int64')  # Nullable integer type
                self.fixes_applied.append(f"✅ Converted '{col}' to integer type")
                return True
            elif len(non_null) > 0:
                # Keep as float if has decimal values
                self.fixes_applied.append(f"✅ Converted '{col}' to numeric (float) type")
                return True
        except:
            return False
        return False
    
    def _try_float_conversion(self, df: pd.DataFrame, col: str, sample_values: list) -> bool:
        """Try to convert column to float"""
        try:
            # Remove common non-numeric characters
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('$', '').str.replace('%', '').str.strip()
            
            # Try numeric conversion
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Check if conversion was successful (at least 70% valid numbers)
            valid_ratio = df[col].notna().sum() / len(df)
            if valid_ratio > 0.7:
                self.fixes_applied.append(f"✅ Converted '{col}' to numeric type (removed special characters)")
                return True
            else:
                return False
        except:
            return False
    
    def _try_category_conversion(self, df: pd.DataFrame, col: str) -> bool:
        """Try to convert low-cardinality string columns to category"""
        if df[col].dtype == 'object':
            unique_ratio = df[col].nunique() / len(df)
            
            # Convert to category if low cardinality (< 50% unique values)
            if unique_ratio < 0.5 and df[col].nunique() < 100:
                try:
                    df[col] = df[col].astype('category')
                    self.fixes_applied.append(f"✅ Converted '{col}' to category type (optimized for {df[col].nunique()} unique values)")
                    return True
                except:
                    return False
        return False
    
    def _clean_string_column(self, df: pd.DataFrame, col: str):
        """Clean string columns"""
        try:
            # Remove leading/trailing whitespace
            original = df[col].copy()
            df[col] = df[col].astype(str).str.strip()
            
            # Check if cleaning made a difference
            if not df[col].equals(original):
                self.fixes_applied.append(f"✅ Cleaned whitespace in '{col}'")
        except:
            pass
    
    def _remove_zero_variance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove columns with zero variance"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cols_to_drop = []
        
        for col in numeric_cols:
            if df[col].std() == 0:
                cols_to_drop.append(col)
        
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)
            self.fixes_applied.append(f"✅ Removed {len(cols_to_drop)} zero-variance columns: {cols_to_drop}")
        
        return df

# ============================================================================
# AGENT 3: FIELD GENERATION AGENT (NEW)
# ============================================================================

class FieldGenerationAgent:
    """Autonomously generates missing fields from existing data"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
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
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.hypotheses = []
    
    def generate_hypotheses(self, df: pd.DataFrame) -> List[Dict]:
        """Autonomously generate testable hypotheses"""
        self.logger.log(
            "Hypothesis Generation Agent",
            "Analyzing data to discover patterns and relationships",
            "Generating testable hypotheses"
        )
        
        self.hypotheses = []
        
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
            f"Generated {len(self.hypotheses)} testable hypotheses",
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
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
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

# ============================================================================
# AGENT 6: VISUALIZATION AGENT
# ============================================================================

class VisualizationAgent:
    """Autonomously selects optimal chart types and creates visualizations"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.visualizations = []
    
    def create_visualizations(self, df: pd.DataFrame, hypotheses: List[Dict]) -> List[Dict]:
        """Autonomously decide and create visualizations"""
        self.logger.log(
            "Visualization Agent",
            "Analyzing data characteristics to select optimal visualizations",
            "Deciding chart types based on data patterns"
        )
        
        self.visualizations = []
        
        # Create visualizations based on hypotheses
        for hyp in hypotheses:
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
    
    def _select_and_create_viz(self, df: pd.DataFrame, hypothesis: Dict) -> Dict:
        """Intelligently select chart type based on hypothesis"""
        hyp_type = hypothesis['type']
        variables = hypothesis['variables']
        
        if hyp_type == 'correlation' and len(variables) == 2:
            # Scatter plot for correlation
            fig = px.scatter(df, x=variables[0], y=variables[1], 
                           title=f"Correlation: {variables[0]} vs {variables[1]}")
            
            # Add manual trendline using numpy
            x_data = df[variables[0]].dropna()
            y_data = df[variables[1]].dropna()
            if len(x_data) > 1 and len(y_data) > 1:
                # Align the data
                combined = pd.DataFrame({variables[0]: df[variables[0]], variables[1]: df[variables[1]]}).dropna()
                if len(combined) > 1:
                    z = np.polyfit(combined[variables[0]], combined[variables[1]], 1)
                    p = np.poly1d(z)
                    fig.add_trace(go.Scatter(
                        x=combined[variables[0]].sort_values(),
                        y=p(combined[variables[0]].sort_values()),
                        mode='lines',
                        name='Trendline',
                        line=dict(color='red', dash='dash')
                    ))
            
            self.logger.log(
                "Visualization Agent",
                f"Selected scatter plot for correlation between {variables[0]} and {variables[1]}",
                "Scatter plots best show relationships between two numeric variables"
            )
            
            return {
                'chart_type': 'scatter',
                'figure': fig,
                'title': f"{variables[0]} vs {variables[1]}",
                'reasoning': 'Scatter plot selected to visualize correlation between two numeric variables'
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
                'reasoning': 'Line chart selected to visualize trend over time/sequence'
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
                'reasoning': 'Histogram selected to show frequency distribution'
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
                'reasoning': 'Box plot selected to compare distributions across groups'
            }
        
        return None
    
    def _create_overview_visualizations(self, df: pd.DataFrame):
        """Create general overview visualizations"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Correlation heatmap if multiple numeric columns
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, 
                           title="Correlation Heatmap",
                           color_continuous_scale="RdBu",
                           aspect="auto")
            
            self.logger.log(
                "Visualization Agent",
                "Created correlation heatmap for all numeric variables",
                "Heatmap provides overview of all relationships"
            )
            
            self.visualizations.append({
                'chart_type': 'heatmap',
                'figure': fig,
                'title': 'Correlation Matrix',
                'reasoning': 'Heatmap selected to show all pairwise correlations at once'
            })

# ============================================================================
# AGENT 7: EXPLANATION AGENT
# ============================================================================

class ExplanationAgent:
    """Translates technical findings into plain English"""
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
        self.explanations = []
    
    def explain_findings(self, df: pd.DataFrame, hypotheses: List[Dict], 
                        analysis_results: Dict) -> List[str]:
        """Generate plain-English explanations"""
        self.logger.log(
            "Explanation Agent",
            "Translating technical findings to plain English",
            "Creating non-technical explanations"
        )
        
        self.explanations = []
        
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
    
    def __init__(self, logger: AgentLogger):
        self.logger = logger
    
    def fetch_stock_data(self, symbol: str, period: str) -> pd.DataFrame:
        """Fetch stock/crypto data"""
        self.logger.log(
            "Stock Analysis Agent",
            f"Fetching market data for {symbol}",
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
        page_title="🤖 Autonomous Data Analysis System",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Autonomous Data Analysis System")
    st.markdown("### Council of Intelligent Agents - No External AI Models")
    
    # Initialize logger
    logger = AgentLogger()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        
        analysis_mode = st.radio(
            "Select Analysis Mode:",
            ["📊 Report Analysis", "📈 Stock Analysis"]
        )
        
        st.markdown("---")
        st.markdown("### 🤖 Agent Status")
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
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "📈 Visualizations", "🧠 Agent Logs"])
    
    # ========================================================================
    # REPORT ANALYSIS MODE
    # ========================================================================
    
    if analysis_mode == "📊 Report Analysis":
        with tab1:
            st.header("📊 Report Analysis")
            
            # File upload
            st.subheader("1️⃣ Upload Your Data")
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file",
                type=['csv', 'xlsx', 'xls'],
                help="Upload your dataset for autonomous analysis"
            )
            
            # Sample data option
            use_sample = st.checkbox("Use sample dataset (Iris)")
            
            if use_sample:
                from sklearn.datasets import load_iris
                iris = load_iris()
                df = pd.DataFrame(iris.data, columns=iris.feature_names)
                df['species'] = iris.target
                st.success("✅ Loaded sample Iris dataset")
            elif uploaded_file:
                # Initialize agents
                ingestion_agent = DataIngestionAgent(logger)
                df = ingestion_agent.ingest_csv(uploaded_file)
                
                if df is not None:
                    st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
                else:
                    st.error("❌ Failed to load file")
                    df = None
            else:
                df = None
            
            if df is not None:
                # Show data preview
                with st.expander("📋 Data Preview"):
                    st.dataframe(df.head(10))
                
                st.markdown("---")
                st.subheader("2️⃣ Select Variables to Analyze")
                
                all_columns = list(df.columns)
                selected_columns = st.multiselect(
                    "Choose variables for analysis:",
                    all_columns,
                    default=all_columns[:min(5, len(all_columns))]
                )
                
                # Field Generation Section
                st.markdown("---")
                st.subheader("🔧 Generate New Fields (Optional)")
                
                with st.expander("✨ Auto-Generate Derived Fields"):
                    st.markdown("**The Field Generation Agent can create new variables from existing data:**")
                    
                    field_gen_agent = FieldGenerationAgent(logger)
                    suggestions = field_gen_agent.suggest_derivable_fields(df[selected_columns] if selected_columns else df)
                    
                    if suggestions:
                        st.markdown("**Suggested fields you can generate:**")
                        for i, sug in enumerate(suggestions[:6], 1):  # Show top 6 suggestions
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"{i}. **{sug['name']}** - {sug['description']}")
                            with col2:
                                if st.button(f"Generate", key=f"gen_{i}"):
                                    df = field_gen_agent.generate_field(df, sug['name'], sug['type'])
                                    st.session_state['df_modified'] = df
                                    st.success(f"✅ Generated '{sug['name']}'")
                                    st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**Or create a custom field:**")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        custom_field_name = st.text_input(
                            "New field name:",
                            placeholder="e.g., profit_margin, growth_rate"
                        )
                    
                    with col2:
                        derivation_type = st.selectbox(
                            "Derivation type:",
                            ['auto', 'ratio', 'difference', 'sum', 'average', 
                             'percent_change', 'rolling_average', 'normalized', 
                             'cumulative_sum', 'squared', 'logarithm']
                        )
                    
                    if st.button("🚀 Generate Custom Field"):
                        if custom_field_name:
                            field_gen_agent = FieldGenerationAgent(logger)
                            df = field_gen_agent.generate_field(df, custom_field_name, derivation_type)
                            st.session_state['df_modified'] = df
                            
                            if custom_field_name in df.columns:
                                st.success(f"✅ Successfully generated field: '{custom_field_name}'")
                                if field_gen_agent.derivation_log:
                                    st.info(f"📝 {field_gen_agent.derivation_log[-1]}")
                                st.rerun()
                            else:
                                st.warning("⚠️ Field generation attempted but not successful")
                        else:
                            st.warning("Please enter a field name")
                
                # Update selected columns to include generated fields
                if 'df_modified' in st.session_state:
                    df = st.session_state['df_modified']
                    all_columns = list(df.columns)
                    
                    # Show generated fields badge
                    if hasattr(field_gen_agent, 'generated_fields') and field_gen_agent.generated_fields:
                        st.success(f"🎉 {len(field_gen_agent.generated_fields)} field(s) generated and ready for analysis")
                
                st.markdown("---")
                
                if st.button("🚀 Run Autonomous Analysis", type="primary"):
                    if selected_columns:
                        df_analysis = df[selected_columns].copy()
                        
                        try:
                            # Show initial data types
                            with st.expander("📋 Initial Data Types"):
                                st.dataframe(df_analysis.dtypes.to_frame('Original Data Type'))
                            
                            with st.spinner("🤖 Agents are working..."):
                                # Data Ingestion Agent
                                ingestion_agent = DataIngestionAgent(logger)
                                validation_report = ingestion_agent.validate_data(df_analysis)
                                
                                # Self-Healing Agent with progress indicator
                                with st.spinner("🔧 Self-Healing Agent: Fixing data types and quality issues..."):
                                    healing_agent = SelfHealingAgent(logger)
                                    df_clean = healing_agent.heal_data(df_analysis)
                                
                                # Store issues and fixes
                                st.session_state['issues'] = ingestion_agent.issues_detected
                                st.session_state['fixes'] = healing_agent.fixes_applied
                                
                                # Show corrected data types
                                if healing_agent.fixes_applied:
                                    with st.expander("✅ Corrected Data Types"):
                                        st.dataframe(df_clean.dtypes.to_frame('Corrected Data Type'))
                                
                                # Hypothesis Generation Agent
                                hypothesis_agent = HypothesisGenerationAgent(logger)
                                hypotheses = hypothesis_agent.generate_hypotheses(df_clean)
                                st.session_state['hypotheses'] = hypotheses
                                
                                # Analysis Agent
                                analysis_agent = AnalysisAgent(logger)
                                analysis_results = analysis_agent.analyze_data(df_clean, hypotheses)
                                st.session_state['analysis_results'] = analysis_results
                                
                                # Visualization Agent
                                viz_agent = VisualizationAgent(logger)
                                visualizations = viz_agent.create_visualizations(df_clean, hypotheses)
                                st.session_state['visualizations'] = visualizations
                                
                                # Explanation Agent
                                explanation_agent = ExplanationAgent(logger)
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
                    st.subheader("🔍 Data Quality Report")
                    
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
                            for fix in st.session_state['fixes']:
                                st.success(fix)
                        else:
                            st.info("No fixes needed")
                    
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
                    
                    st.markdown("---")
                    st.subheader("🔄 Dynamic Field Comparison")
                    
                    if 'df_clean' in st.session_state:
                        df_compare = st.session_state['df_clean']
                        numeric_cols = df_compare.select_dtypes(include=[np.number]).columns.tolist()
                        
                        if len(numeric_cols) >= 2:
                            st.markdown("**Compare any two variables dynamically:**")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                var1 = st.selectbox("First variable:", numeric_cols, key="compare_var1")
                            with col2:
                                var2 = st.selectbox("Second variable:", 
                                                   [col for col in numeric_cols if col != var1], 
                                                   key="compare_var2")
                            with col3:
                                comparison_type = st.selectbox("Comparison type:", 
                                                              ["Scatter Plot", "Line Comparison", "Distribution Compare"],
                                                              key="compare_type")
                            
                            if st.button("📊 Generate Comparison", key="generate_compare"):
                                with st.spinner("Creating comparison visualization..."):
                                    if comparison_type == "Scatter Plot":
                                        fig = px.scatter(df_compare, x=var1, y=var2, 
                                                       title=f"Relationship: {var1} vs {var2}")
                                        
                                        # Add manual trendline using numpy
                                        combined = df_compare[[var1, var2]].dropna()
                                        if len(combined) > 1:
                                            z = np.polyfit(combined[var1], combined[var2], 1)
                                            p = np.poly1d(z)
                                            fig.add_trace(go.Scatter(
                                                x=combined[var1].sort_values(),
                                                y=p(combined[var1].sort_values()),
                                                mode='lines',
                                                name='Trendline',
                                                line=dict(color='red', dash='dash')
                                            ))
                                        
                                        st.plotly_chart(fig, use_container_width=True)
                                        
                                        # Calculate correlation
                                        corr = df_compare[var1].corr(df_compare[var2])
                                        st.info(f"📈 Correlation coefficient: {corr:.3f}")
                                        
                                    elif comparison_type == "Line Comparison":
                                        fig = go.Figure()
                                        fig.add_trace(go.Scatter(y=df_compare[var1], name=var1, 
                                                               line=dict(color='blue')))
                                        fig.add_trace(go.Scatter(y=df_compare[var2], name=var2, 
                                                               line=dict(color='red')))
                                        fig.update_layout(title=f"Trend Comparison: {var1} vs {var2}")
                                        st.plotly_chart(fig, use_container_width=True)
                                        
                                    elif comparison_type == "Distribution Compare":
                                        fig = go.Figure()
                                        fig.add_trace(go.Histogram(x=df_compare[var1], name=var1, 
                                                                 opacity=0.7))
                                        fig.add_trace(go.Histogram(x=df_compare[var2], name=var2, 
                                                                 opacity=0.7))
                                        fig.update_layout(title=f"Distribution: {var1} vs {var2}",
                                                        barmode='overlay')
                                        st.plotly_chart(fig, use_container_width=True)
                                        
                                        # Statistical comparison
                                        stat, p_val = stats.ttest_ind(df_compare[var1].dropna(), 
                                                                      df_compare[var2].dropna())
                                        st.info(f"📊 T-test p-value: {p_val:.4f} - " + 
                                               ("Significantly different" if p_val < 0.05 else "Not significantly different"))
    
    # ========================================================================
    # STOCK ANALYSIS MODE
    # ========================================================================
    
    elif analysis_mode == "📈 Stock Analysis":
        with tab1:
            st.header("📈 Stock Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                symbol = st.text_input(
                    "Enter Stock Symbol:",
                    value="AAPL",
                    help="Examples: AAPL, TSLA"
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
                        with st.spinner("📊 Fetching and analyzing data..."):
                            # Initialize stock agent
                            stock_agent = StockAnalysisAgent(logger)
                            
                            # Fetch data
                            df_stock = stock_agent.fetch_stock_data(symbol, period)
                            
                            if df_stock is not None and not df_stock.empty:
                                # Analyze stock
                                stock_analysis = stock_agent.analyze_stock(df_stock, features)
                                
                                st.session_state['stock_data'] = df_stock
                                st.session_state['stock_analysis'] = stock_analysis
                                st.session_state['stock_symbol'] = symbol
                                
                                st.success("✅ Analysis complete!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(f"❌ No data available for symbol '{symbol}'. Please verify the symbol is correct.")
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
                st.subheader(f"📊 Analysis Results: {st.session_state['stock_symbol']}")
                
                # Display insights
                for insight in st.session_state['stock_analysis']['insights']:
                    st.info(insight)
                
                st.markdown("---")
                
                # Create visualizations
                df_stock = st.session_state['stock_data']
                
                # Price chart
                st.subheader("📈 Price Chart")
                fig_price = go.Figure()
                fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['Close'], 
                                              name='Close Price', line=dict(color='blue', width=2)))
                
                if 'MA_20' in df_stock.columns:
                    fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['MA_20'], 
                                                  name='MA 20', line=dict(color='orange', dash='dash')))
                
                if 'MA_50' in df_stock.columns:
                    fig_price.add_trace(go.Scatter(x=df_stock.index, y=df_stock['MA_50'], 
                                                  name='MA 50', line=dict(color='red', dash='dash')))
                
                fig_price.update_layout(title="Price with Moving Averages", 
                                       xaxis_title="Date", yaxis_title="Price ($)")
                st.plotly_chart(fig_price, use_container_width=True)
                
                # Additional charts based on selected features
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'volatility' in features and 'Volatility' in df_stock.columns:
                        st.subheader("📊 Volatility")
                        fig_vol = px.line(df_stock, y='Volatility', title="20-Day Volatility")
                        st.plotly_chart(fig_vol, use_container_width=True)
                
                with col2:
                    if 'rsi' in features and 'RSI' in df_stock.columns:
                        st.subheader("📊 RSI Indicator")
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(x=df_stock.index, y=df_stock['RSI'], 
                                                    name='RSI', line=dict(color='purple')))
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                        fig_rsi.update_layout(title="Relative Strength Index (RSI)")
                        st.plotly_chart(fig_rsi, use_container_width=True)
    
    # ========================================================================
    # VISUALIZATIONS TAB
    # ========================================================================
    
    with tab2:
        st.header("📈 Autonomous Visualizations")
        
        if 'visualizations' in st.session_state:
            visualizations = st.session_state['visualizations']
            
            st.info(f"🤖 The Visualization Agent autonomously created {len(visualizations)} charts based on data analysis")
            
            # Add KPI Cards Section
            if 'df_clean' in st.session_state:
                df_clean = st.session_state['df_clean']
                numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
                
                if len(numeric_cols) > 0:
                    st.markdown("### 📊 Key Metrics Summary")
                    
                    # Create KPI cards
                    num_cards = min(4, len(numeric_cols))
                    cols = st.columns(num_cards)
                    
                    for idx, col in enumerate(numeric_cols[:num_cards]):
                        with cols[idx]:
                            value = df_clean[col].mean()
                            delta = df_clean[col].std()
                            
                            st.metric(
                                label=col,
                                value=f"{value:.2f}",
                                delta=f"σ: {delta:.2f}"
                            )
                    
                    st.markdown("---")
            
            # Display all visualizations
            for i, viz in enumerate(visualizations, 1):
                st.subheader(f"{i}. {viz['title']}")
                st.caption(f"💡 **Agent Reasoning:** {viz['reasoning']}")
                st.plotly_chart(viz['figure'], use_container_width=True)
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
            - 📊 **KPI Cards** - For metric summaries
            
            **All selections are made automatically based on data characteristics!**
            """)
    
    # ========================================================================
    # AGENT LOGS TAB
    # ========================================================================
    
    with tab3:
        st.header("🧠 Agent Thinking Logs")
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
