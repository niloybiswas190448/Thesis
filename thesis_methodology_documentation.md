# Dhaka Public Transport Fare System Optimization - Methodology Documentation

## Overview

This document provides detailed methodology for the comprehensive analysis of Dhaka's public transport fare system optimization, addressing all thesis objectives through advanced analytical techniques.

## 1. Objective 1: User Preferences and Affordability Analysis

### 1.1 Discrete Choice Modeling (DCM) Framework

#### Multinomial Logit (MNL) Model
The MNL model is used to analyze mode choice behavior across different income groups:

**Model Specification:**
```
U_ij = β₀ + β₁ × Fare_ij + β₂ × TravelTime_ij + β₃ × Comfort_ij + β₄ × WaitTime_ij + ε_ij
```

Where:
- U_ij = Utility of mode j for individual i
- β₀ = Alternative-specific constant
- β₁, β₂, β₃, β₄ = Parameter estimates for fare, travel time, comfort, and wait time
- ε_ij = Random error term

**Choice Probability:**
```
P_ij = exp(U_ij) / Σ_k exp(U_ik)
```

#### Income Group Heterogeneity Analysis
Separate MNL models are estimated for each income group (Low, Mid, High) to capture preference heterogeneity:

1. **Low Income Group:** Focus on affordability and basic accessibility
2. **Mid Income Group:** Balance between cost and service quality
3. **High Income Group:** Emphasis on comfort and time savings

#### Elasticity Analysis
Direct and cross elasticities are calculated to understand fare sensitivity:

**Direct Fare Elasticity:**
```
E_ii = (∂P_i/∂Fare_i) × (Fare_i/P_i) = β_fare × Fare_i × (1 - P_i)
```

**Cross Fare Elasticity:**
```
E_ij = (∂P_i/∂Fare_j) × (Fare_j/P_i) = -β_fare × Fare_j × P_j
```

### 1.2 Contingent Valuation Method (CVM)

#### Willingness to Pay (WTP) Estimation
WTP is estimated using the stated preference survey responses:

**WTP Calculation:**
```
WTP_i = max(Fare_i | U_i ≥ U_threshold)
```

Where U_threshold represents the minimum acceptable utility level.

#### Affordability Analysis
Affordability ratios are calculated to assess financial constraints:

**Affordability Ratio:**
```
AR_i = Fare_Paid_i / WTP_i
```

**Affordability Thresholds:**
- AR < 0.5: Highly affordable
- 0.5 ≤ AR < 1.0: Affordable
- AR ≥ 1.0: Unaffordable

## 2. Objective 2: Social Welfare Optimization

### 2.1 Welfare Optimization Models

#### Max-R (Revenue Maximization) Model
```
Maximize: R = Σ_i (P_i × Fare_i × Demand_i)
Subject to: Fare_min ≤ Fare_i ≤ Fare_max
```

#### Max-P (Profit Maximization) Model
```
Maximize: Π = Σ_i (P_i × Fare_i × Demand_i - Cost_i)
Subject to: Fare_min ≤ Fare_i ≤ Fare_max
```

#### Max-B (Benefit Maximization) Model
```
Maximize: B = Σ_i (Consumer_Surplus_i + Producer_Surplus_i)
Subject to: Fare_min ≤ Fare_i ≤ Fare_max
```

#### Max-D (Demand Maximization) Model
```
Maximize: D = Σ_i Demand_i
Subject to: Revenue_constraint
```

#### Max-S (Social Welfare Maximization) Model
```
Maximize: SW = Σ_i (Consumer_Surplus_i + Producer_Surplus_i - Environmental_Cost_i)
Subject to: Budget_constraint
```

### 2.2 Multi-Criteria Decision Analysis (MCDA)

#### Criteria and Weights
Five criteria are used for mode evaluation:

1. **Social Welfare (40%):** Primary objective
2. **Revenue (20%):** Financial sustainability
3. **Profit (20%):** Operator viability
4. **Demand (10%):** Accessibility
5. **Equity (10%):** Distributional fairness

#### Scoring Method
```
Score_i = Σ_j (w_j × s_ij)
```

Where:
- w_j = Weight of criterion j
- s_ij = Normalized score of mode i for criterion j

## 3. Objective 3: Travel Time and Key Factors Analysis

### 3.1 Generalized Cost Function

#### Cost Components
The generalized cost includes multiple components:

```
GC_ij = Fare_ij + α × TravelTime_ij + β × WaitTime_ij + γ × TransferCost_ij
```

Where:
- α = Value of Time (VOT)
- β = Waiting time penalty factor (typically 1.5×VOT)
- γ = Transfer inconvenience factor

#### Value of Time Estimation
VOT is calculated by income group:

```
VOT_i = WTP_i / TotalTime_i
```

### 3.2 Equity-Sensitive Policy Analysis

#### Policy Scenarios
Four subsidy policies are evaluated:

1. **Current Policy:** No subsidies
2. **Progressive Subsidy:** 30% (Low), 15% (Mid), 0% (High)
3. **Universal Subsidy:** 20% for all income groups
4. **Targeted Subsidy:** 40% (Low), 10% (Mid), 0% (High)

