import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
from typing import Dict, List, Tuple

def main():
    st.set_page_config(
        page_title="Retirement Portfolio Calculator",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .portfolio-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("💰 Retirement Portfolio Calculator")
    st.markdown("Plan your financial future with confidence using comprehensive portfolio analysis and withdrawal scenario modeling.")
    
    # Initialize session state
    if 'portfolios' not in st.session_state:
        st.session_state.portfolios = [
            {"name": "Primary Portfolio", "initial": 50000, "annual": 10000, "rate": 0.07}
        ]
    
    if 'retirement_portfolios' not in st.session_state:
        st.session_state.retirement_portfolios = [
            {"name": "Conservative Bonds", "allocation": 0.60, "rate": 0.03},
            {"name": "Dividend Stocks", "allocation": 0.40, "rate": 0.06}
        ]
    
    # Sidebar inputs
    with st.sidebar:
        st.header("📊 Analysis Parameters")
        
        # Years to retirement
        years_to_retirement = st.slider(
            "Years to Retirement",
            min_value=10,
            max_value=30,
            value=15,
            help="Number of years until you plan to retire"
        )
        
        # Retirement length
        retirement_length = st.slider(
            "Retirement Length (Years)",
            min_value=20,
            max_value=40,
            value=30,
            help="Expected length of retirement period"
        )
        
        st.markdown("---")
        st.markdown("**Retirement Portfolio Allocation**")
        st.markdown("Configure how you'll reallocate your portfolio during retirement")
        
        # Currency selection
        currency = st.selectbox(
            "Currency",
            options=["GBP", "USD", "EUR"],
            index=0,
            help="Select your preferred currency for calculations"
        )
        
        # Withdrawal rates
        withdrawal_rates = st.multiselect(
            "Withdrawal Rates to Test",
            options=["3%", "4%", "5%", "6%", "7%"],
            default=["3%", "4%", "5%"],
            help="Annual withdrawal rates as percentage of portfolio value"
        )
        
        # Convert withdrawal rates to floats
        withdrawal_rates_float = [float(rate.strip('%')) / 100 for rate in withdrawal_rates]
    
    # Currency symbols
    currency_symbols = {"GBP": "£", "USD": "$", "EUR": "€"}
    symbol = currency_symbols[currency]
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["📊 Accumulation Phase", "🏦 Retirement Phase", "📈 Analysis & Results"])
    
    # Tab 1: Accumulation Phase
    with tab1:
        st.subheader("📋 Pre-Retirement Portfolio Configuration")
        st.markdown("Configure your investment portfolios during your working years")
        
        # Portfolio template selector
        template = st.selectbox(
            "Choose a template or build custom:",
            ["Custom", "Conservative", "Balanced", "Aggressive"],
            help="Select a pre-built portfolio template or create your own custom portfolio"
        )
        
        # Apply template if selected
        if template != "Custom":
            apply_template(template)
        
        # Dynamic portfolio input
        st.markdown("### Portfolio Components")
        
        # Portfolio input form
        portfolio_container = st.container()
        with portfolio_container:
            for i, portfolio in enumerate(st.session_state.portfolios):
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                
                with col1:
                    portfolio["name"] = st.text_input(
                        f"Portfolio Name {i+1}",
                        value=portfolio["name"],
                        key=f"name_{i}",
                        placeholder="e.g., 401k, IRA, Stocks"
                    )
                
                with col2:
                    portfolio["initial"] = st.number_input(
                        f"Initial Amount ({symbol})",
                        min_value=0,
                        value=portfolio["initial"],
                        step=1000,
                        key=f"initial_{i}",
                        format="%d"
                    )
                
                with col3:
                    portfolio["annual"] = st.number_input(
                        f"Annual Contribution ({symbol})",
                        min_value=0,
                        value=portfolio["annual"],
                        step=500,
                        key=f"annual_{i}",
                        format="%d"
                    )
                
                with col4:
                    portfolio["rate"] = st.number_input(
                        f"Growth Rate (%)",
                        min_value=0.0,
                        max_value=0.20,
                        value=portfolio["rate"],
                        step=0.01,
                        key=f"rate_{i}",
                        format="%.2f"
                    )
                
                with col5:
                    if st.button("🗑️", key=f"delete_{i}", help="Remove this portfolio"):
                        if len(st.session_state.portfolios) > 1:
                            st.session_state.portfolios.pop(i)
                            st.rerun()
        
        # Add/Remove portfolio buttons
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("➕ Add Portfolio"):
                st.session_state.portfolios.append({
                    "name": f"Portfolio {len(st.session_state.portfolios) + 1}",
                    "initial": 0,
                    "annual": 0,
                    "rate": 0.07
                })
                st.rerun()
        
        with col2:
            if st.button("💾 Save Config"):
                save_portfolio_config()
        
        # Show accumulation summary
        if validate_portfolios():
            st.markdown("### Portfolio Summary")
            total_initial = sum(p["initial"] for p in st.session_state.portfolios)
            total_annual = sum(p["annual"] for p in st.session_state.portfolios)
            weighted_rate = sum(p["initial"] * p["rate"] for p in st.session_state.portfolios) / total_initial if total_initial > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Current Value", f"{symbol}{total_initial:,.0f}")
            with col2:
                st.metric("Annual Contributions", f"{symbol}{total_annual:,.0f}")
            with col3:
                st.metric("Weighted Avg Growth Rate", f"{weighted_rate:.1%}")
    
    # Tab 2: Retirement Phase
    with tab2:
        st.subheader("🏦 Retirement Portfolio Allocation")
        st.markdown("Configure how you'll reallocate your portfolio during retirement (typically more conservative)")
        
        # Retirement template selector
        retirement_template = st.selectbox(
            "Choose a retirement template:",
            ["Custom", "Conservative", "Moderate", "Balanced"],
            help="Choose a retirement portfolio template"
        )
        
        if retirement_template != "Custom":
            apply_retirement_template(retirement_template)
        
        st.markdown("### Retirement Asset Allocation")
        
        # Retirement portfolio input form
        retirement_container = st.container()
        with retirement_container:
            for i, portfolio in enumerate(st.session_state.retirement_portfolios):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    portfolio["name"] = st.text_input(
                        f"Asset Type {i+1}",
                        value=portfolio["name"],
                        key=f"ret_name_{i}",
                        placeholder="e.g., Bonds, Dividend Stocks"
                    )
                
                with col2:
                    portfolio["allocation"] = st.number_input(
                        f"Allocation (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=portfolio["allocation"] * 100,
                        step=5.0,
                        key=f"ret_allocation_{i}",
                        format="%.1f"
                    ) / 100
                
                with col3:
                    portfolio["rate"] = st.number_input(
                        f"Growth Rate (%)",
                        min_value=0.0,
                        max_value=0.15,
                        value=portfolio["rate"],
                        step=0.01,
                        key=f"ret_rate_{i}",
                        format="%.2f"
                    )
                
                with col4:
                    if st.button("🗑️", key=f"ret_delete_{i}", help="Remove this asset"):
                        if len(st.session_state.retirement_portfolios) > 1:
                            st.session_state.retirement_portfolios.pop(i)
                            st.rerun()
        
        # Add retirement portfolio buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("➕ Add Retirement Asset"):
                st.session_state.retirement_portfolios.append({
                    "name": f"Asset {len(st.session_state.retirement_portfolios) + 1}",
                    "allocation": 0.0,
                    "rate": 0.04
                })
                st.rerun()
        
        # Show retirement allocation summary
        if st.session_state.retirement_portfolios:
            st.markdown("### Retirement Allocation Summary")
            total_allocation = sum(p["allocation"] for p in st.session_state.retirement_portfolios)
            blended_rate = sum(p["allocation"] * p["rate"] for p in st.session_state.retirement_portfolios)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Allocation", f"{total_allocation:.1%}")
            with col2:
                st.metric("Blended Growth Rate", f"{blended_rate:.1%}")
            with col3:
                if abs(total_allocation - 1.0) > 0.01:
                    st.error("⚠️ Must total 100%")
                else:
                    st.success("✅ Allocation Valid")
    
    # Tab 3: Analysis & Results
    with tab3:
        # Validate portfolios
        valid_portfolios = validate_portfolios()
        valid_retirement_portfolios = validate_retirement_portfolios()
        
        if valid_portfolios and valid_retirement_portfolios:
            # Calculate and display results
            display_portfolio_analysis(
                years_to_retirement,
                retirement_length,
                withdrawal_rates_float,
                symbol
            )
        else:
            st.warning("⚠️ Please complete both accumulation and retirement portfolio configurations to see analysis.")
            
            if not valid_portfolios:
                st.error("❌ Accumulation portfolios incomplete or invalid")
            if not valid_retirement_portfolios:
                st.error("❌ Retirement allocation incomplete or doesn't total 100%")
            
            st.markdown("### Quick Tips:")
            st.markdown("""
            1. **Accumulation Phase**: Add your current investment accounts (401k, IRA, etc.)
            2. **Retirement Phase**: Plan your asset allocation during retirement (typically more conservative)
            3. **Analysis**: View comprehensive projections and withdrawal scenarios
            """)

