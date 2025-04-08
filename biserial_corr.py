import argparse
import pandas as pd
from scipy import stats
import glob
import os
from boxplotter import box_plot_from_output_file


def calculate_pb(project_name: str, results_df=None):
    df = pd.read_csv(f"output/{project_name}_analysis.csv")
    cov_array = df["Condition Coverage"]
    mut_array = df["Mutation Score"]
    bool_array = df["Bug Present"] == True

    pb_cov = stats.pointbiserialr(cov_array, bool_array)
    pb_mut = stats.pointbiserialr(mut_array, bool_array)

    project_results = pd.DataFrame(
        {
            "Project": [project_name, project_name],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [pb_cov[0], pb_mut[0]],
            "P_Value": [pb_cov[1], pb_mut[1]],
        }
    )

    if results_df is None:
        return project_results
    else:
        return pd.concat([results_df, project_results], ignore_index=True)


def combined_pb(results_df):
    """Calculate point-biserial correlation for combined data and add to results."""
    csv_files = glob.glob("./output/*_analysis.csv")
    dataframes = []
    for file in csv_files:
        print(f"Found file {file}")
        dataframes.append(pd.read_csv(file))

    combined_df = pd.concat(dataframes)
    combined_cov_array = combined_df["Condition Coverage"]
    combined_mut_array = combined_df["Mutation Score"]
    combined_bool_array = combined_df["Bug Present"] == True

    combined_pb_cov = stats.pointbiserialr(combined_cov_array, combined_bool_array)
    combined_pb_mut = stats.pointbiserialr(combined_mut_array, combined_bool_array)

    combined_results = pd.DataFrame(
        {
            "Project": ["Combined", "Combined"],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [combined_pb_cov[0], combined_pb_mut[0]],
            "P_Value": [combined_pb_cov[1], combined_pb_mut[1]],
        }
    )

    return pd.concat([results_df, combined_results], ignore_index=True)


def main():
    # Create an empty DataFrame to store all results
    all_results = pd.DataFrame(columns=["Project", "Metric", "Correlation", "P_Value"])

    # Get all CSV files in the output directory
    csv_files = glob.glob("./output/*_analysis.csv")

    # Process each project individually
    for file in csv_files:
        # Extract project name from filename (remove path and _analysis.csv suffix)
        project_name = os.path.basename(file).replace("_analysis.csv", "")
        print(f"Processing {project_name}...")
        all_results = calculate_pb(project_name, all_results)

        # Create box plot for the project
        box_plot_from_output_file(file.split("/")[-1])
        print(f"Box plot for {project_name} created.")

    # Process all projects combined
    print("Processing combined data...")
    all_results = combined_pb(all_results)

    # Create results directory if it doesn't exist
    os.makedirs("analysis", exist_ok=True)

    # Save all results to a single CSV file
    all_results.to_csv("analysis/analysis_results.csv", index=False)
    print("All results saved to analysis/analysis_results.csv")
    print("Analysis complete!")


if __name__ == "__main__":
    main()
