1932-            if df is not None and len(df) > 0:
1933-                # Show data preview
1934:                with st.expander("📋 Data Preview"):
1935-                    st.dataframe(df.head(10))
1936-                
1937-                st.markdown("---")
1938-                st.subheader("2️⃣ Select Variables to Analyze")
1939-                
--
1952-                st.subheader("🔧 Generate New Fields (Optional)")
1953-                
1954:                with st.expander("✨ Auto-Generate Derived Fields"):
1955-                    st.markdown("**The Field Generation Agent can create new variables from existing data:**")
1956-                    
1957-                    field_gen_agent = FieldGenerationAgent(logger)
1958-                    suggestions = field_gen_agent.suggest_derivable_fields(df[selected_columns] if selected_columns else df)
1959-                    
--
2025-                        try:
2026-                            # Show initial data types
2027:                            with st.expander("📋 Initial Data Types"):
2028-                                st.dataframe(df_analysis.dtypes.to_frame('Original Data Type'))
2029-                            
2030-                            with st.spinner("🤖 Agents are working... This may take a moment"):
2031-                                # Data Ingestion Agent
2032-                                ingestion_agent = DataIngestionAgent(logger)
--
2054-                                # Show corrected data types
2055-                                if healing_agent.fixes_applied:
2056:                                    with st.expander("✅ Corrected Data Types"):
2057-                                        st.dataframe(df_clean.dtypes.to_frame('Corrected Data Type'))
2058-                                
2059-                                # Hypothesis Generation Agent
2060-                                hypothesis_agent = HypothesisGenerationAgent(logger)
2061-                                hypotheses = hypothesis_agent.generate_hypotheses(df_clean)
--
2144-                            for idx, anomaly in enumerate(anomalies):
2145-                                with cols[idx % len(cols)]:
2146:                                    with st.expander(f"**{anomaly['column']}** ({anomaly['count']} outlines)", expanded=True):
2147-                                        st.metric("Max Deviation", f"{anomaly['max_deviation']:.1f}σ")
2148-                                        st.caption("Extreme Values Example:")
2149-                                        st.code(str(anomaly['example_values']))
2150-                        else:
2151-                            st.success("✅ No extreme statistical anomalies detected in numeric columns.")
--
2193-                    if st.session_state.get('hypotheses'):
2194-                        for i, hyp in enumerate(st.session_state['hypotheses'], 1):
2195:                            with st.expander(f"Hypothesis {i}: {hyp['hypothesis']}"):
2196-                                st.write(f"**Type:** {hyp['type']}")
2197-                                st.write(f"**Strength:** {hyp['strength']:.3f}")
2198-                                if hyp.get('p_value'):
2199-                                    st.write(f"**P-value:** {hyp['p_value']:.4f}")
2200-                                    if hyp['p_value'] < 0.05:
--
2214-                            st.session_state['df_filtered'] = df_master.copy()
2215-                            
2216:                        with st.expander("⚙️ Set Global Data Filters", expanded=True):
2217-                            cat_cols = df_master.select_dtypes(include=['object', 'category']).columns.tolist()
2218-                            num_cols = df_master.select_dtypes(include=[np.number]).columns.tolist()
2219-                            
2220-                            f_col1, f_col2 = st.columns(2)
2221-                            
--
2453-                
2454-                # Display insights in an expander
2455:                with st.expander("🤖 Agent Analysis Insights", expanded=True):
2456-                    for insight in st.session_state['stock_analysis']['insights']:
2457-                        st.info(insight)
2458-                
2459-                # Interactive Settings
2460-                st.markdown("### ⚙️ Dashboard Controls")
--
2567-                    st.markdown("### 📈 Distribution Analysis")
2568-                    
2569:                    with st.expander("📊 View Distribution Details"):
2570-                        for col in numeric_cols[:6]:  # Show first 6 numeric columns
2571:                            with st.expander(f"**{col}**"):
2572-                                col1, col2, col3 = st.columns(3)
2573-                                
2574-                                with col1:
2575-                                    st.metric("Mean", f"{df_clean[col].mean():.2f}")
2576-                                with col2:
--
2600-                    st.markdown(f"#### {viz['title']}")
2601-                    
2602:                    with st.expander("⚙️ Settings & Agent Reasoning"):
2603-                        st.caption(f"💡 **Agent Reasoning:** {viz['reasoning']}")
2604-                        
2605-                        override_key = f"override_toggle_{i}"
2606-                        st.checkbox("Enable manual chart override", key=override_key)
2607-                        
--
2694-            
2695-            for log in filtered_logs:
2696:                with st.container():
2697-                    col1, col2 = st.columns([1, 4])
2698-                    
2699-                    with col1:
2700-                        st.code(log['timestamp'])
2701-                        