def apply_template(template_name: str):
    """Apply a predefined portfolio template"""
    templates = {
        "Conservative": [
            {"name": "Government Bonds", "initial": 30000, "annual": 5000, "rate": 0.03},
            {"name": "Corporate Bonds", "initial": 20000, "annual": 3000, "rate": 0.04},
            {"name": "Dividend Stocks", "initial": 15000, "annual": 2000, "rate": 0.06}
        ],
        "Balanced": [
            {"name": "Index Funds", "initial": 40000, "annual": 8000, "rate": 0.07},
            {"name": "Bonds", "initial": 25000, "annual": 4000, "rate": 0.04},
            {"name": "International Stocks", "initial": 15000, "annual": 3000, "rate": 0.08}
        ],
        "Aggressive": [
            {"name": "Growth Stocks", "initial": 35000, "annual": 7000, "rate": 0.10},
            {"name": "Tech Stocks", "initial": 25000, "annual": 5000, "rate": 0.12},
            {"name": "Emerging Markets", "initial": 15000, "annual": 3000, "rate": 0.09}
        ]
    }
    
    if template_name in templates:
        st.session_state.portfolios = templates[template_name]
        st.success(f"Applied {template_name} template!")

def apply_retirement_template(template_name: str):
    """Apply a predefined retirement portfolio template"""
    retirement_templates = {
        "Conservative": [
            {"name": "Treasury Bonds", "allocation": 0.70, "rate": 0.03},
            {"name": "High-Yield Savings", "allocation": 0.20, "rate": 0.02},
            {"name": "Dividend Stocks", "allocation": 0.10, "rate": 0.05}
        ],
        "Moderate": [
            {"name": "Government Bonds", "allocation": 0.50, "rate": 0.03},
            {"name": "Corporate Bonds", "allocation": 0.30, "rate": 0.04},
            {"name": "Dividend Stocks", "allocation": 0.20, "rate": 0.06}
        ],
        "Balanced": [
            {"name": "Bonds", "allocation": 0.40, "rate": 0.035},
            {"name": "Dividend Stocks", "allocation": 0.40, "rate": 0.06},
            {"name": "Growth Stocks", "allocation": 0.20, "rate": 0.08}
        ]
    }
    
    if template_name in retirement_templates:
        st.session_state.retirement_portfolios = retirement_templates[template_name]