#### Policy Impact Metrics
**Cost Effectiveness:**
```
CE = Accessibility_Improvement / Total_Subsidy_Cost
```

**Accessibility Improvement:**
```
AI = Σ_i (Original_Unaffordable_i - New_Unaffordable_i)
```

## 4. Data Sources and Preprocessing

### 4.1 Primary Data (Stated Preference Survey)
- **Sample Size:** 500+ respondents
- **Variables:** Mode choice, fare, travel time, comfort, WTP, income
- **Format:** Wide format with choice scenarios

### 4.2 Secondary Data
- **Income-Fare Matrix:** Cross-tabulation by income group and mode
- **Operator Costs:** Operating, maintenance, and infrastructure costs
- **Environmental Data:** Emissions per mode and distance

### 4.3 Data Preprocessing Steps
1. **Data Cleaning:** Remove missing values and outliers
2. **Variable Creation:** Generate derived variables (total time, fare per km)
3. **Dummy Variables:** Create categorical variable indicators
4. **Normalization:** Scale variables for model estimation

## 5. Model Estimation and Validation

### 5.1 Model Estimation
- **Software:** Python with statsmodels and pylogit
- **Method:** Maximum Likelihood Estimation (MLE)
- **Convergence:** Iterative optimization with tolerance criteria

### 5.2 Model Validation
- **Goodness of Fit:** McFadden's R², AIC, BIC
- **Parameter Significance:** t-statistics and p-values
- **Model Comparison:** Likelihood ratio tests

### 5.3 Sensitivity Analysis
- **Parameter Uncertainty:** Monte Carlo simulation
- **Scenario Analysis:** Alternative parameter values
- **Robustness Checks:** Different model specifications

## 6. Policy Implications and Recommendations

### 6.1 Differentiated Pricing Strategy
Based on income group analysis, implement:
- **Low Income:** Subsidized fares with basic service
- **Mid Income:** Standard fares with improved service
- **High Income:** Premium fares with enhanced comfort

### 6.2 Service Quality Improvements
Focus on:
- **Reducing Waiting Times:** Especially for high-value modes
- **Enhancing Comfort:** Air conditioning, seating, cleanliness
- **Improving Reliability:** Punctuality and frequency

### 6.3 Equity and Accessibility
Implement:
- **Progressive Subsidy Structure:** Higher subsidies for low-income users
- **Affordability Monitoring:** Regular assessment of fare burdens
- **Accessibility Targets:** Minimum service levels for all areas

### 6.4 Environmental Considerations
Incorporate:
- **Carbon Pricing:** Environmental externalities in fare structure
- **Mode Promotion:** Incentives for sustainable transport
- **Emission Reduction:** Technology upgrades and operational efficiency

## 7. Limitations and Future Research

### 7.1 Current Limitations
- **Sample Representativeness:** Limited to surveyed areas
- **Static Analysis:** No dynamic effects considered
- **Simplified Cost Functions:** Linear approximations used
- **Environmental Externalities:** Limited quantification

### 7.2 Future Research Directions
- **Dynamic Modeling:** Time-series analysis of fare changes
- **Stakeholder Integration:** Multi-stakeholder preference modeling
- **Real-time Optimization:** Adaptive fare systems
- **Environmental Impact:** Comprehensive lifecycle analysis

## 8. Software and Tools

### 8.1 Primary Software
- **Python 3.8+:** Main programming language
- **pandas:** Data manipulation and analysis
- **numpy:** Numerical computations
- **scipy:** Optimization and statistical functions

### 8.2 Statistical Modeling
- **statsmodels:** Econometric modeling
- **pylogit:** Discrete choice modeling
- **scikit-learn:** Machine learning algorithms

### 8.3 Visualization
- **matplotlib:** Basic plotting
- **seaborn:** Statistical graphics
- **plotly:** Interactive dashboards

### 8.4 Optimization
- **cvxpy:** Convex optimization
- **scipy.optimize:** Nonlinear optimization

## 9. Output Files and Reports

### 9.1 Generated Files
1. **comprehensive_analysis_dashboard.html:** Interactive visualization dashboard
2. **comprehensive_thesis_report.md:** Detailed analysis report
3. **welfare_optimization_report.md:** Optimization results
4. **discrete_choice_analysis.md:** DCM model results

### 9.2 Report Structure
- **Executive Summary:** Key findings and recommendations
- **Methodology:** Detailed analytical approach
- **Results:** Quantitative analysis outcomes
- **Policy Implications:** Strategic recommendations
- **Technical Appendices:** Model specifications and validation

## 10. Quality Assurance

### 10.1 Data Quality
- **Validation:** Cross-checking with secondary sources
- **Consistency:** Logical consistency checks
- **Completeness:** Missing data assessment

### 10.2 Model Quality
- **Specification:** Theoretical foundation verification
- **Estimation:** Convergence and parameter validation
- **Prediction:** Out-of-sample testing

### 10.3 Results Quality
- **Sensitivity:** Parameter uncertainty analysis
- **Robustness:** Alternative model specifications
- **Interpretation:** Policy relevance assessment

This methodology provides a comprehensive framework for analyzing Dhaka's public transport fare system optimization, ensuring rigorous analysis and actionable policy recommendations.