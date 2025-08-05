#!/usr/bin/env python3
"""
Dhaka Public Transport Fare System Optimization - Analysis Execution Script
===========================================================================

This script executes the comprehensive thesis analysis for optimizing Dhaka's 
public transport fare system.

Usage:
    python run_thesis_analysis.py

Outputs:
    - comprehensive_analysis_dashboard.html (Interactive dashboard)
    - comprehensive_thesis_report.md (Detailed report)
    - analysis_summary.txt (Executive summary)
"""

import sys
import time
from datetime import datetime
from thesis_comprehensive_analysis import ThesisComprehensiveAnalyzer

def main():
    """Main execution function"""
    
    print("="*80)
    print("DHAKA PUBLIC TRANSPORT FARE SYSTEM OPTIMIZATION")
    print("COMPREHENSIVE THESIS ANALYSIS")
    print("="*80)
    print(f"Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Initialize the comprehensive analyzer
        print("Initializing analysis framework...")
        analyzer = ThesisComprehensiveAnalyzer()
        
        # Run the complete analysis
        print("Starting comprehensive analysis...")
        start_time = time.time()
        
        results = analyzer.run_complete_analysis()
        
        end_time = time.time()
        analysis_duration = end_time - start_time
        
        # Generate executive summary
        generate_executive_summary(results, analysis_duration)
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"Total analysis time: {analysis_duration:.2f} seconds")
        print()
        print("Generated Output Files:")
        print("1. comprehensive_analysis_dashboard.html - Interactive visualization dashboard")
        print("2. comprehensive_thesis_report.md - Detailed analysis report")
        print("3. analysis_summary.txt - Executive summary")
        print("4. thesis_methodology_documentation.md - Methodology documentation")
        print()
        print("Key Findings Summary:")
        print_summary_findings(results)
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Analysis failed with error: {str(e)}")
        print("Please check the data files and dependencies.")
        return False

def generate_executive_summary(results, duration):
    """Generate executive summary of the analysis"""
    
    summary = []
    summary.append("DHAKA PUBLIC TRANSPORT FARE SYSTEM OPTIMIZATION")
    summary.append("EXECUTIVE SUMMARY")
    summary.append("="*50)
    summary.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append(f"Analysis Duration: {duration:.2f} seconds")
    summary.append("")
    
    # Objective 1 Summary
    summary.append("OBJECTIVE 1: USER PREFERENCES AND AFFORDABILITY")
    summary.append("-" * 40)
    
    if 'objective_1' in results:
        wtp_analysis = results['objective_1']['wtp_analysis']
        affordability_analysis = results['objective_1']['affordability_analysis']
        
        for income_group in ['Low', 'Mid', 'High']:
            mean_wtp = wtp_analysis[income_group]['mean_wtp']
            unaffordable_pct = affordability_analysis[income_group]['unaffordable_percentage']
            summary.append(f"{income_group} Income Group:")
            summary.append(f"  - Mean WTP: {mean_wtp:.2f} BDT")
            summary.append(f"  - Unaffordable trips: {unaffordable_pct:.1f}%")
            summary.append("")
    
    # Objective 2 Summary
    summary.append("OBJECTIVE 2: SOCIAL WELFARE OPTIMIZATION")
    summary.append("-" * 40)
    
    if 'objective_2' in results:
        welfare_results = results['objective_2']['welfare_results']
        mcda_results = results['objective_2']['mcda_results']
        
        summary.append("Optimal Fare Levels (Social Welfare Maximization):")
        for mode, results_mode in welfare_results.items():
            optimal_price = results_mode['max_social_welfare']['optimal_price']
            social_welfare = results_mode['max_social_welfare']['optimal_revenue']
            summary.append(f"  {mode}: {optimal_price:.2f} BDT (Welfare: {social_welfare:.2f})")
        summary.append("")
        
        summary.append("MCDA Ranking (Overall Performance):")
        sorted_modes = sorted(mcda_results.items(), key=lambda x: x[1]['weighted_score'], reverse=True)
        for i, (mode, result) in enumerate(sorted_modes, 1):
            summary.append(f"  {i}. {mode}: {result['weighted_score']:.3f}")
        summary.append("")
    
    # Objective 3 Summary
    summary.append("OBJECTIVE 3: TRAVEL TIME AND EQUITY ANALYSIS")
    summary.append("-" * 40)
    
    if 'objective_3' in results:
        vot_analysis = results['objective_3']['vot_analysis']
        policy_analysis = results['objective_3']['policy_analysis']
        
        summary.append("Value of Time by Income Group:")
        for income_group in ['Low', 'Mid', 'High']:
            vot_per_hour = vot_analysis[income_group]['vot_per_hour']
            summary.append(f"  {income_group}: {vot_per_hour:.2f} BDT/hour")
        summary.append("")
        
        summary.append("Policy Recommendations:")
        best_policy = max(policy_analysis.items(), key=lambda x: x[1]['cost_effectiveness'])
        summary.append(f"  Recommended: {best_policy[0].replace('_', ' ').title()}")
        summary.append(f"  Cost Effectiveness: {best_policy[1]['cost_effectiveness']:.3f}")
        summary.append("")
    
    # Policy Recommendations
    summary.append("KEY POLICY RECOMMENDATIONS")
    summary.append("-" * 40)
    summary.append("1. Implement income-based differentiated pricing")
    summary.append("2. Provide targeted subsidies for low-income users")
    summary.append("3. Focus on reducing waiting times and improving comfort")
    summary.append("4. Consider social welfare maximization as primary objective")
    summary.append("5. Monitor affordability thresholds by income group")
    summary.append("6. Incorporate environmental externalities in pricing")
    summary.append("")
    
    summary.append("For detailed analysis and methodology, please refer to:")
    summary.append("- comprehensive_thesis_report.md")
    summary.append("- thesis_methodology_documentation.md")
    summary.append("- comprehensive_analysis_dashboard.html")
    
    # Save summary
    with open('analysis_summary.txt', 'w') as f:
        f.write('\n'.join(summary))
    
    print("✓ Executive summary generated: analysis_summary.txt")