def validate_portfolios() -> bool:
    """Validate portfolio configurations"""
    for portfolio in st.session_state.portfolios:
        if not portfolio["name"].strip():
            return False
        if portfolio["initial"] < 0 or portfolio["annual"] < 0 or portfolio["rate"] < 0:
            return False
        if portfolio["initial"] == 0 and portfolio["annual"] == 0:
            return False
    return True

def validate_retirement_portfolios() -> bool:
    """Validate retirement portfolio configurations"""
    if not st.session_state.retirement_portfolios:
        return False
    
    total_allocation = sum(p["allocation"] for p in st.session_state.retirement_portfolios)
    if abs(total_allocation - 1.0) > 0.01:  # Allow 1% tolerance
        return False
    
    for portfolio in st.session_state.retirement_portfolios:
        if not portfolio["name"].strip():
            return False
        if portfolio["allocation"] < 0 or portfolio["rate"] < 0:
            return False
        if portfolio["allocation"] == 0:
            return False
    
    return True

def save_portfolio_config():
    """Save portfolio configuration to JSON"""
    config = {
        "portfolios": st.session_state.portfolios,
        "timestamp": pd.Timestamp.now().isoformat()
    }
    
    config_json = json.dumps(config, indent=2)
    st.download_button(
        label="💾 Download Portfolio Configuration",
        data=config_json,
        file_name="portfolio_config.json",
        mime="application/json"
    )

def calculate_portfolio_growth(portfolios: List[Dict], years: int) -> pd.DataFrame:
    """Calculate year-by-year portfolio growth"""
    results = []
    
    for year in range(years + 1):
        year_data = {"Year": year}
        total_value = 0
        
        for portfolio in portfolios:
            if year == 0:
                value = portfolio["initial"]
            else:
                # Calculate compound growth with annual contributions
                value = portfolio["initial"]
                for y in range(year):
                    value = (value + portfolio["annual"]) * (1 + portfolio["rate"])
            
            year_data[portfolio["name"]] = value
            total_value += value
        
        year_data["Total"] = total_value
        results.append(year_data)
    
    return pd.DataFrame(results)

