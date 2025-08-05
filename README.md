# Dhaka Public Transport Fare System Optimization Analysis

## Overview

This comprehensive analysis framework addresses the optimization of Dhaka's public transport fare system, focusing on social welfare maximization while considering user preferences, affordability constraints, and equity concerns.

## Objectives

### 1. Assessing User Preferences and Affordability Constraints
- **1.1** Assess how fare, travel time, and service quality affect mode choice among different income brackets
- **1.2** Analyze affordability thresholds and willingness to pay for improved services

### 2. Modeling and Comparing Social Welfare Outcomes
- **2.1** Quantify welfare outcomes under different mode-specific scenarios
- **2.2** Compare cumulative social welfare impacts across modes

### 3. Examining Travel Time and Key Factors
- **3.1** Identify the role of travel time, waiting time, and transfer inconvenience in mode selection
- **3.2** Evaluate equity-sensitive fare/subsidy policies and their distributional impact

## Methodology

### Data Sources
- **Primary Data**: Stated Preference (SP) survey data
- **Secondary Data**: Income-Fare matrix, DTCA data, operator costs, emissions data

### Analytical Techniques
- **Discrete Choice Modeling**: Multinomial Logit, Mixed Logit, Nested Logit
- **Contingent Valuation Method (CVM)**: Willingness to pay estimation
- **Welfare Optimization**: Max-R, Max-P, Max-B, Max-D, Max-S models
- **Multi-criteria Decision Analysis (MCDA)**: Comparative policy evaluation
- **Generalized Cost Function**: Accessibility and utility modeling

## Files Structure

```
├── transport_fare_analysis.py      # Main analysis framework
├── discrete_choice_models.py       # Advanced DCM techniques
├── welfare_optimization.py         # Welfare optimization models
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── transport_analysis_dashboard.html  # Interactive dashboard (generated)
├── transport_analysis_report.md    # Analysis report (generated)
└── welfare_optimization_report.md  # Optimization report (generated)
```

## Installation and Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Analysis
```python
# Import the main analyzer
from transport_fare_analysis import TransportFareAnalyzer

# Initialize and run complete analysis
analyzer = TransportFareAnalyzer()
analyzer.load_data()  # Uses sample data by default
analyzer.run_complete_analysis()
```

### 3. Use with Real Data
```python
# Load your actual data files
analyzer.load_data(
    sp_file='your_sp_survey_data.xlsx',
    income_fare_file='your_income_fare_matrix.xlsx',
    secondary_file='your_secondary_data.xlsx'
)
```

## Key Features

### 1. TransportFareAnalyzer Class
- **Mode Choice Analysis**: Multinomial Logit modeling with income group heterogeneity
- **Affordability Analysis**: Fare elasticity and willingness to pay estimation
- **Welfare Optimization**: Five different objective functions (Max-R, Max-P, Max-B, Max-D, Max-S)
- **Equity Analysis**: Generalized cost functions and distributional impact assessment
- **Policy Evaluation**: Scenario simulation for different subsidy policies

### 2. DiscreteChoiceAnalyzer Class
- **Advanced DCM**: Mixed Logit and Nested Logit models
- **Income Heterogeneity**: Separate models for different income groups
- **Elasticity Analysis**: Direct and cross elasticities calculation
- **Scenario Analysis**: Mode share prediction under different conditions

### 3. WelfareOptimizer Class
- **Multi-objective Optimization**: Combined optimization with weighted objectives
- **Sensitivity Analysis**: Parameter uncertainty assessment
- **Income Group Optimization**: Separate optimization for different income levels
- **Constraint Handling**: Budget and policy constraint implementation

## Output Files

### 1. Interactive Dashboard (`transport_analysis_dashboard.html`)
- Mode choice by income group
- Fare elasticity analysis
- Welfare optimization results
- MCDA scores visualization
- Generalized cost analysis
- Policy impact comparison

