#!/usr/bin/env python3
"""
Example Usage of Dhaka Transport Fare Analysis Framework
=======================================================

This script demonstrates how to use the transport fare analysis framework
for optimizing Dhaka's public transport system.

Author: [Your Name]
Date: [Current Date]
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transport_fare_analysis import TransportFareAnalyzer
from discrete_choice_models import DiscreteChoiceAnalyzer
from welfare_optimization import WelfareOptimizer

def main():
    """
    Main function demonstrating the complete analysis workflow
    """
    print("Dhaka Transport Fare System Optimization Analysis")
    print("=" * 60)
    
    # Step 1: Initialize the main analyzer
    print("\n1. Initializing Transport Fare Analyzer...")
    analyzer = TransportFareAnalyzer()
    
    # Step 2: Load data
    print("\n2. Loading data...")
    analyzer.load_data()  # Uses sample data for demonstration
    
    print(f"   - SP Data: {analyzer.sp_data.shape[0]} observations")
    print(f"   - Income Groups: {analyzer.sp_data['income_group'].unique()}")
    print(f"   - Transport Modes: {analyzer.sp_data['mode'].unique()}")
    
    # Step 3: Run basic analyses
    print("\n3. Running basic analyses...")
    
    # Mode choice preferences
    print("   - Analyzing mode choice preferences...")
    mnl_model, income_analysis = analyzer.analyze_mode_choice_preferences()
    
    # Affordability analysis
    print("   - Analyzing affordability and willingness to pay...")
    elasticity_results, wtp_analysis = analyzer.analyze_affordability_and_wtp()
    
    # Welfare optimization
    print("   - Modeling social welfare outcomes...")
    welfare_results = analyzer.model_social_welfare_outcomes()
    
    # MCDA analysis
    print("   - Comparing cumulative social welfare...")
    mcda_results = analyzer.compare_cumulative_welfare()
    
    # Travel time analysis
    print("   - Analyzing travel time factors...")
    equity_analysis, vot_analysis = analyzer.analyze_travel_time_factors()
    
    # Policy evaluation
    print("   - Evaluating equity policies...")
    policy_results = analyzer.evaluate_equity_policies()
    
    # Step 4: Advanced analyses
    print("\n4. Running advanced analyses...")
    
    # Discrete Choice Modeling
    print("   - Advanced discrete choice modeling...")
    dcm_analyzer = DiscreteChoiceAnalyzer()
    dcm_results = dcm_analyzer.run_complete_dcm_analysis(analyzer.sp_data)
    
    # Welfare Optimization
    print("   - Advanced welfare optimization...")
    welfare_optimizer = WelfareOptimizer()
    optimization_results = welfare_optimizer.run_complete_optimization(
        analyzer.sp_data, analyzer.secondary_data
    )
    
    # Step 5: Generate outputs
    print("\n5. Generating outputs...")
    
    # Generate visualizations
    print("   - Creating interactive dashboard...")
    analyzer.generate_visualizations()
    
    # Generate reports
    print("   - Generating analysis reports...")
    analyzer.generate_report()
    
    # Step 6: Display key findings
    print("\n6. Key Findings Summary:")
    print("-" * 40)
    
    # Mode choice findings
    if 'mnl_mode_choice' in analyzer.models:
        model = analyzer.models['mnl_mode_choice']
        print(f"   • Model fit: Pseudo R² = {model.prsquared:.3f}")
    
    # Affordability findings
    if 'fare_elasticity' in analyzer.results:
        most_elastic = min(analyzer.results['fare_elasticity'].items(), key=lambda x: x[1])
        print(f"   • Most price-sensitive group: {most_elastic[0]} (elasticity: {most_elastic[1]:.3f})")
    
    # Welfare optimization findings
    if 'welfare_optimization' in analyzer.results:
        for mode, results in analyzer.results['welfare_optimization'].items():
            max_welfare = results['Max-S']
            print(f"   • {mode}: Optimal fare for social welfare = {max_welfare['optimal_fare']:.1f} BDT")
    
    # MCDA findings
    if 'mcda_analysis' in analyzer.results:
        best_mode = max(analyzer.results['mcda_analysis'].items(), 
                       key=lambda x: x[1]['weighted_score'])[0]
        print(f"   • Best performing mode: {best_mode}")
    
    # Policy findings
    if 'policy_evaluation' in analyzer.results:
        scenarios = list(analyzer.results['policy_evaluation'].keys())
        print(f"   • Policy scenarios analyzed: {len(scenarios)}")
    
    # Step 7: Policy recommendations
    print("\n7. Policy Recommendations:")
    print("-" * 40)
    recommendations = [
        "Implement income-based differentiated pricing",
        "Focus on social welfare maximization as primary objective",
        "Target subsidies to low-income users",
        "Improve service quality (comfort, reliability, travel time)",
        "Monitor and evaluate policy impacts regularly",
        "Consider environmental externalities in pricing decisions"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Step 8: Output files summary
    print("\n8. Generated Output Files:")
    print("-" * 40)
    output_files = [
        "transport_analysis_dashboard.html - Interactive dashboard",
        "transport_analysis_report.md - Comprehensive analysis report",
        "welfare_optimization_report.md - Optimization results"
    ]
    
    for file_info in output_files:
        print(f"   • {file_info}")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Open 'transport_analysis_dashboard.html' in your browser")
    print("2. Review 'transport_analysis_report.md' for detailed findings")
    print("3. Check 'welfare_optimization_report.md' for optimization results")
    print("4. Replace sample data with your actual data files")
    print("5. Customize analysis parameters as needed")

def run_quick_analysis():
    """
    Quick analysis for demonstration purposes
    """
    print("Quick Transport Fare Analysis Demo")
    print("=" * 40)
    
    # Initialize analyzer
    analyzer = TransportFareAnalyzer()
    analyzer.load_data()
    
    # Run quick analyses
    print("\nRunning quick analyses...")
    
    # Mode choice
    mnl_model, _ = analyzer.analyze_mode_choice_preferences()
    print(f"✓ Mode choice model fitted (R² = {mnl_model.prsquared:.3f})")
    
    # Affordability
    elasticity_results, wtp_analysis = analyzer.analyze_affordability_and_wtp()
    print(f"✓ Affordability analysis completed ({len(elasticity_results)} income groups)")
    
    # Welfare optimization
    welfare_results = analyzer.model_social_welfare_outcomes()
    print(f"✓ Welfare optimization completed ({len(welfare_results)} modes)")
    
    # MCDA
    mcda_results = analyzer.compare_cumulative_welfare()
    best_mode = max(mcda_results.items(), key=lambda x: x[1]['weighted_score'])[0]
    print(f"✓ MCDA completed (best mode: {best_mode})")
    
    # Generate dashboard
    analyzer.generate_visualizations()
    print("✓ Interactive dashboard generated")
    
    print("\nQuick analysis complete! Check 'transport_analysis_dashboard.html'")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dhaka Transport Fare Analysis")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick analysis demo")
    
    args = parser.parse_args()
    
    if args.quick:
        run_quick_analysis()
    else:
        main()