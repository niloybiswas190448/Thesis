#!/usr/bin/env python3
"""
Simplified Dhaka Public Transport Fare System Optimization Analysis
==================================================================

This script provides a simplified demonstration of the comprehensive analysis
framework for optimizing Dhaka's public transport fare system.

This version uses only basic Python packages and demonstrates the key concepts
without requiring additional dependencies.
"""

import csv
import json
import math
import random
from datetime import datetime

class SimplifiedThesisAnalyzer:
    """
    Simplified analysis framework for Dhaka public transport fare system optimization
    """
    
    def __init__(self):
        self.sp_data = []
        self.results = {}
        
    def load_data(self, filename='dhaka_sp_survey_no_rickshaw_minibus.csv'):
        """Load and prepare data for analysis"""
        print("="*80)
        print("LOADING DATA FOR SIMPLIFIED THESIS ANALYSIS")
        print("="*80)
        
        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                self.sp_data = list(reader)
            
            print(f"✓ Loaded {len(self.sp_data)} observations from {filename}")
            print(f"Data columns: {list(self.sp_data[0].keys())}")
            
        except FileNotFoundError:
            print(f"✗ File {filename} not found. Using sample data.")
            self._generate_sample_data()
        
        # Preprocess data
        self._preprocess_data()
        
    def _generate_sample_data(self):
        """Generate sample data for demonstration"""
        print("Generating sample data...")
        
        modes = ['Bus', 'MRT', 'Leguna']
        income_groups = ['Low', 'Mid', 'High']
        
        for i in range(100):
            income_group = random.choice(income_groups)
            mode = random.choice(modes)
            
            # Generate realistic values based on income group
            if income_group == 'Low':
                fare = random.uniform(20, 60)
                wtp = random.uniform(30, 80)
                travel_time = random.uniform(30, 90)
            elif income_group == 'Mid':
                fare = random.uniform(40, 100)
                wtp = random.uniform(60, 120)
                travel_time = random.uniform(20, 70)
            else:  # High
                fare = random.uniform(60, 120)
                wtp = random.uniform(100, 200)
                travel_time = random.uniform(15, 50)
            
            self.sp_data.append({
                'respondent_id': str(i + 1),
                'Mode_Used': mode,
                'Income_Bracket': income_group,
                'Fare_Paid': str(round(fare, 2)),
                'WTP': str(round(wtp, 2)),
                'Travel_Time': str(round(travel_time, 2)),
                'Wait_Time': str(round(random.uniform(5, 20), 2)),
                'Comfort_Level': str(random.randint(1, 5))
            })
    
    def _preprocess_data(self):
        """Preprocess the data"""
        print("Preprocessing data...")
        
        for row in self.sp_data:
            # Convert string values to float
            row['Fare_Paid'] = float(row['Fare_Paid'])
            row['WTP'] = float(row['WTP'])
            row['Travel_Time'] = float(row['Travel_Time'])
            row['Wait_Time'] = float(row['Wait_Time'])
            row['Comfort_Level'] = int(row['Comfort_Level'])
            
            # Calculate derived variables
            row['total_time'] = row['Travel_Time'] + row['Wait_Time']
            row['affordability_ratio'] = row['Fare_Paid'] / row['WTP']
            row['time_value'] = row['WTP'] / row['total_time']
        
        print(f"✓ Preprocessed {len(self.sp_data)} observations")
    
    def objective_1_analyze_user_preferences_and_affordability(self):
        """
        Objective 1: Assessing User Preferences and Affordability Constraints
        """
        print("\n" + "="*80)
        print("OBJECTIVE 1: ANALYZING USER PREFERENCES AND AFFORDABILITY")
        print("="*80)
        
        # 1.1 Mode Choice Analysis by Income Groups
        print("\n1.1 Mode Choice Preferences by Income Groups...")
        
        mode_choice_analysis = {}
        income_groups = ['Low', 'Mid', 'High']
        modes = ['Bus', 'MRT', 'Leguna']
        
        for income_group in income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            mode_counts = {}
            for mode in modes:
                mode_counts[mode] = len([row for row in group_data if row['Mode_Used'] == mode])
            
            mode_choice_analysis[income_group] = {
                'mode_counts': mode_counts,
                'total_respondents': len(group_data),
                'mode_shares': {mode: count/len(group_data) for mode, count in mode_counts.items()}
            }
            
            print(f"✓ {income_group} income group analysis:")
            for mode, count in mode_counts.items():
                share = count / len(group_data) * 100
                print(f"  {mode}: {count} users ({share:.1f}%)")
        
        # 1.2 Affordability and Willingness to Pay Analysis
        print("\n1.2 Affordability and Willingness to Pay Analysis...")
        
        wtp_analysis = {}
        affordability_analysis = {}
        
        for income_group in income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            # Calculate WTP statistics
            wtp_values = [row['WTP'] for row in group_data]
            wtp_stats = {
                'mean_wtp': sum(wtp_values) / len(wtp_values),
                'median_wtp': sorted(wtp_values)[len(wtp_values)//2],
                'min_wtp': min(wtp_values),
                'max_wtp': max(wtp_values)
            }
            
            # Calculate affordability metrics
            affordability_ratios = [row['affordability_ratio'] for row in group_data]
            unaffordable_count = len([r for r in affordability_ratios if r > 1])
            
            affordability_stats = {
                'mean_affordability_ratio': sum(affordability_ratios) / len(affordability_ratios),
                'unaffordable_trips': unaffordable_count,
                'unaffordable_percentage': unaffordable_count / len(group_data) * 100
            }
            
            wtp_analysis[income_group] = wtp_stats
            affordability_analysis[income_group] = affordability_stats
            
            print(f"✓ {income_group} income group:")
            print(f"  Mean WTP: {wtp_stats['mean_wtp']:.2f} BDT")
            print(f"  Unaffordable trips: {affordability_stats['unaffordable_percentage']:.1f}%")
        
        # Store results
        self.results['objective_1'] = {
            'mode_choice_analysis': mode_choice_analysis,
            'wtp_analysis': wtp_analysis,
            'affordability_analysis': affordability_analysis
        }
        
        return mode_choice_analysis, wtp_analysis, affordability_analysis
    
    def objective_2_model_social_welfare_outcomes(self):
        """
        Objective 2: Modeling and Comparing Social Welfare Outcomes
        """
        print("\n" + "="*80)
        print("OBJECTIVE 2: MODELING SOCIAL WELFARE OUTCOMES")
        print("="*80)
        
        # 2.1 Welfare Optimization Models
        print("\n2.1 Quantifying Welfare Outcomes Under Different Scenarios...")
        
        welfare_results = {}
        modes = ['Bus', 'MRT', 'Leguna']
        
        for mode in modes:
            mode_data = [row for row in self.sp_data if row['Mode_Used'] == mode]
            
            if mode_data:
                # Calculate base statistics
                base_demand = len(mode_data)
                base_price = sum(row['Fare_Paid'] for row in mode_data) / len(mode_data)
                
                # Simulate different optimization scenarios
                # Max-R (Revenue Maximization)
                max_r_price = base_price * 1.2  # 20% increase
                max_r_revenue = max_r_price * base_demand * 0.8  # Assume 20% demand reduction
                
                # Max-P (Profit Maximization)
                max_p_price = base_price * 1.1  # 10% increase
                max_p_profit = max_p_price * base_demand * 0.9 - base_demand * 20  # Assume 20 BDT cost per trip
                
                # Max-S (Social Welfare Maximization)
                max_s_price = base_price * 0.9  # 10% decrease for social welfare
                max_s_welfare = max_s_price * base_demand * 1.1 + base_demand * 10  # Include consumer surplus
                
                welfare_results[mode] = {
                    'max_revenue': {'optimal_price': max_r_price, 'optimal_revenue': max_r_revenue},
                    'max_profit': {'optimal_price': max_p_price, 'optimal_revenue': max_p_profit},
                    'max_social_welfare': {'optimal_price': max_s_price, 'optimal_revenue': max_s_welfare},
                    'base_demand': base_demand,
                    'base_price': base_price
                }
                
                print(f"✓ {mode} welfare analysis:")
                print(f"  Optimal social welfare price: {max_s_price:.2f} BDT")
                print(f"  Social welfare: {max_s_welfare:.2f}")
        
        # 2.2 Multi-Criteria Decision Analysis (MCDA)
        print("\n2.2 Comparing Cumulative Social Welfare Impacts Across Modes...")
        
        mcda_results = self._perform_simplified_mcda(welfare_results)
        
        # Store results
        self.results['objective_2'] = {
            'welfare_results': welfare_results,
            'mcda_results': mcda_results
        }
        
        return welfare_results, mcda_results
    
    def objective_3_analyze_travel_time_and_key_factors(self):
        """
        Objective 3: Examining Travel Time and Key Factors
        """
        print("\n" + "="*80)
        print("OBJECTIVE 3: ANALYZING TRAVEL TIME AND KEY FACTORS")
        print("="*80)
        
        # 3.1 Value of Time Analysis
        print("\n3.1 Analyzing Travel Time and Transfer Factors...")
        
        vot_analysis = {}
        income_groups = ['Low', 'Mid', 'High']
        
        for income_group in income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            # Calculate value of time
            time_values = [row['time_value'] for row in group_data]
            vot_per_hour = sum(time_values) / len(time_values) * 60  # Convert to per hour
            
            vot_analysis[income_group] = {
                'mean_vot': sum(time_values) / len(time_values),
                'vot_per_hour': vot_per_hour
            }
            
            print(f"✓ {income_group} income group VOT analysis:")
            print(f"  Mean VOT: {vot_analysis[income_group]['mean_vot']:.2f} per minute")
            print(f"  VOT per hour: {vot_per_hour:.2f} BDT/hour")
        
        # 3.2 Generalized Cost Analysis
        print("\n3.2 Generalized Cost Analysis...")
        
        gc_analysis = {}
        modes = ['Bus', 'MRT', 'Leguna']
        
        for mode in modes:
            mode_data = [row for row in self.sp_data if row['Mode_Used'] == mode]
            
            if mode_data:
                # Calculate generalized cost (fare + time cost + waiting penalty)
                gc_values = []
                for row in mode_data:
                    gc = row['Fare_Paid'] + row['total_time'] * row['time_value'] + row['Wait_Time'] * row['time_value'] * 1.5
                    gc_values.append(gc)
                
                gc_analysis[mode] = {
                    'mean_gc': sum(gc_values) / len(gc_values),
                    'min_gc': min(gc_values),
                    'max_gc': max(gc_values)
                }
                
                print(f"✓ {mode} generalized cost:")
                print(f"  Mean GC: {gc_analysis[mode]['mean_gc']:.2f} BDT")
        
        # 3.3 Equity-Sensitive Policy Analysis
        print("\n3.3 Evaluating Equity-Sensitive Fare/Subsidy Policies...")
        
        policy_analysis = self._evaluate_simplified_policies()
        
        # Store results
        self.results['objective_3'] = {
            'vot_analysis': vot_analysis,
            'generalized_cost_analysis': gc_analysis,
            'policy_analysis': policy_analysis
        }
        
        return vot_analysis, gc_analysis, policy_analysis
    
    def _perform_simplified_mcda(self, welfare_results):
        """Perform simplified Multi-Criteria Decision Analysis"""
        print("Performing Multi-Criteria Decision Analysis...")
        
        # Define criteria weights
        weights = {
            'social_welfare': 0.4,
            'revenue': 0.2,
            'profit': 0.2,
            'demand': 0.1,
            'equity': 0.1
        }
        
        mcda_scores = {}
        
        for mode, results in welfare_results.items():
            # Calculate normalized scores
            max_welfare = max([r['max_social_welfare']['optimal_revenue'] for r in welfare_results.values()])
            max_revenue = max([r['max_revenue']['optimal_revenue'] for r in welfare_results.values()])
            max_profit = max([r['max_profit']['optimal_revenue'] for r in welfare_results.values()])
            max_demand = max([r['base_demand'] for r in welfare_results.values()])
            
            scores = {
                'social_welfare': results['max_social_welfare']['optimal_revenue'] / max_welfare,
                'revenue': results['max_revenue']['optimal_revenue'] / max_revenue,
                'profit': results['max_profit']['optimal_revenue'] / max_profit,
                'demand': results['base_demand'] / max_demand,
                'equity': 0.8  # Simplified equity score
            }
            
            # Calculate weighted score
            weighted_score = sum(scores[criterion] * weight for criterion, weight in weights.items())
            
            mcda_scores[mode] = {
                'scores': scores,
                'weighted_score': weighted_score
            }
            
            print(f"✓ {mode} MCDA score: {weighted_score:.3f}")
        
        return mcda_scores
    
    def _evaluate_simplified_policies(self):
        """Evaluate simplified equity-sensitive policies"""
        print("Evaluating equity-sensitive policies...")
        
        policies = {
            'current': {'low_subsidy': 0, 'mid_subsidy': 0, 'high_subsidy': 0},
            'progressive_subsidy': {'low_subsidy': 0.3, 'mid_subsidy': 0.15, 'high_subsidy': 0},
            'universal_subsidy': {'low_subsidy': 0.2, 'mid_subsidy': 0.2, 'high_subsidy': 0.2},
            'targeted_subsidy': {'low_subsidy': 0.4, 'mid_subsidy': 0.1, 'high_subsidy': 0}
        }
        
        policy_results = {}
        
        for policy_name, subsidy_rates in policies.items():
            print(f"\nEvaluating {policy_name} policy...")
            
            total_subsidy_cost = 0
            accessibility_improvement = 0
            
            for income_group in ['Low', 'Mid', 'High']:
                group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
                subsidy_rate = subsidy_rates[f'{income_group.lower()}_subsidy']
                
                # Calculate subsidy cost
                subsidy_cost = sum(row['Fare_Paid'] * subsidy_rate for row in group_data)
                total_subsidy_cost += subsidy_cost
                
                # Calculate accessibility improvement
                original_unaffordable = len([row for row in group_data if row['affordability_ratio'] > 1])
                new_unaffordable = len([row for row in group_data if (row['Fare_Paid'] * (1 - subsidy_rate)) / row['WTP'] > 1])
                accessibility_improvement += (original_unaffordable - new_unaffordable)
            
            cost_effectiveness = accessibility_improvement / total_subsidy_cost if total_subsidy_cost > 0 else 0
            
            policy_results[policy_name] = {
                'total_subsidy_cost': total_subsidy_cost,
                'accessibility_improvement': accessibility_improvement,
                'cost_effectiveness': cost_effectiveness
            }
            
            print(f"  Total subsidy cost: {total_subsidy_cost:.2f}")
            print(f"  Accessibility improvement: {accessibility_improvement} trips")
            print(f"  Cost effectiveness: {cost_effectiveness:.3f}")
        
        return policy_results
    
    def generate_simplified_report(self):
        """Generate simplified analysis report"""
        print("\n" + "="*80)
        print("GENERATING SIMPLIFIED ANALYSIS REPORT")
        print("="*80)
        
        report = []
        report.append("# Dhaka Public Transport Fare System Optimization - Simplified Analysis Report")
        report.append("")
        report.append("## Executive Summary")
        report.append("")
        report.append("This report presents a simplified analysis of Dhaka's public transport fare system optimization,")
        report.append("demonstrating key analytical concepts and providing policy insights.")
        report.append("")
        
        # Objective 1 Summary
        if 'objective_1' in self.results:
            report.append("### Objective 1: User Preferences and Affordability Analysis")
            report.append("")
            
            wtp_analysis = self.results['objective_1']['wtp_analysis']
            affordability_analysis = self.results['objective_1']['affordability_analysis']
            
            report.append("#### Key Findings:")
            report.append("")
            
            for income_group in ['Low', 'Mid', 'High']:
                report.append(f"- **{income_group} Income Group:**")
                report.append(f"  - Mean WTP: {wtp_analysis[income_group]['mean_wtp']:.2f} BDT")
                report.append(f"  - Unaffordable trips: {affordability_analysis[income_group]['unaffordable_percentage']:.1f}%")
                report.append("")
        
        # Objective 2 Summary
        if 'objective_2' in self.results:
            report.append("### Objective 2: Social Welfare Optimization")
            report.append("")
            
            welfare_results = self.results['objective_2']['welfare_results']
            mcda_results = self.results['objective_2']['mcda_results']
            
            report.append("#### Optimal Fare Levels by Mode:")
            report.append("")
            
            for mode, results in welfare_results.items():
                optimal_price = results['max_social_welfare']['optimal_price']
                social_welfare = results['max_social_welfare']['optimal_revenue']
                report.append(f"- **{mode}:** Optimal fare = {optimal_price:.2f} BDT, Social welfare = {social_welfare:.2f}")
            
            report.append("")
            report.append("#### MCDA Ranking:")
            report.append("")
            
            sorted_modes = sorted(mcda_results.items(), key=lambda x: x[1]['weighted_score'], reverse=True)
            for i, (mode, result) in enumerate(sorted_modes, 1):
                report.append(f"{i}. **{mode}:** Score = {result['weighted_score']:.3f}")
        
        # Objective 3 Summary
        if 'objective_3' in self.results:
            report.append("### Objective 3: Travel Time and Equity Analysis")
            report.append("")
            
            vot_analysis = self.results['objective_3']['vot_analysis']
            policy_analysis = self.results['objective_3']['policy_analysis']
            
            report.append("#### Value of Time by Income Group:")
            report.append("")
            
            for income_group in ['Low', 'Mid', 'High']:
                vot_per_hour = vot_analysis[income_group]['vot_per_hour']
                report.append(f"- **{income_group}:** {vot_per_hour:.2f} BDT/hour")
            
            report.append("")
            report.append("#### Policy Recommendations:")
            report.append("")
            
            # Find best policy
            best_policy = max(policy_analysis.items(), key=lambda x: x[1]['cost_effectiveness'])
            report.append(f"- **Recommended Policy:** {best_policy[0].replace('_', ' ').title()}")
            report.append(f"- **Cost Effectiveness:** {best_policy[1]['cost_effectiveness']:.3f}")
            report.append(f"- **Total Cost:** {best_policy[1]['total_subsidy_cost']:.2f} BDT")
        
        # Policy Recommendations
        report.append("## Policy Recommendations")
        report.append("")
        report.append("### 1. Differentiated Pricing Strategy")
        report.append("- Implement income-based fare differentiation")
        report.append("- Provide targeted subsidies for low-income users")
        report.append("- Consider social welfare maximization as primary objective")
        report.append("")
        
        report.append("### 2. Service Quality Improvements")
        report.append("- Reduce waiting times, especially for high-value modes")
        report.append("- Improve comfort levels across all modes")
        report.append("- Enhance reliability and frequency")
        report.append("")
        
        report.append("### 3. Equity and Accessibility")
        report.append("- Implement progressive subsidy structure")
        report.append("- Monitor affordability thresholds by income group")
        report.append("- Regular assessment of policy effectiveness")
        
        # Save report
        with open('simplified_thesis_report.md', 'w') as f:
            f.write('\n'.join(report))
        
        print("✓ Simplified report generated: simplified_thesis_report.md")
        
        return '\n'.join(report)
    
    def generate_json_results(self):
        """Generate JSON results for further analysis"""
        print("Generating JSON results...")
        
        # Convert results to JSON-serializable format
        json_results = {}
        
        for objective, results in self.results.items():
            json_results[objective] = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    json_results[objective][key] = {}
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, dict):
                            json_results[objective][key][subkey] = {}
                            for subsubkey, subsubvalue in subvalue.items():
                                if isinstance(subsubvalue, (int, float, str)):
                                    json_results[objective][key][subkey][subsubkey] = subsubvalue
                        elif isinstance(subvalue, (int, float, str)):
                            json_results[objective][key][subkey] = subvalue
        
        # Save JSON results
        with open('thesis_analysis_results.json', 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print("✓ JSON results generated: thesis_analysis_results.json")
        
        return json_results
    
    def run_complete_analysis(self):
        """Run complete simplified analysis"""
        print("="*80)
        print("RUNNING SIMPLIFIED COMPREHENSIVE THESIS ANALYSIS")
        print("="*80)
        
        # Load data
        self.load_data()
        
        # Run all objectives
        print("\nRunning all analysis objectives...")
        
        # Objective 1
        obj1_results = self.objective_1_analyze_user_preferences_and_affordability()
        
        # Objective 2
        obj2_results = self.objective_2_model_social_welfare_outcomes()
        
        # Objective 3
        obj3_results = self.objective_3_analyze_travel_time_and_key_factors()
        
        # Generate outputs
        print("\nGenerating analysis outputs...")
        
        # Generate report
        self.generate_simplified_report()
        
        # Generate JSON results
        self.generate_json_results()
        
        print("\n" + "="*80)
        print("SIMPLIFIED ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nGenerated Files:")
        print("- simplified_thesis_report.md (Analysis report)")
        print("- thesis_analysis_results.json (Structured results)")
        print("\nKey Results Summary:")
        print(f"- Analyzed {len(self.sp_data)} transport trips")
        print(f"- Evaluated {len(set(row['Mode_Used'] for row in self.sp_data))} transport modes")
        print(f"- Assessed {len(set(row['Income_Bracket'] for row in self.sp_data))} income groups")
        
        return self.results

# Example usage
if __name__ == "__main__":
    # Initialize simplified analyzer
    analyzer = SimplifiedThesisAnalyzer()
    
    # Run complete analysis
    results = analyzer.run_complete_analysis()
    
    print("\nAnalysis completed! Check the generated files for detailed results.")