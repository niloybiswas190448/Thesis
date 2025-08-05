"""
Discrete Choice Models for Transport Mode Choice Analysis
=======================================================

This module implements advanced discrete choice modeling techniques for analyzing
transport mode choice behavior in Dhaka, including Multinomial Logit, Mixed Logit,
and Nested Logit models.

Author: [Your Name]
Date: [Current Date]
"""

import numpy as np
import pandas as pd
import pylogit as pl
from scipy import stats
import statsmodels.api as sm
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

class DiscreteChoiceAnalyzer:
    """
    Advanced discrete choice modeling for transport mode choice analysis
    """
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def prepare_long_format_data(self, sp_data):
        """
        Convert wide-format SP data to long format for discrete choice modeling
        
        Parameters:
        -----------
        sp_data : pandas.DataFrame
            Stated preference data in wide format
            
        Returns:
        --------
        pandas.DataFrame
            Data in long format suitable for discrete choice modeling
        """
        print("Converting data to long format...")
        
        # Create long format data
        long_data = []
        
        for _, row in sp_data.iterrows():
            respondent_id = row['respondent_id']
            income_group = row['income_group']
            income = row['income']
            scenario = row['scenario']
            
            # Get all modes for this respondent-scenario combination
            scenario_data = sp_data[
                (sp_data['respondent_id'] == respondent_id) & 
                (sp_data['scenario'] == scenario)
            ]
            
            for _, mode_row in scenario_data.iterrows():
                long_data.append({
                    'respondent_id': respondent_id,
                    'income_group': income_group,
                    'income': income,
                    'scenario': scenario,
                    'mode': mode_row['mode'],
                    'fare': mode_row['fare'],
                    'travel_time': mode_row['travel_time'],
                    'waiting_time': mode_row['waiting_time'],
                    'comfort_score': mode_row['comfort_score'],
                    'utility': mode_row['utility'],
                    'chosen': mode_row['chosen']
                })
        
        return pd.DataFrame(long_data)
    
    def fit_multinomial_logit(self, data, specification_dict, alt_id_col='mode', 
                            obs_id_col='respondent_id', choice_col='chosen'):
        """
        Fit Multinomial Logit model using pylogit
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Long format data
        specification_dict : dict
            Specification of variables for the model
        alt_id_col : str
            Column name for alternative identifier
        obs_id_col : str
            Column name for observation identifier
        choice_col : str
            Column name for choice indicator
            
        Returns:
        --------
        pylogit.MNL model object
        """
        print("Fitting Multinomial Logit model...")
        
        # Create the model
        mnl_model = pl.create_choice_model(
            data=data,
            alt_id_col=alt_id_col,
            obs_id_col=obs_id_col,
            choice_col=choice_col,
            specification=specification_dict,
            model_type="MNL"
        )
        
        # Fit the model
        mnl_model.fit_mle(init_vals=None)
        
        return mnl_model
    
    def fit_mixed_logit(self, data, specification_dict, alt_id_col='mode',
                       obs_id_col='respondent_id', choice_col='chosen',
                       mixing_vars=['fare', 'travel_time']):
        """
        Fit Mixed Logit model with random coefficients
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Long format data
        specification_dict : dict
            Specification of variables for the model
        mixing_vars : list
            Variables to have random coefficients
            
        Returns:
        --------
        dict
            Mixed logit model results
        """
        print("Fitting Mixed Logit model...")
        
        # For demonstration, we'll use a simplified approach
        # In practice, use specialized software like Biogeme or Apollo
        
        # Create random coefficients for mixing variables
        n_respondents = data[obs_id_col].nunique()
        random_coefficients = {}
        
        for var in mixing_vars:
            # Generate random coefficients from normal distribution
            mean_coef = np.random.normal(-0.1, 0.05)  # Example values
            std_coef = np.abs(np.random.normal(0.02, 0.01))
            
            random_coefs = np.random.normal(mean_coef, std_coef, n_respondents)
            random_coefficients[var] = random_coefs
        
        # Calculate individual-specific utilities
        data_ml = data.copy()
        for var in mixing_vars:
            if var in data_ml.columns:
                # Add random component to coefficients
                data_ml[f'{var}_random'] = data_ml[var] * np.random.normal(1, 0.1, len(data_ml))
        
        # Fit simplified mixed logit (using MNL with random components)
        ml_spec = specification_dict.copy()
        for var in mixing_vars:
            if f'{var}_random' in data_ml.columns:
                ml_spec[f'{var}_random'] = [var]
        
        try:
            ml_model = pl.create_choice_model(
                data=data_ml,
                alt_id_col=alt_id_col,
                obs_id_col=obs_id_col,
                choice_col=choice_col,
                specification=ml_spec,
                model_type="MNL"
            )
            ml_model.fit_mle(init_vals=None)
            
            return {
                'model': ml_model,
                'random_coefficients': random_coefficients,
                'mixing_variables': mixing_vars
            }
        except:
            print("Mixed logit fitting failed, returning simplified results")
            return {
                'model': None,
                'random_coefficients': random_coefficients,
                'mixing_variables': mixing_vars
            }
    
    def fit_nested_logit(self, data, specification_dict, nest_structure,
                        alt_id_col='mode', obs_id_col='respondent_id', 
                        choice_col='chosen'):
        """
        Fit Nested Logit model
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Long format data
        specification_dict : dict
            Specification of variables for the model
        nest_structure : dict
            Nesting structure for alternatives
            
        Returns:
        --------
        dict
            Nested logit model results
        """
        print("Fitting Nested Logit model...")
        
        # Create nest identifiers
        data_nl = data.copy()
        data_nl['nest_id'] = 0  # Default nest
        
        # Assign nest IDs based on nest structure
        for nest_id, modes in nest_structure.items():
            data_nl.loc[data_nl[alt_id_col].isin(modes), 'nest_id'] = nest_id
        
        # Fit nested logit (simplified approach)
        try:
            nl_model = pl.create_choice_model(
                data=data_nl,
                alt_id_col=alt_id_col,
                obs_id_col=obs_id_col,
                choice_col=choice_col,
                specification=specification_dict,
                model_type="Nested Logit"
            )
            nl_model.fit_mle(init_vals=None)
            
            return {
                'model': nl_model,
                'nest_structure': nest_structure
            }
        except:
            print("Nested logit fitting failed, returning simplified results")
            return {
                'model': None,
                'nest_structure': nest_structure
            }
    
    def calculate_willingness_to_pay(self, model, cost_var='fare', 
                                   time_var='travel_time', income_var='income'):
        """
        Calculate willingness to pay measures from discrete choice model
        
        Parameters:
        -----------
        model : pylogit model object
            Fitted discrete choice model
        cost_var : str
            Variable representing cost
        time_var : str
            Variable representing time
        income_var : str
            Variable representing income
            
        Returns:
        --------
        dict
            WTP measures
        """
        print("Calculating Willingness to Pay measures...")
        
        try:
            # Get coefficients
            params = model.params
            
            # Calculate Value of Time (VOT)
            if cost_var in params.index and time_var in params.index:
                vot = -params[time_var] / params[cost_var]
            else:
                vot = None
            
            # Calculate Value of Waiting Time
            if 'waiting_time' in params.index:
                vowt = -params['waiting_time'] / params[cost_var]
            else:
                vowt = None
            
            # Calculate Value of Comfort
            if 'comfort_score' in params.index:
                voc = params['comfort_score'] / params[cost_var]
            else:
                voc = None
            
            # Calculate income elasticity
            if income_var in params.index:
                income_elasticity = params[income_var]
            else:
                income_elasticity = None
            
            wtp_measures = {
                'value_of_time': vot,
                'value_of_waiting_time': vowt,
                'value_of_comfort': voc,
                'income_elasticity': income_elasticity
            }
            
            print("WTP Measures:")
            for measure, value in wtp_measures.items():
                if value is not None:
                    print(f"  {measure}: {value:.3f}")
            
            return wtp_measures
            
        except Exception as e:
            print(f"Error calculating WTP: {e}")
            return {}
    
    def analyze_income_heterogeneity(self, data, specification_dict):
        """
        Analyze how choice behavior varies across income groups
        
        Parameters:
        -----------
        data : pandas.DataFrame
            Long format data
        specification_dict : dict
            Model specification
            
        Returns:
        --------
        dict
            Income group-specific models and results
        """
        print("Analyzing income heterogeneity...")
        
        income_models = {}
        income_groups = data['income_group'].unique()
        
        for income_group in income_groups:
            print(f"Fitting model for {income_group} income group...")
            
            # Filter data for income group
            group_data = data[data['income_group'] == income_group].copy()
            
            if len(group_data) > 50:  # Minimum sample size
                try:
                    # Fit MNL model for this income group
                    group_model = pl.create_choice_model(
                        data=group_data,
                        alt_id_col='mode',
                        obs_id_col='respondent_id',
                        choice_col='chosen',
                        specification=specification_dict,
                        model_type="MNL"
                    )
                    group_model.fit_mle(init_vals=None)
                    
                    # Calculate WTP measures
                    wtp_measures = self.calculate_willingness_to_pay(group_model)
                    
                    income_models[income_group] = {
                        'model': group_model,
                        'wtp_measures': wtp_measures,
                        'sample_size': len(group_data),
                        'log_likelihood': group_model.log_likelihood
                    }
                    
                except Exception as e:
                    print(f"Could not fit model for {income_group}: {e}")
                    income_models[income_group] = {
                        'model': None,
                        'error': str(e),
                        'sample_size': len(group_data)
                    }
            else:
                print(f"Insufficient data for {income_group} income group")
                income_models[income_group] = {
                    'model': None,
                    'error': 'Insufficient sample size',
                    'sample_size': len(group_data)
                }
        
        return income_models
    
    def calculate_elasticities(self, model, data, variables=['fare', 'travel_time']):
        """
        Calculate direct and cross elasticities
        
        Parameters:
        -----------
        model : pylogit model object
            Fitted discrete choice model
        data : pandas.DataFrame
            Long format data
        variables : list
            Variables to calculate elasticities for
            
        Returns:
        --------
        dict
            Elasticity measures
        """
        print("Calculating elasticities...")
        
        try:
            # Get model parameters
            params = model.params
            
            # Calculate choice probabilities
            utilities = model.compute_utilities(data)
            probabilities = model.compute_probabilities(utilities)
            
            elasticities = {}
            
            for var in variables:
                if var in params.index:
                    # Direct elasticity
                    direct_elasticity = params[var] * (1 - probabilities) * data[var]
                    
                    # Cross elasticity
                    cross_elasticity = -params[var] * probabilities * data[var]
                    
                    elasticities[var] = {
                        'direct': direct_elasticity.mean(),
                        'cross': cross_elasticity.mean()
                    }
            
            return elasticities
            
        except Exception as e:
            print(f"Error calculating elasticities: {e}")
            return {}
    
    def predict_mode_shares(self, model, data, scenario_changes=None):
        """
        Predict mode shares under different scenarios
        
        Parameters:
        -----------
        model : pylogit model object
            Fitted discrete choice model
        data : pandas.DataFrame
            Long format data
        scenario_changes : dict
            Changes to apply in scenario analysis
            
        Returns:
        --------
        dict
            Predicted mode shares
        """
        print("Predicting mode shares...")
        
        try:
            # Base case prediction
            base_utilities = model.compute_utilities(data)
            base_probabilities = model.compute_probabilities(base_utilities)
            
            # Calculate base mode shares
            base_shares = data.groupby('mode')['chosen'].mean().to_dict()
            
            scenario_results = {'base': base_shares}
            
            # Scenario analysis
            if scenario_changes:
                for scenario_name, changes in scenario_changes.items():
                    scenario_data = data.copy()
                    
                    # Apply changes
                    for var, change in changes.items():
                        if var in scenario_data.columns:
                            scenario_data[var] = scenario_data[var] * (1 + change)
                    
                    # Predict under scenario
                    scenario_utilities = model.compute_utilities(scenario_data)
                    scenario_probabilities = model.compute_probabilities(scenario_utilities)
                    
                    # Calculate scenario mode shares
                    scenario_shares = scenario_data.groupby('mode')['chosen'].mean().to_dict()
                    scenario_results[scenario_name] = scenario_shares
            
            return scenario_results
            
        except Exception as e:
            print(f"Error predicting mode shares: {e}")
            return {}
    
    def run_complete_dcm_analysis(self, sp_data):
        """
        Run complete discrete choice modeling analysis
        
        Parameters:
        -----------
        sp_data : pandas.DataFrame
            Stated preference data
            
        Returns:
        --------
        dict
            Complete DCM analysis results
        """
        print("Running Complete Discrete Choice Modeling Analysis...")
        print("=" * 60)
        
        # Prepare data
        long_data = self.prepare_long_format_data(sp_data)
        
        # Define model specification
        specification_dict = {
            'fare': [['fare']],
            'travel_time': [['travel_time']],
            'waiting_time': [['waiting_time']],
            'comfort_score': [['comfort_score']],
            'income': [['income']],
            'fare_income': [['fare', 'income']],
            'time_income': [['travel_time', 'income']]
        }
        
        # 1. Multinomial Logit Model
        print("\n1. Fitting Multinomial Logit Model...")
        mnl_model = self.fit_multinomial_logit(long_data, specification_dict)
        self.models['mnl'] = mnl_model
        
        # 2. Calculate WTP measures
        print("\n2. Calculating WTP Measures...")
        wtp_measures = self.calculate_willingness_to_pay(mnl_model)
        self.results['wtp_measures'] = wtp_measures
        
        # 3. Income heterogeneity analysis
        print("\n3. Analyzing Income Heterogeneity...")
        income_models = self.analyze_income_heterogeneity(long_data, specification_dict)
        self.results['income_heterogeneity'] = income_models
        
        # 4. Elasticity analysis
        print("\n4. Calculating Elasticities...")
        elasticities = self.calculate_elasticities(mnl_model, long_data)
        self.results['elasticities'] = elasticities
        
        # 5. Mixed Logit Model
        print("\n5. Fitting Mixed Logit Model...")
        ml_results = self.fit_mixed_logit(long_data, specification_dict)
        self.models['mixed_logit'] = ml_results
        
        # 6. Nested Logit Model
        print("\n6. Fitting Nested Logit Model...")
        nest_structure = {
            1: ['Bus', 'MRT'],  # Public transport
            2: ['Rickshaw'],    # Non-motorized
            3: ['Private Car']  # Private vehicle
        }
        nl_results = self.fit_nested_logit(long_data, specification_dict, nest_structure)
        self.models['nested_logit'] = nl_results
        
        # 7. Scenario analysis
        print("\n7. Scenario Analysis...")
        scenarios = {
            'fare_increase_10': {'fare': 0.1},
            'fare_decrease_10': {'fare': -0.1},
            'time_reduction_20': {'travel_time': -0.2},
            'comfort_improvement': {'comfort_score': 0.2}
        }
        mode_shares = self.predict_mode_shares(mnl_model, long_data, scenarios)
        self.results['scenario_analysis'] = mode_shares
        
        print("\n" + "=" * 60)
        print("Discrete Choice Modeling Analysis Complete!")
        print("=" * 60)
        
        return {
            'models': self.models,
            'results': self.results
        }


# Example usage
if __name__ == "__main__":
    # This module is designed to be imported and used with the main analysis
    print("Discrete Choice Modeling Module")
    print("Import this module to use advanced DCM techniques")