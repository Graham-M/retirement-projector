# 💰 Retirement Portfolio Calculator

A comprehensive web application for retirement portfolio planning and withdrawal scenario analysis.

## Features

- **Three-phase interface** with organized tabs
- **Dynamic portfolio builder** with templates
- **Retirement reallocation planning** 
- **Interactive visualizations** and analysis
- **Multiple withdrawal scenarios** testing
- **Professional styling** for financial planning

## Installation

1. Create and activate virtual environment:
```bash
python -m venv ~/.venv/retirementcalc
source ~/.venv/retirementcalc/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
source ~/.venv/retirementcalc/bin/activate
streamlit run retirement-projector.py
```

Access at: `http://localhost:8501`

## Interface Overview

### 📊 Accumulation Phase
- Configure pre-retirement portfolios (401k, IRA, stocks, etc.)
- Set initial amounts, annual contributions, and growth rates
- Choose from templates: Conservative, Balanced, Aggressive
- View portfolio summary and validation

### 🏦 Retirement Phase  
- Configure retirement asset allocation
- Set percentage allocations for different asset types
- Choose from retirement templates: Conservative, Moderate, Balanced
- View blended growth rates and allocation validation

### 📈 Analysis & Results
- Portfolio growth projections over time
- Accumulation milestone summary
- Withdrawal scenario comparisons
- Retirement timeline analysis
- Sustainability indicators

## Key Concepts

**Accumulation Phase**: Your money grows at different rates based on where it's invested (stocks, bonds, etc.)

**Retirement Phase**: You reallocate to a more conservative portfolio mix, creating a blended growth rate for withdrawal calculations

**Withdrawal Scenarios**: Test different withdrawal rates (3%, 4%, 5%) to see portfolio sustainability

## Templates

### Accumulation Templates
- **Conservative**: Government bonds, corporate bonds, dividend stocks
- **Balanced**: Index funds, bonds, international stocks  
- **Aggressive**: Growth stocks, tech stocks, emerging markets

### Retirement Templates
- **Conservative**: 70% treasury bonds, 20% savings, 10% dividend stocks
- **Moderate**: 50% government bonds, 30% corporate bonds, 20% dividend stocks
- **Balanced**: 40% bonds, 40% dividend stocks, 20% growth stocks

## Currency Support

Supports GBP (£), USD ($), and EUR (€) calculations.

## Requirements

- Python 3.7+
- Streamlit 1.28+
- Pandas 1.5+
- Plotly 5.15+
- NumPy 1.21+
