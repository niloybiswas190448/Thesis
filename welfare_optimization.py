"""
Welfare Optimization Models for Transport Fare System
===================================================

This module implements various welfare optimization models including Max-R, Max-P,
Max-B, Max-D, and Max-S models for optimizing transport fare systems in Dhaka.

Author: [Your Name]
Date: [Current Date]
"""

import numpy as np
import pandas as pd
import cvxpy as cp
from scipy.optimize import minimize, differential_evolution
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class WelfareOptimizer:
    """
    Welfare optimization for transport fare systems
    """
    
    def __init__(self):
        self.optimization_results = {}
        self.constraints = {}
        self.objective_functions = {}
        
    def define_demand_function(self, base_demand, price_elasticity, base_price):
        """
        Define demand function based on price elasticity
        
        Parameters:
        -----------
        base_demand : float
            Base demand at current price
        price_elasticity : float
            Price elasticity of demand
        base_price : float
            Current base price
            
        Returns:
        --------
        function
            Demand function
        """
        def demand_function(price):
            return base_demand * (price / base_price) ** price_elasticity
        
        return demand_function
    
    def max_revenue_model(self, demand_func, cost_func, price_range=(0, 200)):
        """
        Maximize Revenue (Max-R) model
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
            
        Returns:
        --------
        dict
            Optimization results
        """
        print("Solving Max-R (Revenue Maximization) model...")
        
        def objective(price):
            demand = demand_func(price)
            revenue = price * demand
            return -revenue  # Negative for minimization
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        optimal_revenue = optimal_price * optimal_demand
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_revenue': optimal_revenue,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def max_profit_model(self, demand_func, cost_func, price_range=(0, 200)):
        """
        Maximize Profit (Max-P) model
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
            
        Returns:
        --------
        dict
            Optimization results
        """
        print("Solving Max-P (Profit Maximization) model...")
        
        def objective(price):
            demand = demand_func(price)
            revenue = price * demand
            cost = cost_func(demand)
            profit = revenue - cost
            return -profit  # Negative for minimization
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        optimal_revenue = optimal_price * optimal_demand
        optimal_cost = cost_func(optimal_demand)
        optimal_profit = optimal_revenue - optimal_cost
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_revenue': optimal_revenue,
            'optimal_cost': optimal_cost,
            'optimal_profit': optimal_profit,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def max_benefit_model(self, demand_func, cost_func, price_range=(0, 200),
                         consumer_surplus_weight=1.0):
        """
        Maximize User Benefits (Max-B) model
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
        consumer_surplus_weight : float
            Weight for consumer surplus in objective function
            
        Returns:
        --------
        dict
            Optimization results
        """
        print("Solving Max-B (User Benefit Maximization) model...")
        
        def objective(price):
            demand = demand_func(price)
            
            # Calculate consumer surplus (simplified)
            # In practice, this would require integration of demand function
            base_price = price_range[1]  # Assume base price is max price
            consumer_surplus = 0.5 * (base_price - price) * demand
            
            return -consumer_surplus_weight * consumer_surplus
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        base_price = price_range[1]
        optimal_consumer_surplus = 0.5 * (base_price - optimal_price) * optimal_demand
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_consumer_surplus': optimal_consumer_surplus,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def max_demand_model(self, demand_func, cost_func, price_range=(0, 200),
                        budget_constraint=None):
        """
        Maximize Demand (Max-D) model
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
        budget_constraint : float
            Maximum budget constraint
            
        Returns:
        --------
        dict
            Optimization results
        """
        print("Solving Max-D (Demand Maximization) model...")
        
        def objective(price):
            demand = demand_func(price)
            return -demand  # Negative for minimization
        
        # Define constraints
        constraints = []
        if budget_constraint is not None:
            def budget_constraint_func(price):
                demand = demand_func(price)
                cost = cost_func(demand)
                return budget_constraint - cost
            
            constraints.append({'type': 'ineq', 'fun': budget_constraint_func})
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            constraints=constraints,
            method='SLSQP'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        optimal_cost = cost_func(optimal_demand)
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_cost': optimal_cost,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def max_social_welfare_model(self, demand_func, cost_func, price_range=(0, 200),
                               equity_weight=0.3, environmental_weight=0.2):
        """
        Maximize Social Welfare (Max-S) model
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
        equity_weight : float
            Weight for equity considerations
        environmental_weight : float
            Weight for environmental considerations
            
        Returns:
        --------
        dict
            Optimization results
        """
        print("Solving Max-S (Social Welfare Maximization) model...")
        
        def objective(price):
            demand = demand_func(price)
            revenue = price * demand
            cost = cost_func(demand)
            
            # Consumer surplus
            base_price = price_range[1]
            consumer_surplus = 0.5 * (base_price - price) * demand
            
            # Producer surplus (profit)
            producer_surplus = revenue - cost
            
            # Equity component (simplified - lower prices benefit low-income users)
            equity_component = -price * equity_weight
            
            # Environmental component (simplified - higher demand may have environmental costs)
            environmental_component = -demand * environmental_weight
            
            # Total social welfare
            social_welfare = (consumer_surplus + producer_surplus + 
                            equity_component + environmental_component)
            
            return -social_welfare  # Negative for minimization
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        optimal_revenue = optimal_price * optimal_demand
        optimal_cost = cost_func(optimal_demand)
        
        # Calculate components
        base_price = price_range[1]
        consumer_surplus = 0.5 * (base_price - optimal_price) * optimal_demand
        producer_surplus = optimal_revenue - optimal_cost
        equity_component = -optimal_price * equity_weight
        environmental_component = -optimal_demand * environmental_weight
        
        total_welfare = (consumer_surplus + producer_surplus + 
                        equity_component + environmental_component)
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_revenue': optimal_revenue,
            'optimal_cost': optimal_cost,
            'consumer_surplus': consumer_surplus,
            'producer_surplus': producer_surplus,
            'equity_component': equity_component,
            'environmental_component': environmental_component,
            'total_welfare': total_welfare,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def multi_objective_optimization(self, demand_func, cost_func, price_range=(0, 200),
                                   weights={'revenue': 0.2, 'profit': 0.2, 'benefit': 0.2,
                                           'demand': 0.2, 'welfare': 0.2}):
        """
        Multi-objective optimization combining all objectives
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
        weights : dict
            Weights for different objectives
            
        Returns:
        --------
        dict
            Multi-objective optimization results
        """
        print("Solving Multi-Objective Optimization model...")
        
        def objective(price):
            demand = demand_func(price)
            revenue = price * demand
            cost = cost_func(demand)
            profit = revenue - cost
            
            # Consumer surplus
            base_price = price_range[1]
            consumer_surplus = 0.5 * (base_price - price) * demand
            
            # Social welfare components
            equity_component = -price * 0.3
            environmental_component = -demand * 0.2
            social_welfare = (consumer_surplus + profit + equity_component + environmental_component)
            
            # Weighted objective
            weighted_objective = (
                weights['revenue'] * revenue +
                weights['profit'] * profit +
                weights['benefit'] * consumer_surplus +
                weights['demand'] * demand +
                weights['welfare'] * social_welfare
            )
            
            return -weighted_objective  # Negative for minimization
        
        # Optimize
        result = minimize(
            objective,
            x0=np.mean(price_range),
            bounds=[price_range],
            method='L-BFGS-B'
        )
        
        optimal_price = result.x[0]
        optimal_demand = demand_func(optimal_price)
        optimal_revenue = optimal_price * optimal_demand
        optimal_cost = cost_func(optimal_demand)
        optimal_profit = optimal_revenue - optimal_cost
        
        return {
            'optimal_price': optimal_price,
            'optimal_demand': optimal_demand,
            'optimal_revenue': optimal_revenue,
            'optimal_cost': optimal_cost,
            'optimal_profit': optimal_profit,
            'weights_used': weights,
            'success': result.success,
            'objective_value': -result.fun
        }
    
    def sensitivity_analysis(self, demand_func, cost_func, price_range=(0, 200),
                           parameter_ranges=None):
        """
        Perform sensitivity analysis on optimization results
        
        Parameters:
        -----------
        demand_func : function
            Demand function
        cost_func : function
            Cost function
        price_range : tuple
            Range of feasible prices
        parameter_ranges : dict
            Ranges for sensitivity analysis parameters
            
        Returns:
        --------
        dict
            Sensitivity analysis results
        """
        print("Performing Sensitivity Analysis...")
        
        if parameter_ranges is None:
            parameter_ranges = {
                'price_elasticity': np.linspace(-2.0, -0.5, 10),
                'base_demand': np.linspace(50, 200, 10),
                'cost_multiplier': np.linspace(0.5, 2.0, 10)
            }
        
        sensitivity_results = {}
        
        # Price elasticity sensitivity
        if 'price_elasticity' in parameter_ranges:
            elasticity_results = []
            for elasticity in parameter_ranges['price_elasticity']:
                # Modify demand function for this elasticity
                def modified_demand(price):
                    return demand_func(price) * (price / 50) ** (elasticity + 1)
                
                result = self.max_social_welfare_model(modified_demand, cost_func, price_range)
                elasticity_results.append({
                    'elasticity': elasticity,
                    'optimal_price': result['optimal_price'],
                    'optimal_demand': result['optimal_demand'],
                    'total_welfare': result['total_welfare']
                })
            sensitivity_results['price_elasticity'] = elasticity_results
        
        # Base demand sensitivity
        if 'base_demand' in parameter_ranges:
            demand_results = []
            for base_demand in parameter_ranges['base_demand']:
                # Modify demand function for this base demand
                def modified_demand(price):
                    return demand_func(price) * (base_demand / 100)
                
                result = self.max_social_welfare_model(modified_demand, cost_func, price_range)
                demand_results.append({
                    'base_demand': base_demand,
                    'optimal_price': result['optimal_price'],
                    'optimal_demand': result['optimal_demand'],
                    'total_welfare': result['total_welfare']
                })
            sensitivity_results['base_demand'] = demand_results
        
        return sensitivity_results
    
    def optimize_by_income_group(self, sp_data, secondary_data):
        """
        Optimize fares separately for different income groups
        
        Parameters:
        -----------
        sp_data : pandas.DataFrame
            Stated preference data
        secondary_data : pandas.DataFrame
            Secondary data with cost information
            
        Returns:
        --------
        dict
            Income group-specific optimization results
        """
        print("Optimizing fares by income group...")
        
        income_group_results = {}
        income_groups = sp_data['income_group'].unique()
        
        for income_group in income_groups:
            print(f"Optimizing for {income_group} income group...")
            
            # Filter data for income group
            group_data = sp_data[sp_data['income_group'] == income_group]
            
            # Calculate group-specific parameters
            avg_income = group_data['income'].mean()
            avg_fare = group_data['fare'].mean()
            avg_demand = group_data['chosen'].mean()
            
            # Estimate price elasticity for this group
            fare_changes = group_data['fare'].pct_change()
            demand_changes = group_data['chosen'].pct_change()
            
            valid_mask = (fare_changes != np.inf) & (fare_changes != -np.inf) & \
                        (demand_changes != np.inf) & (demand_changes != -np.inf) & \
                        (fare_changes != 0)
            
            if valid_mask.sum() > 10:
                elasticity = np.corrcoef(fare_changes[valid_mask], demand_changes[valid_mask])[0, 1]
            else:
                elasticity = -1.0  # Default elasticity
            
            # Define demand and cost functions for this group
            def group_demand_func(price):
                return avg_demand * (price / avg_fare) ** elasticity
            
            def group_cost_func(demand):
                # Assume linear cost function
                return demand * 10  # Simplified cost per unit
            
            # Run optimization models
            group_results = {}
            
            # Max-R
            group_results['max_revenue'] = self.max_revenue_model(
                group_demand_func, group_cost_func
            )
            
            # Max-P
            group_results['max_profit'] = self.max_profit_model(
                group_demand_func, group_cost_func
            )
            
            # Max-B
            group_results['max_benefit'] = self.max_benefit_model(
                group_demand_func, group_cost_func
            )
            
            # Max-D
            group_results['max_demand'] = self.max_demand_model(
                group_demand_func, group_cost_func
            )
            
            # Max-S
            group_results['max_welfare'] = self.max_social_welfare_model(
                group_demand_func, group_cost_func
            )
            
            income_group_results[income_group] = {
                'parameters': {
                    'avg_income': avg_income,
                    'avg_fare': avg_fare,
                    'avg_demand': avg_demand,
                    'elasticity': elasticity
                },
                'optimization_results': group_results
            }
        
        return income_group_results
    
    def generate_optimization_report(self, results):
        """
        Generate comprehensive optimization report
        
        Parameters:
        -----------
        results : dict
            Optimization results
            
        Returns:
        --------
        str
            Report text
        """
        report = []
        report.append("# Welfare Optimization Analysis Report\n")
        
        # Summary of results
        report.append("## Optimization Results Summary\n")
        
        for mode, mode_results in results.items():
            report.append(f"### {mode}\n")
            
            for objective, obj_results in mode_results.items():
                report.append(f"#### {objective}\n")
                report.append(f"- Optimal Price: {obj_results['optimal_price']:.1f} BDT\n")
                report.append(f"- Optimal Demand: {obj_results['optimal_demand']:.1f}\n")
                
                if 'optimal_revenue' in obj_results:
                    report.append(f"- Revenue: {obj_results['optimal_revenue']:.1f} BDT\n")
                
                if 'optimal_profit' in obj_results:
                    report.append(f"- Profit: {obj_results['optimal_profit']:.1f} BDT\n")
                
                if 'total_welfare' in obj_results:
                    report.append(f"- Total Welfare: {obj_results['total_welfare']:.1f} BDT\n")
                
                report.append("\n")
        
        # Policy recommendations
        report.append("## Policy Recommendations\n")
        report.append("Based on the optimization analysis:\n")
        report.append("1. **Implement differentiated pricing** based on optimization objectives\n")
        report.append("2. **Consider social welfare maximization** for overall system optimization\n")
        report.append("3. **Balance revenue and accessibility** objectives\n")
        report.append("4. **Monitor demand responses** to fare changes\n")
        report.append("5. **Evaluate equity impacts** across income groups\n")
        
        return "\n".join(report)
    
    def run_complete_optimization(self, sp_data, secondary_data):
        """
        Run complete welfare optimization analysis
        
        Parameters:
        -----------
        sp_data : pandas.DataFrame
            Stated preference data
        secondary_data : pandas.DataFrame
            Secondary data
            
        Returns:
        --------
        dict
            Complete optimization results
        """
        print("Running Complete Welfare Optimization Analysis...")
        print("=" * 60)
        
        # Mode-specific optimization
        mode_optimization = {}
        modes = sp_data['mode'].unique()
        
        for mode in modes:
            print(f"\nOptimizing for {mode}...")
            
            mode_data = sp_data[sp_data['mode'] == mode]
            secondary_mode_data = secondary_data[secondary_data['mode'] == mode].iloc[0]
            
            # Get mode-specific parameters
            avg_fare = mode_data['fare'].mean()
            avg_demand = mode_data['chosen'].mean()
            operator_cost = secondary_mode_data['operator_cost_per_km']
            
            # Define demand and cost functions
            def demand_func(price):
                return avg_demand * (1 - 0.5 * (price - avg_fare) / avg_fare)
            
            def cost_func(demand):
                return demand * operator_cost
            
            # Run all optimization models
            mode_results = {}
            mode_results['max_revenue'] = self.max_revenue_model(demand_func, cost_func)
            mode_results['max_profit'] = self.max_profit_model(demand_func, cost_func)
            mode_results['max_benefit'] = self.max_benefit_model(demand_func, cost_func)
            mode_results['max_demand'] = self.max_demand_model(demand_func, cost_func)
            mode_results['max_welfare'] = self.max_social_welfare_model(demand_func, cost_func)
            
            mode_optimization[mode] = mode_results
        
        # Income group optimization
        income_optimization = self.optimize_by_income_group(sp_data, secondary_data)
        
        # Multi-objective optimization
        multi_objective = {}
        for mode in modes:
            mode_data = sp_data[sp_data['mode'] == mode]
            avg_fare = mode_data['fare'].mean()
            avg_demand = mode_data['chosen'].mean()
            operator_cost = secondary_data[secondary_data['mode'] == mode]['operator_cost_per_km'].iloc[0]
            
            def demand_func(price):
                return avg_demand * (1 - 0.5 * (price - avg_fare) / avg_fare)
            
            def cost_func(demand):
                return demand * operator_cost
            
            multi_objective[mode] = self.multi_objective_optimization(demand_func, cost_func)
        
        # Sensitivity analysis
        sensitivity = {}
        for mode in modes:
            mode_data = sp_data[sp_data['mode'] == mode]
            avg_fare = mode_data['fare'].mean()
            avg_demand = mode_data['chosen'].mean()
            operator_cost = secondary_data[secondary_data['mode'] == mode]['operator_cost_per_km'].iloc[0]
            
            def demand_func(price):
                return avg_demand * (1 - 0.5 * (price - avg_fare) / avg_fare)
            
            def cost_func(demand):
                return demand * operator_cost
            
            sensitivity[mode] = self.sensitivity_analysis(demand_func, cost_func)
        
        # Generate report
        report = self.generate_optimization_report(mode_optimization)
        
        # Save results
        with open("welfare_optimization_report.md", "w") as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("Welfare Optimization Analysis Complete!")
        print("Report saved as 'welfare_optimization_report.md'")
        print("=" * 60)
        
        return {
            'mode_optimization': mode_optimization,
            'income_optimization': income_optimization,
            'multi_objective': multi_objective,
            'sensitivity': sensitivity,
            'report': report
        }


# Example usage
if __name__ == "__main__":
    # This module is designed to be imported and used with the main analysis
    print("Welfare Optimization Module")
    print("Import this module to use optimization techniques")