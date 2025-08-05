"""
Dhaka Public Transport Fare System Optimization Analysis
=======================================================

This script implements comprehensive analysis for optimizing Dhaka's public transport
fare system considering user preferences, affordability constraints, and social welfare outcomes.

Author: [Your Name]
Date: [Current Date]
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import Logit
import pylogit as pl
from scipy import stats
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TransportFareAnalyzer:
    """
    Main class for analyzing transport fare systems and optimizing social welfare
    """
    
    def __init__(self):
        self.sp_data = None
        self.income_fare_matrix = None
        self.secondary_data = None
        self.models = {}
        self.results = {}
        
    def load_data(self, sp_file=None, income_fare_file=None, secondary_file=None):
        """
        Load and prepare data for analysis
        
        Parameters:
        -----------
        sp_file : str
            Path to Stated Preference survey data
        income_fare_file : str
            Path to Income-Fare matrix data
        secondary_file : str
            Path to secondary data (DTCA, operator costs, emissions)
        """
        print("Loading data...")
        
        # Load SP data (simulated for demonstration)
        if sp_file:
            self.sp_data = pd.read_excel(sp_file)
        else:
            self.sp_data = self._generate_sample_sp_data()
            
        # Load income-fare matrix
        if income_fare_file:
            self.income_fare_matrix = pd.read_excel(income_fare_file)
        else:
            self.income_fare_matrix = self._generate_sample_income_fare_data()
            
        # Load secondary data
        if secondary_file:
            self.secondary_data = pd.read_excel(secondary_file)
        else:
            self.secondary_data = self._generate_sample_secondary_data()
            
        print("Data loaded successfully!")
        
    def _generate_sample_sp_data(self):
        """Generate sample Stated Preference data for demonstration"""
        np.random.seed(42)
        n_respondents = 1000
        
        data = []
        modes = ['Bus', 'Rickshaw', 'MRT', 'Private Car']
        income_groups = ['Low', 'Medium', 'High']
        
        for i in range(n_respondents):
            income_group = np.random.choice(income_groups, p=[0.4, 0.4, 0.2])
            income = np.random.normal(
                {'Low': 15000, 'Medium': 35000, 'High': 75000}[income_group],
                {'Low': 5000, 'Medium': 10000, 'High': 20000}[income_group]
            )
            
            for mode in modes:
                # Generate choice scenarios
                for scenario in range(3):
                    fare = np.random.uniform(10, 100)
                    travel_time = np.random.uniform(15, 90)
                    waiting_time = np.random.uniform(2, 20)
                    comfort_score = np.random.uniform(1, 5)
                    
                    # Calculate utility (simplified)
                    utility = (
                        -0.1 * fare + 
                        -0.05 * travel_time + 
                        -0.02 * waiting_time + 
                        0.3 * comfort_score +
                        np.random.normal(0, 1)
                    )
                    
                    data.append({
                        'respondent_id': i,
                        'income_group': income_group,
                        'income': income,
                        'mode': mode,
                        'scenario': scenario,
                        'fare': fare,
                        'travel_time': travel_time,
                        'waiting_time': waiting_time,
                        'comfort_score': comfort_score,
                        'utility': utility,
                        'chosen': 0  # Will be updated based on utility
                    })
        
        df = pd.DataFrame(data)
        
        # Determine chosen mode for each respondent in each scenario
        for scenario in range(3):
            for respondent in range(n_respondents):
                mask = (df['respondent_id'] == respondent) & (df['scenario'] == scenario)
                max_utility_idx = df[mask]['utility'].idxmax()
                df.loc[max_utility_idx, 'chosen'] = 1
                
        return df
    
    def _generate_sample_income_fare_data(self):
        """Generate sample income-fare matrix data"""
        income_levels = np.arange(10000, 100001, 5000)
        fare_levels = np.arange(10, 101, 5)
        
        data = []
        for income in income_levels:
            for fare in fare_levels:
                # Willingness to pay decreases with fare and increases with income
                wtp = max(0, 0.3 * income - 2 * fare + np.random.normal(0, 1000))
                affordability = max(0, 1 - (fare / (income * 0.1)))
                
                data.append({
                    'income': income,
                    'fare': fare,
                    'willingness_to_pay': wtp,
                    'affordability_score': affordability
                })
                
        return pd.DataFrame(data)
    
    def _generate_sample_secondary_data(self):
        """Generate sample secondary data"""
        modes = ['Bus', 'Rickshaw', 'MRT', 'Private Car']
        
        data = []
        for mode in modes:
            data.append({
                'mode': mode,
                'operator_cost_per_km': np.random.uniform(5, 25),
                'emissions_per_km': np.random.uniform(50, 200),
                'capacity': np.random.uniform(20, 200),
                'infrastructure_cost': np.random.uniform(1000000, 10000000),
                'maintenance_cost': np.random.uniform(1000, 10000)
            })
            
        return pd.DataFrame(data)
    
    def analyze_mode_choice_preferences(self):
        """
        Objective 1.1: Assess how fare, travel time, and service quality affect mode choice
        among different income brackets using Multinomial Logit Model
        """
        print("\n=== Analyzing Mode Choice Preferences ===")
        
        # Prepare data for MNL model
        choice_data = self.sp_data[self.sp_data['chosen'] == 1].copy()
        
        # Create dummy variables for modes
        mode_dummies = pd.get_dummies(choice_data['mode'], prefix='mode')
        choice_data = pd.concat([choice_data, mode_dummies], axis=1)
        
        # Create interaction terms with income
        choice_data['fare_income'] = choice_data['fare'] * choice_data['income']
        choice_data['time_income'] = choice_data['travel_time'] * choice_data['income']
        
        # Fit MNL model
        X = choice_data[['fare', 'travel_time', 'waiting_time', 'comfort_score', 
                        'income', 'fare_income', 'time_income']]
        X = sm.add_constant(X)
        y = choice_data['chosen']
        
        mnl_model = sm.Logit(y, X).fit()
        self.models['mnl_mode_choice'] = mnl_model
        
        print("Multinomial Logit Model Results:")
        print(mnl_model.summary())
        
        # Analyze by income group
        income_group_analysis = {}
        for income_group in choice_data['income_group'].unique():
            group_data = choice_data[choice_data['income_group'] == income_group]
            
            X_group = group_data[['fare', 'travel_time', 'waiting_time', 'comfort_score']]
            X_group = sm.add_constant(X_group)
            y_group = group_data['chosen']
            
            try:
                group_model = sm.Logit(y_group, X_group).fit()
                income_group_analysis[income_group] = group_model
            except:
                print(f"Could not fit model for {income_group} income group")
                
        self.results['income_group_analysis'] = income_group_analysis
        
        return mnl_model, income_group_analysis
    
    def analyze_affordability_and_wtp(self):
        """
        Objective 1.2: Analyze affordability thresholds and willingness to pay
        using Contingent Valuation Method and Fare Elasticity Estimation
        """
        print("\n=== Analyzing Affordability and Willingness to Pay ===")
        
        # Calculate fare elasticity by income group
        elasticity_results = {}
        
        for income_group in self.sp_data['income_group'].unique():
            group_data = self.sp_data[self.sp_data['income_group'] == income_group]
            
            # Calculate fare elasticity
            fare_changes = group_data['fare'].pct_change()
            demand_changes = group_data['chosen'].pct_change()
            
            # Remove infinite values
            valid_mask = (fare_changes != np.inf) & (fare_changes != -np.inf) & \
                        (demand_changes != np.inf) & (demand_changes != -np.inf) & \
                        (fare_changes != 0)
            
            if valid_mask.sum() > 10:
                elasticity = np.corrcoef(fare_changes[valid_mask], demand_changes[valid_mask])[0, 1]
                elasticity_results[income_group] = elasticity
        
        # CVM Analysis - Estimate willingness to pay
        wtp_analysis = {}
        for income_group in self.sp_data['income_group'].unique():
            group_data = self.sp_data[self.sp_data['income_group'] == income_group]
            
            # Calculate average WTP based on utility function
            avg_income = group_data['income'].mean()
            avg_fare = group_data['fare'].mean()
            
            # Simplified WTP calculation (in practice, use proper CVM survey responses)
            wtp = avg_income * 0.15  # Assume 15% of income as WTP threshold
            wtp_analysis[income_group] = {
                'avg_income': avg_income,
                'avg_fare': avg_fare,
                'wtp_threshold': wtp,
                'affordability_ratio': avg_fare / wtp
            }
        
        self.results['fare_elasticity'] = elasticity_results
        self.results['wtp_analysis'] = wtp_analysis
        
        print("Fare Elasticity by Income Group:")
        for group, elasticity in elasticity_results.items():
            print(f"{group}: {elasticity:.3f}")
            
        print("\nWillingness to Pay Analysis:")
        for group, analysis in wtp_analysis.items():
            print(f"{group}: WTP = {analysis['wtp_threshold']:.0f} BDT, "
                  f"Affordability Ratio = {analysis['affordability_ratio']:.2f}")
        
        return elasticity_results, wtp_analysis
    
    def model_social_welfare_outcomes(self):
        """
        Objective 2.1: Quantify welfare outcomes under different mode-specific scenarios
        using Max-R, Max-P, Max-B, Max-D, and Max-S models
        """
        print("\n=== Modeling Social Welfare Outcomes ===")
        
        # Define optimization models
        optimization_results = {}
        modes = self.sp_data['mode'].unique()
        
        for mode in modes:
            mode_data = self.sp_data[self.sp_data['mode'] == mode]
            
            # Get mode-specific parameters
            avg_fare = mode_data['fare'].mean()
            avg_demand = mode_data['chosen'].mean()
            operator_cost = self.secondary_data[
                self.secondary_data['mode'] == mode
            ]['operator_cost_per_km'].iloc[0]
            
            # Define optimization functions
            def max_revenue(fare):
                demand = max(0, avg_demand * (1 - 0.5 * (fare - avg_fare) / avg_fare))
                return -fare * demand  # Negative for minimization
            
            def max_profit(fare):
                demand = max(0, avg_demand * (1 - 0.5 * (fare - avg_fare) / avg_fare))
                revenue = fare * demand
                cost = operator_cost * demand
                return -(revenue - cost)
            
            def max_benefit(fare):
                demand = max(0, avg_demand * (1 - 0.5 * (fare - avg_fare) / avg_fare))
                consumer_surplus = 0.5 * (avg_fare - fare) * demand
                return -consumer_surplus
            
            def max_demand(fare):
                demand = max(0, avg_demand * (1 - 0.5 * (fare - avg_fare) / avg_fare))
                return -demand
            
            def max_social_welfare(fare):
                demand = max(0, avg_demand * (1 - 0.5 * (fare - avg_fare) / avg_fare))
                revenue = fare * demand
                cost = operator_cost * demand
                consumer_surplus = 0.5 * (avg_fare - fare) * demand
                return -(revenue - cost + consumer_surplus)
            
            # Optimize each objective
            objectives = {
                'Max-R': max_revenue,
                'Max-P': max_profit,
                'Max-B': max_benefit,
                'Max-D': max_demand,
                'Max-S': max_social_welfare
            }
            
            mode_results = {}
            for obj_name, obj_func in objectives.items():
                result = minimize(obj_func, x0=avg_fare, bounds=[(0, 200)])
                mode_results[obj_name] = {
                    'optimal_fare': result.x[0],
                    'objective_value': -result.fun,
                    'success': result.success
                }
            
            optimization_results[mode] = mode_results
        
        self.results['welfare_optimization'] = optimization_results
        
        print("Welfare Optimization Results:")
        for mode, results in optimization_results.items():
            print(f"\n{mode}:")
            for obj, result in results.items():
                print(f"  {obj}: Optimal Fare = {result['optimal_fare']:.1f} BDT, "
                      f"Value = {result['objective_value']:.1f}")
        
        return optimization_results
    
    def compare_cumulative_welfare(self):
        """
        Objective 2.2: Compare cumulative social welfare impacts across modes
        using Multi-criteria Decision Matrix (MCDA) approach
        """
        print("\n=== Comparing Cumulative Social Welfare ===")
        
        # Define criteria weights for MCDA
        criteria_weights = {
            'economic_efficiency': 0.3,
            'social_equity': 0.25,
            'environmental_impact': 0.2,
            'accessibility': 0.15,
            'sustainability': 0.1
        }
        
        # Calculate scores for each mode
        mcda_results = {}
        modes = self.sp_data['mode'].unique()
        
        for mode in modes:
            mode_data = self.sp_data[self.sp_data['mode'] == mode]
            secondary_mode_data = self.secondary_data[
                self.secondary_data['mode'] == mode
            ].iloc[0]
            
            # Economic efficiency (revenue - cost)
            avg_fare = mode_data['fare'].mean()
            avg_demand = mode_data['chosen'].mean()
            revenue = avg_fare * avg_demand
            cost = secondary_mode_data['operator_cost_per_km'] * avg_demand
            economic_score = (revenue - cost) / 1000  # Normalize
            
            # Social equity (accessibility across income groups)
            equity_scores = []
            for income_group in mode_data['income_group'].unique():
                group_data = mode_data[mode_data['income_group'] == income_group]
                group_usage = group_data['chosen'].mean()
                equity_scores.append(group_usage)
            social_equity_score = np.mean(equity_scores)
            
            # Environmental impact (inverse of emissions)
            environmental_score = 1 / (secondary_mode_data['emissions_per_km'] / 100)
            
            # Accessibility (inverse of travel time)
            accessibility_score = 1 / (mode_data['travel_time'].mean() / 60)
            
            # Sustainability (capacity utilization)
            sustainability_score = avg_demand / secondary_mode_data['capacity']
            
            # Calculate weighted score
            weighted_score = (
                criteria_weights['economic_efficiency'] * economic_score +
                criteria_weights['social_equity'] * social_equity_score +
                criteria_weights['environmental_impact'] * environmental_score +
                criteria_weights['accessibility'] * accessibility_score +
                criteria_weights['sustainability'] * sustainability_score
            )
            
            mcda_results[mode] = {
                'economic_efficiency': economic_score,
                'social_equity': social_equity_score,
                'environmental_impact': environmental_score,
                'accessibility': accessibility_score,
                'sustainability': sustainability_score,
                'weighted_score': weighted_score
            }
        
        self.results['mcda_analysis'] = mcda_results
        
        print("Multi-Criteria Decision Analysis Results:")
        for mode, scores in mcda_results.items():
            print(f"\n{mode}:")
            for criterion, score in scores.items():
                print(f"  {criterion}: {score:.3f}")
        
        return mcda_results
    
    def analyze_travel_time_factors(self):
        """
        Objective 3.1: Identify the role of travel time, waiting time, and transfer
        inconvenience in mode selection using Generalized Cost Function
        """
        print("\n=== Analyzing Travel Time Factors ===")
        
        # Generalized Cost Function analysis
        choice_data = self.sp_data[self.sp_data['chosen'] == 1].copy()
        
        # Calculate generalized cost for each mode
        choice_data['generalized_cost'] = (
            choice_data['fare'] + 
            0.5 * choice_data['travel_time'] +  # Value of time = 0.5 BDT/minute
            0.3 * choice_data['waiting_time'] +  # Value of waiting time = 0.3 BDT/minute
            (5 - choice_data['comfort_score']) * 10  # Discomfort cost
        )
        
        # Analyze by income group
        equity_analysis = {}
        for income_group in choice_data['income_group'].unique():
            group_data = choice_data[choice_data['income_group'] == income_group]
            
            # Calculate average generalized cost by mode
            mode_costs = group_data.groupby('mode')['generalized_cost'].mean()
            equity_analysis[income_group] = mode_costs.to_dict()
        
        # Value of Time (VOT) analysis
        vot_analysis = {}
        for income_group in choice_data['income_group'].unique():
            group_data = choice_data[choice_data['income_group'] == income_group]
            
            # Estimate VOT using regression
            X = group_data[['travel_time', 'waiting_time', 'comfort_score']]
            X = sm.add_constant(X)
            y = group_data['fare']
            
            try:
                vot_model = sm.OLS(y, X).fit()
                vot_analysis[income_group] = {
                    'travel_time_coef': vot_model.params['travel_time'],
                    'waiting_time_coef': vot_model.params['waiting_time'],
                    'comfort_coef': vot_model.params['comfort_score'],
                    'r_squared': vot_model.rsquared
                }
            except:
                print(f"Could not estimate VOT for {income_group} income group")
        
        self.results['equity_analysis'] = equity_analysis
        self.results['vot_analysis'] = vot_analysis
        
        print("Generalized Cost by Income Group and Mode:")
        for income_group, mode_costs in equity_analysis.items():
            print(f"\n{income_group}:")
            for mode, cost in mode_costs.items():
                print(f"  {mode}: {cost:.1f} BDT")
        
        print("\nValue of Time Analysis:")
        for income_group, vot in vot_analysis.items():
            print(f"{income_group}: VOT = {vot['travel_time_coef']:.2f} BDT/minute")
        
        return equity_analysis, vot_analysis
    
    def evaluate_equity_policies(self):
        """
        Objective 3.2: Evaluate equity-sensitive fare/subsidy policies and their
        distributional impact using Policy Optimization under Constraints
        """
        print("\n=== Evaluating Equity Policies ===")
        
        # Define policy scenarios
        policy_scenarios = {
            'baseline': {'subsidy_rate': 0.0, 'subsidy_cap': 0.0},
            'low_income_subsidy': {'subsidy_rate': 0.3, 'subsidy_cap': 0.1},
            'universal_subsidy': {'subsidy_rate': 0.2, 'subsidy_cap': 0.15},
            'progressive_subsidy': {'subsidy_rate': 0.4, 'subsidy_cap': 0.12}
        }
        
        policy_results = {}
        
        for scenario_name, policy_params in policy_scenarios.items():
            scenario_results = {}
            
            for mode in self.sp_data['mode'].unique():
                mode_data = self.sp_data[self.sp_data['mode'] == mode].copy()
                
                # Apply subsidy policy
                if policy_params['subsidy_rate'] > 0:
                    # Calculate subsidy based on income
                    for income_group in mode_data['income_group'].unique():
                        group_mask = mode_data['income_group'] == income_group
                        
                        if income_group == 'Low':
                            subsidy_multiplier = policy_params['subsidy_rate']
                        elif income_group == 'Medium':
                            subsidy_multiplier = policy_params['subsidy_rate'] * 0.5
                        else:  # High income
                            subsidy_multiplier = 0
                        
                        # Apply subsidy with cap
                        original_fare = mode_data.loc[group_mask, 'fare']
                        subsidy = original_fare * subsidy_multiplier
                        max_subsidy = original_fare * policy_params['subsidy_cap']
                        actual_subsidy = np.minimum(subsidy, max_subsidy)
                        
                        mode_data.loc[group_mask, 'fare'] = original_fare - actual_subsidy
                        mode_data.loc[group_mask, 'subsidy_received'] = actual_subsidy
                
                # Calculate welfare impacts
                total_subsidy = mode_data.get('subsidy_received', 0).sum()
                demand_change = mode_data['chosen'].sum() - self.sp_data[
                    self.sp_data['mode'] == mode
                ]['chosen'].sum()
                
                # Calculate distributional impact
                income_impacts = {}
                for income_group in mode_data['income_group'].unique():
                    group_data = mode_data[mode_data['income_group'] == income_group]
                    group_subsidy = group_data.get('subsidy_received', 0).sum()
                    group_benefit = group_subsidy + (group_data['chosen'].sum() * 5)  # Assume 5 BDT benefit per trip
                    income_impacts[income_group] = {
                        'subsidy_received': group_subsidy,
                        'total_benefit': group_benefit,
                        'benefit_per_capita': group_benefit / len(group_data)
                    }
                
                scenario_results[mode] = {
                    'total_subsidy': total_subsidy,
                    'demand_change': demand_change,
                    'income_impacts': income_impacts
                }
            
            policy_results[scenario_name] = scenario_results
        
        self.results['policy_evaluation'] = policy_results
        
        print("Policy Evaluation Results:")
        for scenario, results in policy_results.items():
            print(f"\n{scenario.upper()}:")
            total_subsidy = sum(r['total_subsidy'] for r in results.values())
            print(f"Total Subsidy: {total_subsidy:.0f} BDT")
            
            for mode, mode_results in results.items():
                print(f"  {mode}:")
                print(f"    Demand Change: {mode_results['demand_change']:+.0f}")
                print(f"    Subsidy: {mode_results['total_subsidy']:.0f} BDT")
                
                for income_group, impacts in mode_results['income_impacts'].items():
                    print(f"    {income_group}: {impacts['benefit_per_capita']:.1f} BDT/capita")
        
        return policy_results
    
    def generate_visualizations(self):
        """Generate comprehensive visualizations for the analysis"""
        print("\n=== Generating Visualizations ===")
        
        # Create subplots for different analyses
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Mode Choice by Income Group',
                'Fare Elasticity Analysis',
                'Welfare Optimization Results',
                'MCDA Scores by Mode',
                'Generalized Cost Analysis',
                'Policy Impact Comparison'
            ),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "radar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # 1. Mode Choice by Income Group
        mode_choice_data = self.sp_data[self.sp_data['chosen'] == 1].groupby(
            ['income_group', 'mode']
        ).size().reset_index(name='count')
        
        for income_group in mode_choice_data['income_group'].unique():
            group_data = mode_choice_data[mode_choice_data['income_group'] == income_group]
            fig.add_trace(
                go.Bar(
                    x=group_data['mode'],
                    y=group_data['count'],
                    name=income_group,
                    showlegend=True
                ),
                row=1, col=1
            )
        
        # 2. Fare Elasticity
        if 'fare_elasticity' in self.results:
            income_groups = list(self.results['fare_elasticity'].keys())
            elasticities = list(self.results['fare_elasticity'].values())
            
            fig.add_trace(
                go.Scatter(
                    x=income_groups,
                    y=elasticities,
                    mode='markers+lines',
                    name='Fare Elasticity',
                    marker=dict(size=10)
                ),
                row=1, col=2
            )
        
        # 3. Welfare Optimization
        if 'welfare_optimization' in self.results:
            modes = list(self.results['welfare_optimization'].keys())
            objectives = ['Max-R', 'Max-P', 'Max-B', 'Max-D', 'Max-S']
            
            for i, obj in enumerate(objectives):
                fares = [self.results['welfare_optimization'][mode][obj]['optimal_fare'] 
                        for mode in modes]
                fig.add_trace(
                    go.Bar(
                        x=modes,
                        y=fares,
                        name=obj,
                        showlegend=True
                    ),
                    row=2, col=1
                )
        
        # 4. MCDA Radar Chart
        if 'mcda_analysis' in self.results:
            modes = list(self.results['mcda_analysis'].keys())
            criteria = ['economic_efficiency', 'social_equity', 'environmental_impact', 
                       'accessibility', 'sustainability']
            
            for mode in modes:
                values = [self.results['mcda_analysis'][mode][criterion] for criterion in criteria]
                fig.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=criteria,
                        fill='toself',
                        name=mode
                    ),
                    row=2, col=2
                )
        
        # 5. Generalized Cost Analysis
        if 'equity_analysis' in self.results:
            income_groups = list(self.results['equity_analysis'].keys())
            modes = list(self.results['equity_analysis'][income_groups[0]].keys())
            
            for mode in modes:
                costs = [self.results['equity_analysis'][group][mode] for group in income_groups]
                fig.add_trace(
                    go.Bar(
                        x=income_groups,
                        y=costs,
                        name=mode,
                        showlegend=True
                    ),
                    row=3, col=1
                )
        
        # 6. Policy Impact
        if 'policy_evaluation' in self.results:
            scenarios = list(self.results['policy_evaluation'].keys())
            total_subsidies = []
            
            for scenario in scenarios:
                total_subsidy = sum(
                    self.results['policy_evaluation'][scenario][mode]['total_subsidy']
                    for mode in self.results['policy_evaluation'][scenario].keys()
                )
                total_subsidies.append(total_subsidy)
            
            fig.add_trace(
                go.Bar(
                    x=scenarios,
                    y=total_subsidies,
                    name='Total Subsidy',
                    showlegend=False
                ),
                row=3, col=2
            )
        
        fig.update_layout(
            height=1200,
            title_text="Dhaka Transport Fare System Analysis Dashboard",
            showlegend=True
        )
        
        # Save the plot
        fig.write_html("transport_analysis_dashboard.html")
        print("Dashboard saved as 'transport_analysis_dashboard.html'")
        
        return fig
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        print("\n=== Generating Analysis Report ===")
        
        report = []
        report.append("# Dhaka Public Transport Fare System Optimization Analysis Report\n")
        
        # Executive Summary
        report.append("## Executive Summary\n")
        report.append("This report presents a comprehensive analysis of Dhaka's public transport ")
        report.append("fare system optimization, focusing on social welfare maximization while ")
        report.append("addressing equity concerns and environmental externalities.\n")
        
        # Key Findings
        report.append("### Key Findings\n")
        
        if 'mcda_analysis' in self.results:
            best_mode = max(self.results['mcda_analysis'].items(), 
                          key=lambda x: x[1]['weighted_score'])[0]
            report.append(f"- **Optimal Mode**: {best_mode} shows the highest overall welfare score\n")
        
        if 'fare_elasticity' in self.results:
            most_elastic = min(self.results['fare_elasticity'].items(), 
                             key=lambda x: x[1])[0]
            report.append(f"- **Most Price Sensitive**: {most_elastic} income group\n")
        
        if 'policy_evaluation' in self.results:
            best_policy = max(self.results['policy_evaluation'].items(),
                            key=lambda x: sum(r['total_subsidy'] for r in x[1].values()))[0]
            report.append(f"- **Recommended Policy**: {best_policy.replace('_', ' ').title()}\n")
        
        # Detailed Analysis
        report.append("## Detailed Analysis\n")
        
        # Mode Choice Analysis
        report.append("### 1. Mode Choice Preferences\n")
        if 'mnl_mode_choice' in self.models:
            model = self.models['mnl_mode_choice']
            report.append(f"- Model fit: Pseudo R² = {model.prsquared:.3f}\n")
            report.append("- Key factors affecting mode choice:\n")
            for param, coef in model.params.items():
                if param != 'const':
                    report.append(f"  - {param}: {coef:.3f}\n")
        
        # Welfare Optimization
        report.append("### 2. Welfare Optimization Results\n")
        if 'welfare_optimization' in self.results:
            for mode, results in self.results['welfare_optimization'].items():
                report.append(f"#### {mode}\n")
                for obj, result in results.items():
                    report.append(f"- {obj}: Optimal fare = {result['optimal_fare']:.1f} BDT\n")
        
        # Policy Recommendations
        report.append("## Policy Recommendations\n")
        report.append("Based on the analysis, the following policy recommendations are proposed:\n")
        report.append("1. **Implement differentiated pricing** based on income groups\n")
        report.append("2. **Subsidize low-income users** to improve accessibility\n")
        report.append("3. **Optimize fare levels** using social welfare maximization\n")
        report.append("4. **Consider environmental externalities** in pricing\n")
        report.append("5. **Monitor and evaluate** policy impacts regularly\n")
        
        # Save report
        with open("transport_analysis_report.md", "w") as f:
            f.writelines(report)
        
        print("Report saved as 'transport_analysis_report.md'")
        return report
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting Complete Transport Fare Analysis...")
        print("=" * 50)
        
        # Run all analyses
        self.analyze_mode_choice_preferences()
        self.analyze_affordability_and_wtp()
        self.model_social_welfare_outcomes()
        self.compare_cumulative_welfare()
        self.analyze_travel_time_factors()
        self.evaluate_equity_policies()
        
        # Generate outputs
        self.generate_visualizations()
        self.generate_report()
        
        print("\n" + "=" * 50)
        print("Analysis Complete!")
        print("Generated files:")
        print("- transport_analysis_dashboard.html")
        print("- transport_analysis_report.md")
        print("=" * 50)


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = TransportFareAnalyzer()
    
    # Load data (using sample data for demonstration)
    analyzer.load_data()
    
    # Run complete analysis
    analyzer.run_complete_analysis()