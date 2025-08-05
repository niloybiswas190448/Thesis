#!/usr/bin/env python3
"""
Simplified Demo of Dhaka Transport Fare Analysis Framework
========================================================

This script demonstrates the analysis framework structure without requiring
external dependencies. It shows the methodology and approach for optimizing
Dhaka's public transport fare system.

Author: [Your Name]
Date: [Current Date]
"""

import random
import math
from datetime import datetime

class SimpleTransportAnalyzer:
    """
    Simplified transport fare analyzer for demonstration
    """
    
    def __init__(self):
        self.sp_data = []
        self.income_fare_matrix = []
        self.secondary_data = []
        self.results = {}
        
    def generate_sample_data(self):
        """Generate sample data for demonstration"""
        print("Generating sample data...")
        
        # Generate SP data
        modes = ['Bus', 'Rickshaw', 'MRT', 'Private Car']
        income_groups = ['Low', 'Medium', 'High']
        
        for i in range(100):  # 100 respondents
            income_group = random.choice(income_groups)
            income = {
                'Low': random.randint(10000, 25000),
                'Medium': random.randint(25000, 50000),
                'High': random.randint(50000, 100000)
            }[income_group]
            
            for mode in modes:
                for scenario in range(3):
                    fare = random.uniform(10, 100)
                    travel_time = random.uniform(15, 90)
                    waiting_time = random.uniform(2, 20)
                    comfort_score = random.uniform(1, 5)
                    
                    # Calculate utility
                    utility = (
                        -0.1 * fare + 
                        -0.05 * travel_time + 
                        -0.02 * waiting_time + 
                        0.3 * comfort_score +
                        random.normalvariate(0, 1)
                    )
                    
                    self.sp_data.append({
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
                        'chosen': 0
                    })
        
        # Determine chosen modes
        for scenario in range(3):
            for respondent in range(100):
                respondent_data = [d for d in self.sp_data 
                                 if d['respondent_id'] == respondent and d['scenario'] == scenario]
                if respondent_data:
                    best_choice = max(respondent_data, key=lambda x: x['utility'])
                    best_choice['chosen'] = 1
        
        # Generate income-fare matrix
        for income in range(10000, 100001, 5000):
            for fare in range(10, 101, 5):
                wtp = max(0, 0.3 * income - 2 * fare + random.normalvariate(0, 1000))
                affordability = max(0, 1 - (fare / (income * 0.1)))
                
                self.income_fare_matrix.append({
                    'income': income,
                    'fare': fare,
                    'willingness_to_pay': wtp,
                    'affordability_score': affordability
                })
        
        # Generate secondary data
        for mode in modes:
            self.secondary_data.append({
                'mode': mode,
                'operator_cost_per_km': random.uniform(5, 25),
                'emissions_per_km': random.uniform(50, 200),
                'capacity': random.uniform(20, 200),
                'infrastructure_cost': random.uniform(1000000, 10000000),
                'maintenance_cost': random.uniform(1000, 10000)
            })
        
        print(f"Generated {len(self.sp_data)} SP observations")
        print(f"Generated {len(self.income_fare_matrix)} income-fare combinations")
        print(f"Generated {len(self.secondary_data)} mode records")
    
    def analyze_mode_choice_preferences(self):
        """Analyze mode choice preferences"""
        print("\n=== Analyzing Mode Choice Preferences ===")
        
        # Calculate mode shares
        mode_shares = {}
        for mode in ['Bus', 'Rickshaw', 'MRT', 'Private Car']:
            mode_data = [d for d in self.sp_data if d['mode'] == mode]
            chosen_count = sum(1 for d in mode_data if d['chosen'] == 1)
            mode_shares[mode] = chosen_count / len(mode_data) if mode_data else 0
        
        # Analyze by income group
        income_analysis = {}
        for income_group in ['Low', 'Medium', 'High']:
            group_data = [d for d in self.sp_data if d['income_group'] == income_group]
            group_shares = {}
            for mode in ['Bus', 'Rickshaw', 'MRT', 'Private Car']:
                mode_data = [d for d in group_data if d['mode'] == mode]
                chosen_count = sum(1 for d in mode_data if d['chosen'] == 1)
                group_shares[mode] = chosen_count / len(mode_data) if mode_data else 0
            income_analysis[income_group] = group_shares
        
        self.results['mode_shares'] = mode_shares
        self.results['income_analysis'] = income_analysis
        
        print("Mode Shares:")
        for mode, share in mode_shares.items():
            print(f"  {mode}: {share:.3f}")
        
        print("\nMode Shares by Income Group:")
        for income_group, shares in income_analysis.items():
            print(f"  {income_group}:")
            for mode, share in shares.items():
                print(f"    {mode}: {share:.3f}")
        
        return mode_shares, income_analysis
    
    def analyze_affordability_and_wtp(self):
        """Analyze affordability and willingness to pay"""
        print("\n=== Analyzing Affordability and Willingness to Pay ===")
        
        # Calculate fare elasticity by income group
        elasticity_results = {}
        for income_group in ['Low', 'Medium', 'High']:
            group_data = [d for d in self.sp_data if d['income_group'] == income_group]
            
            # Simple elasticity calculation
            avg_fare = sum(d['fare'] for d in group_data) / len(group_data)
            avg_demand = sum(d['chosen'] for d in group_data) / len(group_data)
            
            # Simulate elasticity (in practice, this would be calculated from actual data)
            elasticity = random.uniform(-2.0, -0.5)  # Negative elasticity
            elasticity_results[income_group] = elasticity
        
        # WTP analysis
        wtp_analysis = {}
        for income_group in ['Low', 'Medium', 'High']:
            group_data = [d for d in self.sp_data if d['income_group'] == income_group]
            avg_income = sum(d['income'] for d in group_data) / len(group_data)
            avg_fare = sum(d['fare'] for d in group_data) / len(group_data)
            
            wtp = avg_income * 0.15  # Assume 15% of income as WTP
            affordability_ratio = avg_fare / wtp
            
            wtp_analysis[income_group] = {
                'avg_income': avg_income,
                'avg_fare': avg_fare,
                'wtp_threshold': wtp,
                'affordability_ratio': affordability_ratio
            }
        
        self.results['fare_elasticity'] = elasticity_results
        self.results['wtp_analysis'] = wtp_analysis
        
        print("Fare Elasticity by Income Group:")
        for group, elasticity in elasticity_results.items():
            print(f"  {group}: {elasticity:.3f}")
        
        print("\nWillingness to Pay Analysis:")
        for group, analysis in wtp_analysis.items():
            print(f"  {group}: WTP = {analysis['wtp_threshold']:.0f} BDT, "
                  f"Affordability Ratio = {analysis['affordability_ratio']:.2f}")
        
        return elasticity_results, wtp_analysis
    
    def model_social_welfare_outcomes(self):
        """Model social welfare outcomes"""
        print("\n=== Modeling Social Welfare Outcomes ===")
        
        optimization_results = {}
        modes = ['Bus', 'Rickshaw', 'MRT', 'Private Car']
        
        for mode in modes:
            mode_data = [d for d in self.sp_data if d['mode'] == mode]
            secondary_mode_data = [d for d in self.secondary_data if d['mode'] == mode][0]
            
            avg_fare = sum(d['fare'] for d in mode_data) / len(mode_data)
            avg_demand = sum(d['chosen'] for d in mode_data) / len(mode_data)
            operator_cost = secondary_mode_data['operator_cost_per_km']
            
            # Calculate optimal fares for different objectives
            mode_results = {}
            
            # Max-R (Revenue)
            optimal_fare_r = avg_fare * 1.2  # 20% increase for revenue maximization
            mode_results['Max-R'] = {
                'optimal_fare': optimal_fare_r,
                'objective_value': optimal_fare_r * avg_demand * 0.8  # Reduced demand
            }
            
            # Max-P (Profit)
            optimal_fare_p = avg_fare * 1.1  # 10% increase for profit maximization
            mode_results['Max-P'] = {
                'optimal_fare': optimal_fare_p,
                'objective_value': (optimal_fare_p - operator_cost) * avg_demand * 0.9
            }
            
            # Max-B (Benefit)
            optimal_fare_b = avg_fare * 0.8  # 20% decrease for benefit maximization
            mode_results['Max-B'] = {
                'optimal_fare': optimal_fare_b,
                'objective_value': (avg_fare - optimal_fare_b) * avg_demand * 1.2
            }
            
            # Max-D (Demand)
            optimal_fare_d = avg_fare * 0.7  # 30% decrease for demand maximization
            mode_results['Max-D'] = {
                'optimal_fare': optimal_fare_d,
                'objective_value': avg_demand * 1.5
            }
            
            # Max-S (Social Welfare)
            optimal_fare_s = avg_fare * 0.9  # 10% decrease for social welfare
            mode_results['Max-S'] = {
                'optimal_fare': optimal_fare_s,
                'objective_value': (avg_fare - optimal_fare_s) * avg_demand * 1.1 + 
                                 (optimal_fare_s - operator_cost) * avg_demand * 0.9
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
        """Compare cumulative social welfare"""
        print("\n=== Comparing Cumulative Social Welfare ===")
        
        # Define criteria weights
        criteria_weights = {
            'economic_efficiency': 0.3,
            'social_equity': 0.25,
            'environmental_impact': 0.2,
            'accessibility': 0.15,
            'sustainability': 0.1
        }
        
        mcda_results = {}
        modes = ['Bus', 'Rickshaw', 'MRT', 'Private Car']
        
        for mode in modes:
            mode_data = [d for d in self.sp_data if d['mode'] == mode]
            secondary_mode_data = [d for d in self.secondary_data if d['mode'] == mode][0]
            
            # Calculate scores for each criterion
            avg_fare = sum(d['fare'] for d in mode_data) / len(mode_data)
            avg_demand = sum(d['chosen'] for d in mode_data) / len(mode_data)
            
            # Economic efficiency (revenue - cost)
            economic_score = (avg_fare * avg_demand - secondary_mode_data['operator_cost_per_km'] * avg_demand) / 1000
            
            # Social equity (accessibility across income groups)
            equity_scores = []
            for income_group in ['Low', 'Medium', 'High']:
                group_data = [d for d in mode_data if d['income_group'] == income_group]
                if group_data:
                    group_usage = sum(d['chosen'] for d in group_data) / len(group_data)
                    equity_scores.append(group_usage)
            social_equity_score = sum(equity_scores) / len(equity_scores) if equity_scores else 0
            
            # Environmental impact (inverse of emissions)
            environmental_score = 1 / (secondary_mode_data['emissions_per_km'] / 100)
            
            # Accessibility (inverse of travel time)
            avg_travel_time = sum(d['travel_time'] for d in mode_data) / len(mode_data)
            accessibility_score = 1 / (avg_travel_time / 60)
            
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
    
    def evaluate_equity_policies(self):
        """Evaluate equity policies"""
        print("\n=== Evaluating Equity Policies ===")
        
        policy_scenarios = {
            'baseline': {'subsidy_rate': 0.0, 'subsidy_cap': 0.0},
            'low_income_subsidy': {'subsidy_rate': 0.3, 'subsidy_cap': 0.1},
            'universal_subsidy': {'subsidy_rate': 0.2, 'subsidy_cap': 0.15},
            'progressive_subsidy': {'subsidy_rate': 0.4, 'subsidy_cap': 0.12}
        }
        
        policy_results = {}
        
        for scenario_name, policy_params in policy_scenarios.items():
            scenario_results = {}
            
            for mode in ['Bus', 'Rickshaw', 'MRT', 'Private Car']:
                mode_data = [d for d in self.sp_data if d['mode'] == mode]
                
                # Calculate subsidy and impacts
                total_subsidy = 0
                demand_change = 0
                
                if policy_params['subsidy_rate'] > 0:
                    for income_group in ['Low', 'Medium', 'High']:
                        group_data = [d for d in mode_data if d['income_group'] == income_group]
                        
                        if income_group == 'Low':
                            subsidy_multiplier = policy_params['subsidy_rate']
                        elif income_group == 'Medium':
                            subsidy_multiplier = policy_params['subsidy_rate'] * 0.5
                        else:  # High income
                            subsidy_multiplier = 0
                        
                        for data_point in group_data:
                            subsidy = data_point['fare'] * subsidy_multiplier
                            max_subsidy = data_point['fare'] * policy_params['subsidy_cap']
                            actual_subsidy = min(subsidy, max_subsidy)
                            total_subsidy += actual_subsidy
                            demand_change += 0.1  # Assume 10% demand increase per subsidized trip
                
                scenario_results[mode] = {
                    'total_subsidy': total_subsidy,
                    'demand_change': demand_change
                }
            
            policy_results[scenario_name] = scenario_results
        
        self.results['policy_evaluation'] = policy_results
        
        print("Policy Evaluation Results:")
        for scenario, results in policy_results.items():
            print(f"\n{scenario.upper()}:")
            total_subsidy = sum(r['total_subsidy'] for r in results.values())
            print(f"  Total Subsidy: {total_subsidy:.0f} BDT")
            
            for mode, mode_results in results.items():
                print(f"  {mode}:")
                print(f"    Demand Change: {mode_results['demand_change']:+.0f}")
                print(f"    Subsidy: {mode_results['total_subsidy']:.0f} BDT")
        
        return policy_results
    
    def generate_report(self):
        """Generate analysis report"""
        print("\n=== Generating Analysis Report ===")
        
        report = []
        report.append("# Dhaka Transport Fare System Optimization Analysis Report\n")
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
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
            scenarios = list(self.results['policy_evaluation'].keys())
            report.append(f"- **Policy Scenarios Analyzed**: {len(scenarios)}\n")
        
        # Detailed Analysis
        report.append("## Detailed Analysis\n")
        
        # Mode Choice Analysis
        report.append("### 1. Mode Choice Preferences\n")
        if 'mode_shares' in self.results:
            report.append("- Mode shares across the population:\n")
            for mode, share in self.results['mode_shares'].items():
                report.append(f"  - {mode}: {share:.3f}\n")
        
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
        with open("simple_analysis_report.md", "w") as f:
            f.writelines(report)
        
        print("Report saved as 'simple_analysis_report.md'")
        return report
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("Starting Complete Transport Fare Analysis...")
        print("=" * 50)
        
        # Generate sample data
        self.generate_sample_data()
        
        # Run all analyses
        self.analyze_mode_choice_preferences()
        self.analyze_affordability_and_wtp()
        self.model_social_welfare_outcomes()
        self.compare_cumulative_welfare()
        self.evaluate_equity_policies()
        
        # Generate report
        self.generate_report()
        
        print("\n" + "=" * 50)
        print("Analysis Complete!")
        print("Generated files:")
        print("- simple_analysis_report.md")
        print("=" * 50)

def main():
    """Main function"""
    print("Dhaka Transport Fare System Optimization Analysis")
    print("Simplified Demo Version")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SimpleTransportAnalyzer()
    
    # Run complete analysis
    analyzer.run_complete_analysis()
    
    print("\nKey Insights:")
    print("1. The framework successfully analyzes mode choice preferences")
    print("2. Affordability constraints are identified across income groups")
    print("3. Welfare optimization provides optimal fare recommendations")
    print("4. MCDA helps compare different transport modes")
    print("5. Policy evaluation shows impact of different subsidy schemes")
    
    print("\nNext Steps:")
    print("1. Replace sample data with actual SP survey data")
    print("2. Install required packages for advanced visualizations")
    print("3. Customize analysis parameters for specific requirements")
    print("4. Integrate with real-time data sources")

if __name__ == "__main__":
    main()