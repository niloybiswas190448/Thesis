#!/usr/bin/env python3
"""
Enhanced Dhaka Public Transport Fare System Optimization Analysis
================================================================

This script provides a comprehensive analysis framework for optimizing Dhaka's 
public transport fare system, addressing all three main objectives with advanced
analytical techniques.

Key Features:
1. Advanced Discrete Choice Modeling (Multinomial Logit)
2. Sophisticated Welfare Optimization (Max-R, Max-P, Max-B, Max-D, Max-S)
3. Comprehensive Policy Evaluation with Equity Analysis
4. Multi-Criteria Decision Analysis
5. Environmental Externalities Assessment
"""

import csv
import json
import math
import random
import numpy as np
from datetime import datetime
from collections import defaultdict

class EnhancedThesisAnalyzer:
    """
    Enhanced analysis framework for Dhaka public transport fare system optimization
    """
    
    def __init__(self):
        self.sp_data = []
        self.results = {}
        self.income_groups = ['Low', 'Mid', 'High']
        self.transport_modes = ['Bus', 'MRT', 'Leguna']
        
    def load_data(self, filename='dhaka_sp_survey_no_rickshaw_minibus.csv'):
        """Load and prepare data for analysis"""
        print("="*80)
        print("LOADING DATA FOR ENHANCED THESIS ANALYSIS")
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
        """Generate comprehensive sample data for demonstration"""
        print("Generating comprehensive sample data...")
        
        modes = ['Bus', 'MRT', 'Leguna']
        income_groups = ['Low', 'Mid', 'High']
        trip_purposes = ['Work', 'School', 'Leisure']
        frequencies = ['Daily', 'Weekly', 'Occasional']
        
        for i in range(500):
            income_group = random.choice(income_groups)
            mode = random.choice(modes)
            purpose = random.choice(trip_purposes)
            frequency = random.choice(frequencies)
            
            # Generate realistic values based on income group and mode
            if income_group == 'Low':
                base_fare = random.uniform(20, 60)
                base_wtp = random.uniform(30, 80)
                travel_time = random.uniform(30, 90)
                wait_time = random.uniform(5, 25)
                comfort = random.randint(1, 3)
            elif income_group == 'Mid':
                base_fare = random.uniform(40, 100)
                base_wtp = random.uniform(60, 120)
                travel_time = random.uniform(20, 70)
                wait_time = random.uniform(3, 20)
                comfort = random.randint(2, 4)
            else:  # High
                base_fare = random.uniform(60, 120)
                base_wtp = random.uniform(100, 200)
                travel_time = random.uniform(15, 50)
                wait_time = random.uniform(2, 15)
                comfort = random.randint(3, 5)
            
            # Mode-specific adjustments
            if mode == 'MRT':
                base_fare *= 1.8
                travel_time *= 0.6
                comfort = max(comfort, 4)
            elif mode == 'Leguna':
                base_fare *= 0.7
                travel_time *= 1.2
                comfort = min(comfort, 2)
            
            self.sp_data.append({
                'respondent_id': str(i + 1),
                'Mode_Used': mode,
                'Origin_TAZ': f'Z{random.randint(1, 20)}',
                'Destination_TAZ': f'Z{random.randint(1, 20)}',
                'Income_Bracket': income_group,
                'Trip_Purpose': purpose,
                'Frequency_of_Use': frequency,
                'Travel_Time': str(round(travel_time, 2)),
                'Fare_Paid': str(round(base_fare, 2)),
                'Wait_Time': str(round(wait_time, 2)),
                'Comfort_Level': str(comfort),
                'WTP': str(round(base_wtp, 2)),
                'WTP_Lower_Fare': str(random.randint(0, 1)),
                'WTP_Higher_Comfort': str(random.randint(0, 1))
            })
    
    def _preprocess_data(self):
        """Preprocess the data with enhanced calculations"""
        print("Preprocessing data with enhanced calculations...")
        
        for row in self.sp_data:
            # Convert string values to appropriate types
            row['Fare_Paid'] = float(row['Fare_Paid'])
            row['WTP'] = float(row['WTP'])
            row['Travel_Time'] = float(row['Travel_Time'])
            row['Wait_Time'] = float(row['Wait_Time'])
            row['Comfort_Level'] = int(row['Comfort_Level'])
            row['WTP_Lower_Fare'] = int(row['WTP_Lower_Fare'])
            row['WTP_Higher_Comfort'] = int(row['WTP_Higher_Comfort'])
            
            # Calculate derived variables
            row['total_time'] = row['Travel_Time'] + row['Wait_Time']
            row['affordability_ratio'] = row['Fare_Paid'] / row['WTP']
            row['time_value'] = row['WTP'] / row['total_time']
            row['comfort_value'] = row['Comfort_Level'] * 10  # Comfort utility
            row['generalized_cost'] = row['Fare_Paid'] + (row['total_time'] * row['time_value'])
            
            # Calculate environmental factors (simplified)
            if row['Mode_Used'] == 'MRT':
                row['carbon_emissions'] = 0.05  # kg CO2/km
                row['environmental_cost'] = row['carbon_emissions'] * 0.5  # BDT
            elif row['Mode_Used'] == 'Bus':
                row['carbon_emissions'] = 0.08
                row['environmental_cost'] = row['carbon_emissions'] * 0.5
            else:  # Leguna
                row['carbon_emissions'] = 0.12
                row['environmental_cost'] = row['carbon_emissions'] * 0.5
        
        print(f"✓ Preprocessed {len(self.sp_data)} observations")

    def objective_1_analyze_user_preferences_and_affordability(self):
        """
        Objective 1: Assessing User Preferences and Affordability Constraints
        1.1 Assess how fare, travel time, and service quality affect mode choice
        1.2 Analyze affordability thresholds and willingness to pay
        """
        print("\n" + "="*80)
        print("OBJECTIVE 1: ANALYZING USER PREFERENCES AND AFFORDABILITY")
        print("="*80)
        
        results = {}
        
        # 1.1 Mode Choice Analysis by Income Groups
        print("\n1.1 Mode Choice Preferences by Income Groups...")
        mode_choice_results = {}
        
        for income_group in self.income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            mode_counts = defaultdict(int)
            
            for row in group_data:
                mode_counts[row['Mode_Used']] += 1
            
            total = len(group_data)
            mode_choice_results[income_group] = {
                'total_respondents': total,
                'mode_distribution': {mode: count for mode, count in mode_counts.items()},
                'mode_percentages': {mode: (count/total)*100 for mode, count in mode_counts.items()}
            }
            
            print(f"✓ {income_group} income group analysis:")
            for mode, count in mode_counts.items():
                percentage = (count/total)*100
                print(f"  {mode}: {count} users ({percentage:.1f}%)")
        
        results['mode_choice_analysis'] = mode_choice_results
        
        # 1.2 Discrete Choice Modeling (Simplified Multinomial Logit)
        print("\n1.2 Discrete Choice Modeling Analysis...")
        dcm_results = self._perform_discrete_choice_modeling()
        results['discrete_choice_modeling'] = dcm_results
        
        # 1.3 Affordability and Willingness to Pay Analysis
        print("\n1.3 Affordability and Willingness to Pay Analysis...")
        wtp_results = {}
        
        for income_group in self.income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            wtp_values = [row['WTP'] for row in group_data]
            affordability_ratios = [row['affordability_ratio'] for row in group_data]
            unaffordable_trips = sum(1 for ratio in affordability_ratios if ratio > 1.0)
            
            wtp_results[income_group] = {
                'mean_wtp': np.mean(wtp_values),
                'median_wtp': np.median(wtp_values),
                'min_wtp': min(wtp_values),
                'max_wtp': max(wtp_values),
                'mean_affordability_ratio': np.mean(affordability_ratios),
                'unaffordable_trips': unaffordable_trips,
                'unaffordable_percentage': (unaffordable_trips / len(group_data)) * 100,
                'fare_elasticity': self._calculate_fare_elasticity(group_data)
            }
            
            print(f"✓ {income_group} income group:")
            print(f"  Mean WTP: {wtp_results[income_group]['mean_wtp']:.2f} BDT")
            print(f"  Unaffordable trips: {wtp_results[income_group]['unaffordable_percentage']:.1f}%")
            print(f"  Fare elasticity: {wtp_results[income_group]['fare_elasticity']:.3f}")
        
        results['wtp_analysis'] = wtp_results
        
        # 1.4 Contingent Valuation Method (CVM) Analysis
        print("\n1.4 Contingent Valuation Method Analysis...")
        cvm_results = self._perform_cvm_analysis()
        results['cvm_analysis'] = cvm_results
        
        self.results['objective_1'] = results
        return results

    def _perform_discrete_choice_modeling(self):
        """Perform discrete choice modeling using simplified multinomial logit"""
        print("Performing discrete choice modeling...")
        
        # Simplified utility function parameters
        utility_params = {
            'fare_coefficient': -0.02,  # Negative because higher fare reduces utility
            'time_coefficient': -0.01,  # Negative because longer time reduces utility
            'comfort_coefficient': 0.1,  # Positive because higher comfort increases utility
            'income_coefficient': 0.005  # Positive because higher income increases utility
        }
        
        # Calculate utilities for each mode and respondent
        choice_probabilities = {}
        
        for income_group in self.income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            # Calculate average utilities for each mode
            mode_utilities = {}
            for mode in self.transport_modes:
                mode_data = [row for row in group_data if row['Mode_Used'] == mode]
                if mode_data:
                    avg_fare = np.mean([row['Fare_Paid'] for row in mode_data])
                    avg_time = np.mean([row['total_time'] for row in mode_data])
                    avg_comfort = np.mean([row['Comfort_Level'] for row in mode_data])
                    
                    # Income level (1=Low, 2=Mid, 3=High)
                    income_level = self.income_groups.index(income_group) + 1
                    
                    utility = (utility_params['fare_coefficient'] * avg_fare +
                             utility_params['time_coefficient'] * avg_time +
                             utility_params['comfort_coefficient'] * avg_comfort +
                             utility_params['income_coefficient'] * income_level)
                    
                    mode_utilities[mode] = utility
            
            # Calculate choice probabilities using logit formula
            total_utility = sum(math.exp(u) for u in mode_utilities.values())
            probabilities = {mode: math.exp(utility) / total_utility 
                           for mode, utility in mode_utilities.items()}
            
            choice_probabilities[income_group] = probabilities
        
        print("✓ Discrete choice modeling completed")
        return {
            'utility_parameters': utility_params,
            'choice_probabilities': choice_probabilities
        }

    def _calculate_fare_elasticity(self, group_data):
        """Calculate fare elasticity for a group"""
        fares = [row['Fare_Paid'] for row in group_data]
        demands = [1] * len(group_data)  # Simplified demand representation
        
        if len(fares) < 2:
            return 0.0
        
        # Simplified elasticity calculation
        mean_fare = np.mean(fares)
        mean_demand = np.mean(demands)
        
        # Calculate elasticity using linear approximation
        fare_changes = [fare - mean_fare for fare in fares]
        demand_changes = [demand - mean_demand for demand in demands]
        
        if mean_fare == 0 or mean_demand == 0:
            return 0.0
        
        elasticity = np.mean([(d/mean_demand) / (f/mean_fare) 
                            for f, d in zip(fare_changes, demand_changes) 
                            if f != 0])
        
        return abs(elasticity) if not np.isnan(elasticity) else 0.0

    def _perform_cvm_analysis(self):
        """Perform Contingent Valuation Method analysis"""
        print("Performing CVM analysis...")
        
        cvm_results = {}
        
        for income_group in self.income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            # Analyze willingness to pay for improvements
            wtp_lower_fare = [row for row in group_data if row['WTP_Lower_Fare'] == 1]
            wtp_higher_comfort = [row for row in group_data if row['WTP_Higher_Comfort'] == 1]
            
            # Calculate average WTP for improvements
            avg_wtp_fare_improvement = np.mean([row['WTP'] for row in wtp_lower_fare]) if wtp_lower_fare else 0
            avg_wtp_comfort_improvement = np.mean([row['WTP'] for row in wtp_higher_comfort]) if wtp_higher_comfort else 0
            
            cvm_results[income_group] = {
                'wtp_fare_improvement': avg_wtp_fare_improvement,
                'wtp_comfort_improvement': avg_wtp_comfort_improvement,
                'fare_improvement_acceptance_rate': len(wtp_lower_fare) / len(group_data),
                'comfort_improvement_acceptance_rate': len(wtp_higher_comfort) / len(group_data)
            }
        
        print("✓ CVM analysis completed")
        return cvm_results

    def objective_2_model_social_welfare_outcomes(self):
        """
        Objective 2: Modeling and Comparing Social Welfare Outcomes
        2.1 Quantify welfare outcomes under different mode-specific scenarios
        2.2 Compare cumulative social welfare impacts across modes
        """
        print("\n" + "="*80)
        print("OBJECTIVE 2: MODELING SOCIAL WELFARE OUTCOMES")
        print("="*80)
        
        results = {}
        
        # 2.1 Welfare Optimization Models
        print("\n2.1 Quantifying Welfare Outcomes Under Different Scenarios...")
        welfare_results = {}
        
        for mode in self.transport_modes:
            mode_data = [row for row in self.sp_data if row['Mode_Used'] == mode]
            if not mode_data:
                continue
                
            print(f"\nAnalyzing {mode} welfare optimization...")
            
            # Calculate base parameters
            base_demand = len(mode_data)
            base_price = np.mean([row['Fare_Paid'] for row in mode_data])
            base_cost = base_price * 0.6  # Assume 60% of fare is cost
            
            # Run different optimization models
            optimization_results = self._run_welfare_optimization_models(
                mode, base_demand, base_price, base_cost
            )
            
            welfare_results[mode] = optimization_results
            
            print(f"✓ {mode} welfare analysis:")
            print(f"  Optimal social welfare price: {optimization_results['max_s']['optimal_price']:.2f} BDT")
            print(f"  Social welfare: {optimization_results['max_s']['social_welfare']:.2f}")
        
        results['welfare_optimization'] = welfare_results
        
        # 2.2 Multi-Criteria Decision Analysis
        print("\n2.2 Comparing Cumulative Social Welfare Impacts Across Modes...")
        print("Performing Multi-Criteria Decision Analysis...")
        
        mcda_results = self._perform_enhanced_mcda(welfare_results)
        results['mcda_analysis'] = mcda_results
        
        for mode in self.transport_modes:
            if mode in mcda_results:
                print(f"✓ {mode} MCDA score: {mcda_results[mode]['weighted_score']:.3f}")
        
        self.results['objective_2'] = results
        return results

    def _run_welfare_optimization_models(self, mode, base_demand, base_price, base_cost):
        """Run different welfare optimization models"""
        
        # Price elasticity (simplified)
        price_elasticity = -0.5  # Demand decreases by 0.5% for 1% price increase
        
        # Demand function: Q = Q0 * (P/P0)^elasticity
        def demand_function(price):
            return base_demand * (price / base_price) ** price_elasticity
        
        # Revenue function: R = P * Q
        def revenue_function(price):
            return price * demand_function(price)
        
        # Cost function: C = cost_per_unit * Q
        def cost_function(price):
            return base_cost * demand_function(price)
        
        # Profit function: π = R - C
        def profit_function(price):
            return revenue_function(price) - cost_function(price)
        
        # Consumer surplus function (simplified)
        def consumer_surplus_function(price):
            demand = demand_function(price)
            # Simplified CS calculation
            return demand * (base_price - price) * 0.5
        
        # Social welfare function: SW = CS + π
        def social_welfare_function(price):
            return consumer_surplus_function(price) + profit_function(price)
        
        # Find optimal prices for different objectives
        price_range = np.linspace(base_price * 0.5, base_price * 2.0, 100)
        
        # Max Revenue
        revenues = [revenue_function(p) for p in price_range]
        max_r_price = price_range[np.argmax(revenues)]
        max_r_revenue = max(revenues)
        
        # Max Profit
        profits = [profit_function(p) for p in price_range]
        max_p_price = price_range[np.argmax(profits)]
        max_p_profit = max(profits)
        
        # Max Demand (min price)
        max_d_price = min(price_range)
        max_d_demand = demand_function(max_d_price)
        
        # Max Benefits (max consumer surplus)
        benefits = [consumer_surplus_function(p) for p in price_range]
        max_b_price = price_range[np.argmax(benefits)]
        max_b_benefits = max(benefits)
        
        # Max Social Welfare
        social_welfares = [social_welfare_function(p) for p in price_range]
        max_s_price = price_range[np.argmax(social_welfares)]
        max_s_welfare = max(social_welfares)
        
        return {
            'max_r': {
                'optimal_price': max_r_price,
                'revenue': max_r_revenue,
                'demand': demand_function(max_r_price),
                'profit': profit_function(max_r_price),
                'social_welfare': social_welfare_function(max_r_price)
            },
            'max_p': {
                'optimal_price': max_p_price,
                'revenue': revenue_function(max_p_price),
                'demand': demand_function(max_p_price),
                'profit': max_p_profit,
                'social_welfare': social_welfare_function(max_p_price)
            },
            'max_d': {
                'optimal_price': max_d_price,
                'revenue': revenue_function(max_d_price),
                'demand': max_d_demand,
                'profit': profit_function(max_d_price),
                'social_welfare': social_welfare_function(max_d_price)
            },
            'max_b': {
                'optimal_price': max_b_price,
                'revenue': revenue_function(max_b_price),
                'demand': demand_function(max_b_price),
                'profit': profit_function(max_b_price),
                'social_welfare': social_welfare_function(max_b_price)
            },
            'max_s': {
                'optimal_price': max_s_price,
                'revenue': revenue_function(max_s_price),
                'demand': demand_function(max_s_price),
                'profit': profit_function(max_s_price),
                'social_welfare': max_s_welfare
            }
        }

    def _perform_enhanced_mcda(self, welfare_results):
        """Perform enhanced Multi-Criteria Decision Analysis"""
        
        # Define criteria and weights
        criteria = {
            'social_welfare': 0.35,
            'accessibility': 0.25,
            'environmental_impact': 0.20,
            'cost_effectiveness': 0.15,
            'equity': 0.05
        }
        
        mcda_results = {}
        
        for mode in self.transport_modes:
            if mode not in welfare_results:
                continue
                
            # Get mode data for scoring
            mode_data = [row for row in self.sp_data if row['Mode_Used'] == mode]
            
            # Calculate scores for each criterion
            scores = {}
            
            # Social welfare score (normalized)
            max_welfare = max(welfare_results[m]['max_s']['social_welfare'] 
                            for m in welfare_results.keys())
            scores['social_welfare'] = welfare_results[mode]['max_s']['social_welfare'] / max_welfare
            
            # Accessibility score (based on demand and coverage)
            total_demand = len(mode_data)
            max_demand = max(len([row for row in self.sp_data if row['Mode_Used'] == m]) 
                           for m in self.transport_modes)
            scores['accessibility'] = total_demand / max_demand
            
            # Environmental impact score (inverse of emissions)
            avg_emissions = np.mean([row['carbon_emissions'] for row in mode_data])
            max_emissions = max(np.mean([row['carbon_emissions'] for row in self.sp_data 
                                       if row['Mode_Used'] == m]) for m in self.transport_modes)
            scores['environmental_impact'] = 1 - (avg_emissions / max_emissions)
            
            # Cost effectiveness score
            avg_cost = np.mean([row['Fare_Paid'] for row in mode_data])
            min_cost = min(np.mean([row['Fare_Paid'] for row in self.sp_data 
                                  if row['Mode_Used'] == m]) for m in self.transport_modes)
            max_cost = max(np.mean([row['Fare_Paid'] for row in self.sp_data 
                                  if row['Mode_Used'] == m]) for m in self.transport_modes)
            scores['cost_effectiveness'] = 1 - ((avg_cost - min_cost) / (max_cost - min_cost))
            
            # Equity score (based on income distribution)
            income_distribution = [row['Income_Bracket'] for row in mode_data]
            low_income_share = income_distribution.count('Low') / len(income_distribution)
            scores['equity'] = low_income_share
            
            # Calculate weighted score
            weighted_score = sum(scores[criterion] * weight 
                               for criterion, weight in criteria.items())
            
            mcda_results[mode] = {
                'individual_scores': scores,
                'weighted_score': weighted_score,
                'criteria_weights': criteria
            }
        
        return mcda_results

    def objective_3_analyze_travel_time_and_key_factors(self):
        """
        Objective 3: Examining the Role of Travel Time and Other Key Factors
        3.1 Identify the role of travel time, waiting time, and transfer inconvenience
        3.2 Evaluate equity-sensitive fare/subsidy policies and their distributional impact
        """
        print("\n" + "="*80)
        print("OBJECTIVE 3: ANALYZING TRAVEL TIME AND KEY FACTORS")
        print("="*80)
        
        results = {}
        
        # 3.1 Value of Time Analysis
        print("\n3.1 Analyzing Travel Time and Transfer Factors...")
        vot_results = {}
        
        for income_group in self.income_groups:
            group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
            
            # Calculate value of time
            time_values = [row['time_value'] for row in group_data]
            mean_vot = np.mean(time_values)
            
            vot_results[income_group] = {
                'mean_vot': mean_vot,
                'vot_per_hour': mean_vot * 60,  # Convert to per hour
                'median_vot': np.median(time_values),
                'min_vot': min(time_values),
                'max_vot': max(time_values)
            }
            
            print(f"✓ {income_group} income group VOT analysis:")
            print(f"  Mean VOT: {mean_vot:.2f} per minute")
            print(f"  VOT per hour: {vot_results[income_group]['vot_per_hour']:.2f} BDT/hour")
        
        results['vot_analysis'] = vot_results
        
        # 3.2 Generalized Cost Analysis
        print("\n3.2 Generalized Cost Analysis...")
        gc_results = {}
        
        for mode in self.transport_modes:
            mode_data = [row for row in self.sp_data if row['Mode_Used'] == mode]
            if not mode_data:
                continue
                
            gc_values = [row['generalized_cost'] for row in mode_data]
            
            gc_results[mode] = {
                'mean_gc': np.mean(gc_values),
                'min_gc': min(gc_values),
                'max_gc': max(gc_values),
                'std_gc': np.std(gc_values),
                'median_gc': np.median(gc_values)
            }
            
            print(f"✓ {mode} generalized cost:")
            print(f"  Mean GC: {gc_results[mode]['mean_gc']:.2f} BDT")
        
        results['generalized_cost_analysis'] = gc_results
        
        # 3.3 Policy Evaluation
        print("\n3.3 Evaluating Equity-Sensitive Fare/Subsidy Policies...")
        print("Evaluating equity-sensitive policies...")
        
        policy_results = self._evaluate_equity_policies()
        results['policy_analysis'] = policy_results
        
        for policy_name, policy_data in policy_results.items():
            print(f"✓ {policy_name} policy:")
            print(f"  Total subsidy cost: {policy_data['total_subsidy_cost']:.2f}")
            print(f"  Accessibility improvement: {policy_data['accessibility_improvement']} trips")
            print(f"  Cost effectiveness: {policy_data['cost_effectiveness']:.3f}")
        
        self.results['objective_3'] = results
        return results

    def _evaluate_equity_policies(self):
        """Evaluate different equity-sensitive fare policies"""
        
        policies = {
            'current': {'low_income_subsidy': 0.0, 'mid_income_subsidy': 0.0, 'high_income_subsidy': 0.0},
            'progressive_subsidy': {'low_income_subsidy': 0.4, 'mid_income_subsidy': 0.2, 'high_income_subsidy': 0.0},
            'universal_subsidy': {'low_income_subsidy': 0.2, 'mid_income_subsidy': 0.2, 'high_income_subsidy': 0.2},
            'targeted_subsidy': {'low_income_subsidy': 0.5, 'mid_income_subsidy': 0.1, 'high_income_subsidy': 0.0},
            'environmental_subsidy': {'low_income_subsidy': 0.3, 'mid_income_subsidy': 0.15, 'high_income_subsidy': 0.05}
        }
        
        policy_results = {}
        
        for policy_name, subsidy_rates in policies.items():
            total_subsidy_cost = 0
            accessibility_improvement = 0
            
            for income_group in self.income_groups:
                group_data = [row for row in self.sp_data if row['Income_Bracket'] == income_group]
                subsidy_rate = subsidy_rates[f'{income_group.lower()}_income_subsidy']
                
                for row in group_data:
                    if row['affordability_ratio'] > 1.0:  # Currently unaffordable
                        subsidy_amount = row['Fare_Paid'] * subsidy_rate
                        total_subsidy_cost += subsidy_amount
                        
                        # Check if subsidy makes trip affordable
                        new_affordability_ratio = (row['Fare_Paid'] - subsidy_amount) / row['WTP']
                        if new_affordability_ratio <= 1.0:
                            accessibility_improvement += 1
            
            cost_effectiveness = (accessibility_improvement / total_subsidy_cost 
                                if total_subsidy_cost > 0 else 0)
            
            policy_results[policy_name] = {
                'total_subsidy_cost': total_subsidy_cost,
                'accessibility_improvement': accessibility_improvement,
                'cost_effectiveness': cost_effectiveness,
                'subsidy_rates': subsidy_rates
            }
        
        return policy_results

    def generate_enhanced_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("GENERATING ENHANCED ANALYSIS REPORT")
        print("="*80)
        
        report = []
        report.append("# Dhaka Public Transport Fare System Optimization - Enhanced Analysis Report")
        report.append("")
        report.append("## Executive Summary")
        report.append("")
        report.append("This comprehensive analysis addresses all three main objectives of the thesis:")
        report.append("1. **User Preferences and Affordability Analysis** - Discrete choice modeling and CVM")
        report.append("2. **Social Welfare Optimization** - Five optimization models with MCDA")
        report.append("3. **Travel Time and Equity Analysis** - VOT analysis and policy evaluation")
        report.append("")
        
        # Objective 1 Results
        if 'objective_1' in self.results:
            obj1 = self.results['objective_1']
            report.append("## Objective 1: User Preferences and Affordability Analysis")
            report.append("")
            
            # Mode Choice Analysis
            report.append("### 1.1 Mode Choice Analysis by Income Groups")
            report.append("")
            for income_group in self.income_groups:
                if income_group in obj1['mode_choice_analysis']:
                    data = obj1['mode_choice_analysis'][income_group]
                    report.append(f"**{income_group} Income Group:**")
                    report.append(f"- Total respondents: {data['total_respondents']}")
                    for mode, percentage in data['mode_percentages'].items():
                        report.append(f"- {mode}: {percentage:.1f}%")
                    report.append("")
            
            # WTP Analysis
            report.append("### 1.2 Willingness to Pay and Affordability Analysis")
            report.append("")
            for income_group in self.income_groups:
                if income_group in obj1['wtp_analysis']:
                    data = obj1['wtp_analysis'][income_group]
                    report.append(f"**{income_group} Income Group:**")
                    report.append(f"- Mean WTP: {data['mean_wtp']:.2f} BDT")
                    report.append(f"- Unaffordable trips: {data['unaffordable_percentage']:.1f}%")
                    report.append(f"- Fare elasticity: {data['fare_elasticity']:.3f}")
                    report.append("")
            
            # CVM Analysis
            report.append("### 1.3 Contingent Valuation Method Analysis")
            report.append("")
            for income_group in self.income_groups:
                if income_group in obj1['cvm_analysis']:
                    data = obj1['cvm_analysis'][income_group]
                    report.append(f"**{income_group} Income Group:**")
                    report.append(f"- WTP for fare improvement: {data['wtp_fare_improvement']:.2f} BDT")
                    report.append(f"- WTP for comfort improvement: {data['wtp_comfort_improvement']:.2f} BDT")
                    report.append(f"- Fare improvement acceptance: {data['fare_improvement_acceptance_rate']:.1%}")
                    report.append("")
        
        # Objective 2 Results
        if 'objective_2' in self.results:
            obj2 = self.results['objective_2']
            report.append("## Objective 2: Social Welfare Optimization")
            report.append("")
            
            # Welfare Optimization
            report.append("### 2.1 Welfare Optimization Results")
            report.append("")
            for mode in self.transport_modes:
                if mode in obj2['welfare_optimization']:
                    data = obj2['welfare_optimization'][mode]['max_s']
                    report.append(f"**{mode}:**")
                    report.append(f"- Optimal social welfare price: {data['optimal_price']:.2f} BDT")
                    report.append(f"- Social welfare: {data['social_welfare']:.2f}")
                    report.append(f"- Demand: {data['demand']:.0f}")
                    report.append("")
            
            # MCDA Results
            report.append("### 2.2 Multi-Criteria Decision Analysis")
            report.append("")
            for mode in self.transport_modes:
                if mode in obj2['mcda_analysis']:
                    data = obj2['mcda_analysis'][mode]
                    report.append(f"**{mode}:** MCDA Score = {data['weighted_score']:.3f}")
                    report.append("")
        
        # Objective 3 Results
        if 'objective_3' in self.results:
            obj3 = self.results['objective_3']
            report.append("## Objective 3: Travel Time and Equity Analysis")
            report.append("")
            
            # VOT Analysis
            report.append("### 3.1 Value of Time Analysis")
            report.append("")
            for income_group in self.income_groups:
                if income_group in obj3['vot_analysis']:
                    data = obj3['vot_analysis'][income_group]
                    report.append(f"**{income_group} Income Group:**")
                    report.append(f"- Value of Time: {data['vot_per_hour']:.2f} BDT/hour")
                    report.append("")
            
            # Policy Analysis
            report.append("### 3.2 Policy Evaluation Results")
            report.append("")
            for policy_name, data in obj3['policy_analysis'].items():
                report.append(f"**{policy_name.replace('_', ' ').title()}:**")
                report.append(f"- Total subsidy cost: {data['total_subsidy_cost']:.2f} BDT")
                report.append(f"- Accessibility improvement: {data['accessibility_improvement']} trips")
                report.append(f"- Cost effectiveness: {data['cost_effectiveness']:.3f}")
                report.append("")
        
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
        report.append("")
        
        report.append("### 4. Environmental Considerations")
        report.append("- Integrate carbon pricing into fare structure")
        report.append("- Promote low-emission transport modes")
        report.append("- Consider environmental subsidies")
        report.append("")
        
        # Write report to file
        with open('enhanced_thesis_report.md', 'w') as f:
            f.write('\n'.join(report))
        
        print("✓ Enhanced report generated: enhanced_thesis_report.md")
        return '\n'.join(report)

    def generate_enhanced_json_results(self):
        """Generate comprehensive JSON results"""
        print("Generating enhanced JSON results...")
        
        # Add metadata
        enhanced_results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_observations': len(self.sp_data),
                'income_groups': self.income_groups,
                'transport_modes': self.transport_modes,
                'analysis_version': 'enhanced_1.0'
            },
            'results': self.results
        }
        
        with open('enhanced_thesis_results.json', 'w') as f:
            json.dump(enhanced_results, f, indent=2)
        
        print("✓ Enhanced JSON results generated: enhanced_thesis_results.json")
        return enhanced_results

    def run_complete_enhanced_analysis(self):
        """Run the complete enhanced analysis"""
        print("="*80)
        print("RUNNING ENHANCED COMPREHENSIVE THESIS ANALYSIS")
        print("="*80)
        
        # Load data
        self.load_data()
        
        print("\nRunning all analysis objectives...")
        
        # Run all objectives
        self.objective_1_analyze_user_preferences_and_affordability()
        self.objective_2_model_social_welfare_outcomes()
        self.objective_3_analyze_travel_time_and_key_factors()
        
        # Generate outputs
        print("\nGenerating analysis outputs...")
        self.generate_enhanced_report()
        self.generate_enhanced_json_results()
        
        print("\n" + "="*80)
        print("ENHANCED ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\nGenerated Files:")
        print("- enhanced_thesis_report.md (Comprehensive analysis report)")
        print("- enhanced_thesis_results.json (Structured results)")
        print("\nKey Results Summary:")
        print(f"- Analyzed {len(self.sp_data)} transport trips")
        print(f"- Evaluated {len(self.transport_modes)} transport modes")
        print(f"- Assessed {len(self.income_groups)} income groups")
        print("\nAnalysis completed! Check the generated files for detailed results.")

if __name__ == "__main__":
    analyzer = EnhancedThesisAnalyzer()
    analyzer.run_complete_enhanced_analysis()