def print_summary_findings(results):
    """Print key findings summary"""
    
    print("📊 ANALYSIS RESULTS SUMMARY:")
    print()
    
    # Data overview
    if hasattr(results, 'sp_data'):
        print(f"📈 Data Overview:")
        print(f"   - Total observations: {len(results.sp_data)}")
        print(f"   - Transport modes: {', '.join(results.sp_data['Mode_Used'].unique())}")
        print(f"   - Income groups: {', '.join(results.sp_data['Income_Bracket'].unique())}")
        print()
    
    # Key insights
    print("🔍 Key Insights:")
    
    if 'objective_1' in results:
        wtp_analysis = results['objective_1']['wtp_analysis']
        affordability_analysis = results['objective_1']['affordability_analysis']
        
        # Find most affordable income group
        most_affordable = min(affordability_analysis.items(), 
                            key=lambda x: x[1]['unaffordable_percentage'])
        print(f"   - Most affordable for: {most_affordable[0]} income group")
        
        # Find highest WTP income group
        highest_wtp = max(wtp_analysis.items(), 
                         key=lambda x: x[1]['mean_wtp'])
        print(f"   - Highest WTP: {highest_wtp[0]} income group")
    
    if 'objective_2' in results:
        mcda_results = results['objective_2']['mcda_results']
        best_mode = max(mcda_results.items(), key=lambda x: x[1]['weighted_score'])
        print(f"   - Best performing mode: {best_mode[0]}")
    
    if 'objective_3' in results:
        policy_analysis = results['objective_3']['policy_analysis']
        best_policy = max(policy_analysis.items(), key=lambda x: x[1]['cost_effectiveness'])
        print(f"   - Recommended policy: {best_policy[0].replace('_', ' ').title()}")
    
    print()
    print("📋 Next Steps:")
    print("   1. Review the interactive dashboard for detailed visualizations")
    print("   2. Read the comprehensive report for detailed analysis")
    print("   3. Consider the policy recommendations for implementation")
    print("   4. Validate results with stakeholders and experts")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)