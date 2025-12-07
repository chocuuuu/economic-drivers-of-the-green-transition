from data_loader import load_and_clean_data
from eda import perform_eda
from visualizer import generate_visualizations
from interactive_dashboard import generate_interactive_dashboard

def main():
    print("Starting Global Energy Analysis Pipeline...")
    
    # 1. Load Data
    df = load_and_clean_data()
    
    # 2. Run EDA
    perform_eda(df)
    
    # 3. Generate Static Visuals (for PDF Report)
    generate_visualizations(df)
    
    # 4. Generate Interactive Dashboard (HTML)
    generate_interactive_dashboard(df)
    
    print("\nPipeline Complete. Check the 'figures/' folder for outputs.")

if __name__ == "__main__":
    main()