def calculate_withdrawal_scenarios(
    final_portfolio_value: float,
    withdrawal_rates: List[float],
    retirement_years: int,
    retirement_portfolios: List[Dict]
) -> Dict:
    """Calculate withdrawal scenarios during retirement using retirement portfolio allocation"""
    scenarios = {}
    
    # Calculate blended growth rate from retirement portfolio
    blended_growth_rate = sum(p["allocation"] * p["rate"] for p in retirement_portfolios)
    
    for rate in withdrawal_rates:
        scenario_name = f"{rate:.1%}"
        annual_withdrawal = final_portfolio_value * rate
        
        # Calculate portfolio value over retirement years
        portfolio_values = []
        current_value = final_portfolio_value
        
        for year in range(retirement_years + 1):
            if year == 0:
                portfolio_values.append(current_value)
            else:
                # Withdraw at beginning of year, then grow
                current_value = (current_value - annual_withdrawal) * (1 + blended_growth_rate)
                portfolio_values.append(max(0, current_value))
        
        scenarios[scenario_name] = {
            "annual_withdrawal": annual_withdrawal,
            "monthly_withdrawal": annual_withdrawal / 12,
            "portfolio_values": portfolio_values,
            "final_value": portfolio_values[-1],
            "blended_rate": blended_growth_rate
        }
    
    return scenarios

def display_portfolio_analysis(
    years_to_retirement: int,
    retirement_length: int,
    withdrawal_rates: List[float],
    symbol: str
):
    """Display comprehensive portfolio analysis"""
    
    # Calculate portfolio growth
    growth_df = calculate_portfolio_growth(st.session_state.portfolios, years_to_retirement)
    
    # Calculate initial portfolio value for growth calculations
    total_initial = sum(p["initial"] for p in st.session_state.portfolios)
    
    # Show projected retirement value
    final_value = growth_df["Total"].iloc[-1]
    st.metric("🎯 Projected Retirement Portfolio Value", f"{symbol}{final_value:,.0f}")
    
    # Portfolio growth chart
    st.subheader("📈 Portfolio Growth Projection")
    
    fig_growth = go.Figure()
    
    # Add lines for each portfolio component
    for portfolio in st.session_state.portfolios:
        fig_growth.add_trace(go.Scatter(
            x=growth_df["Year"],
            y=growth_df[portfolio["name"]],
            mode='lines',
            name=portfolio["name"],
            line=dict(width=2)
        ))
    
    # Add total portfolio line (highlighted)
    fig_growth.add_trace(go.Scatter(
        x=growth_df["Year"],
        y=growth_df["Total"],
        mode='lines',
        name="Total Portfolio",
        line=dict(width=4, color='#1f77b4')
    ))
    
    fig_growth.update_layout(
        title="Portfolio Growth Over Time",
        xaxis_title="Years",
        yaxis_title=f"Portfolio Value ({symbol})",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Accumulation summary table
    st.subheader("📋 Accumulation Summary")
    
    milestone_years = [5, 10, years_to_retirement]
    milestone_data = []
    
    for year in milestone_years:
        if year <= years_to_retirement:
            row_data = growth_df[growth_df["Year"] == year].iloc[0]
            milestone_data.append({
                "Milestone": f"Year {year}",
                "Total Value": f"{symbol}{row_data['Total']:,.0f}",
                "Growth": f"{symbol}{row_data['Total'] - total_initial:,.0f}"
            })
    
    milestone_df = pd.DataFrame(milestone_data)
    st.dataframe(milestone_df, use_container_width=True, hide_index=True)
    
    # Withdrawal scenarios
    if withdrawal_rates:
        st.subheader("🏦 Retirement Withdrawal Analysis")
        
        final_value = growth_df["Total"].iloc[-1]
        scenarios = calculate_withdrawal_scenarios(
            final_value, withdrawal_rates, retirement_length, st.session_state.retirement_portfolios
        )
        
        # Withdrawal scenarios comparison
        scenario_data = []
        for rate_name, scenario in scenarios.items():
            scenario_data.append({
                "Withdrawal Rate": rate_name,
                "Annual Income": f"{symbol}{scenario['annual_withdrawal']:,.0f}",
                "Monthly Income": f"{symbol}{scenario['monthly_withdrawal']:,.0f}",
                "Final Portfolio Value": f"{symbol}{scenario['final_value']:,.0f}",
                "Sustainable": "✅" if scenario['final_value'] > 0 else "❌",
                "Blended Rate": f"{scenario['blended_rate']:.1%}"
            })
        
        scenario_df = pd.DataFrame(scenario_data)
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)
        
        # Retirement timeline chart
        st.subheader("📊 Retirement Portfolio Timeline")
        
        fig_retirement = go.Figure()
        
        years_retirement = list(range(retirement_length + 1))
        
        for rate_name, scenario in scenarios.items():
            fig_retirement.add_trace(go.Scatter(
                x=years_retirement,
                y=scenario['portfolio_values'],
                mode='lines+markers',
                name=f"{rate_name} Withdrawal",
                line=dict(width=3)
            ))
        
        fig_retirement.update_layout(
            title="Portfolio Value During Retirement",
            xaxis_title="Years into Retirement",
            yaxis_title=f"Portfolio Value ({symbol})",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_retirement, use_container_width=True)

if __name__ == "__main__":
    main()