### 2. Analysis Report (`transport_analysis_report.md`)
- Executive summary
- Detailed methodology
- Key findings
- Policy recommendations
- Technical appendices

### 3. Optimization Report (`welfare_optimization_report.md`)
- Optimization results by mode
- Income group-specific analysis
- Sensitivity analysis results
- Policy implications

## Example Usage

### Basic Analysis
```python
from transport_fare_analysis import TransportFareAnalyzer

# Initialize analyzer
analyzer = TransportFareAnalyzer()

# Load data
analyzer.load_data()

# Run specific analyses
mnl_model, income_analysis = analyzer.analyze_mode_choice_preferences()
elasticity_results, wtp_analysis = analyzer.analyze_affordability_and_wtp()
welfare_results = analyzer.model_social_welfare_outcomes()
mcda_results = analyzer.compare_cumulative_welfare()
equity_analysis, vot_analysis = analyzer.analyze_travel_time_factors()
policy_results = analyzer.evaluate_equity_policies()

# Generate outputs
analyzer.generate_visualizations()
analyzer.generate_report()
```

### Advanced DCM Analysis
```python
from discrete_choice_models import DiscreteChoiceAnalyzer

# Initialize DCM analyzer
dcm_analyzer = DiscreteChoiceAnalyzer()

# Run complete DCM analysis
dcm_results = dcm_analyzer.run_complete_dcm_analysis(sp_data)
```

### Welfare Optimization
```python
from welfare_optimization import WelfareOptimizer

# Initialize optimizer
optimizer = WelfareOptimizer()

# Run complete optimization
optimization_results = optimizer.run_complete_optimization(sp_data, secondary_data)
```

## Key Findings

### 1. Mode Choice Preferences
- **Fare Sensitivity**: Different income groups show varying sensitivity to fare changes
- **Time Valuation**: Value of time varies significantly across income groups
- **Comfort Preferences**: Higher income groups place more value on comfort

### 2. Affordability Analysis
- **Elasticity Patterns**: Low-income groups show higher fare elasticity
- **WTP Thresholds**: Willingness to pay varies by income level and service quality
- **Affordability Gaps**: Significant affordability constraints for low-income users

### 3. Welfare Optimization
- **Optimal Fares**: Different objectives yield different optimal fare levels
- **Social Welfare**: Max-S model provides balanced approach considering equity
- **Mode Performance**: MRT shows highest overall welfare score in MCDA

### 4. Policy Implications
- **Differentiated Pricing**: Recommended based on income group analysis
- **Subsidy Policies**: Equity-sensitive subsidies improve accessibility
- **Service Quality**: Improvements in comfort and reliability increase welfare

## Policy Recommendations

### 1. Fare Structure
- Implement income-based differentiated pricing
- Consider social welfare maximization as primary objective
- Balance revenue requirements with accessibility goals

### 2. Subsidy Policies
- Target subsidies to low-income users
- Implement progressive subsidy structure
- Monitor and evaluate subsidy effectiveness

### 3. Service Improvements
- Focus on reducing travel time and waiting time
- Improve comfort and reliability
- Consider environmental externalities in pricing

### 4. Monitoring and Evaluation
- Regular assessment of fare elasticity
- Monitor mode share changes
- Evaluate equity impacts of policy changes

## Technical Notes

### Model Assumptions
- Linear utility functions in discrete choice models
- Simplified demand functions for optimization
- Homogeneous preferences within income groups
- Constant elasticity of substitution

### Limitations
- Sample data used for demonstration
- Simplified cost functions
- Limited environmental externalities consideration
- Static analysis (no dynamic effects)

### Future Enhancements
- Integration with real-time data
- Dynamic optimization models
- Environmental impact assessment
- Stakeholder preference incorporation

## Contact and Support

For questions or support regarding this analysis framework, please refer to the technical documentation or contact the development team.

## License

This analysis framework is provided for academic and research purposes. Please ensure proper attribution when using or modifying the code.