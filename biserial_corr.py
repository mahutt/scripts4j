import argparse
import pandas as pd
from scipy import stats
import glob
import os


def calculate_pb(project_name: str):
    df = pd.read_csv(f"output/{project_name}_analysis.csv")
    cov_array = df["Condition Coverage"]
    mut_array = df["Mutation Score"]
    bool_array = df["Bug Present"] == True

    pb_cov = stats.pointbiserialr(cov_array, bool_array)
    pb_mut = stats.pointbiserialr(mut_array, bool_array)

    results = pd.DataFrame(
        {
            "Project": [project_name, project_name],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [pb_cov[0], pb_mut[0]],
            "P_Value": [pb_cov[1], pb_mut[1]],
        }
    )

    # Create results directory if it doesn't exist
    os.makedirs("analysis", exist_ok=True)
    results.to_csv(f"analysis/{project_name}_correlation_results.csv", index=False)
    print(f"Results saved to analysis/{project_name}_correlation_results.csv")


def combined_pb():
    csv_files = glob.glob("./output/*.csv")
    dataframes = []
    for file in csv_files:
        print(f"found file {file}")
        dataframes.append(pd.read_csv(file))

    combined_df = pd.concat(dataframes)
    combined_cov_array = combined_df["Condition Coverage"]
    combined_mut_array = combined_df["Mutation Score"]
    combined_bool_array = combined_df["Bug Present"] == True

    combined_pb_cov = stats.pointbiserialr(combined_cov_array, combined_bool_array)
    combined_pb_mut = stats.pointbiserialr(combined_mut_array, combined_bool_array)

    results = pd.DataFrame(
        {
            "Project": ["combined", "combined"],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [combined_pb_cov[0], combined_pb_mut[0]],
            "P_Value": [combined_pb_cov[1], combined_pb_mut[1]],
        }
    )

    # Create results directory if it doesn't exist
    os.makedirs("analysis", exist_ok=True)
    results.to_csv("analysis/combined_correlation_results.csv", index=False)
    print("Results saved to analysis/combined_correlation_results.csv")


def main():
    # Get all CSV files in the output directory
    csv_files = glob.glob("./output/*_analysis.csv")

    # Process each project individually
    for file in csv_files:
        # Extract project name from filename (remove path and _analysis.csv suffix)
        project_name = os.path.basename(file).replace("_analysis.csv", "")
        print(f"Processing {project_name}...")
        calculate_pb(project_name)

    # Process all projects combined
    print("Processing combined data...")
    combined_pb()

    print("All analysis complete!")


if __name__ == "__main__":
    main()
