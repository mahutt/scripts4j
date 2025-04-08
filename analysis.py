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

    # Calculate point-biserial correlation
    pb_cov = stats.pointbiserialr(cov_array, bool_array)
    pb_mut = stats.pointbiserialr(mut_array, bool_array)

    # Calculate mean and median statistics when bug is present vs absent
    bug_present = df[df["Bug Present"] == True]
    bug_absent = df[df["Bug Present"] == False]

    # Coverage statistics
    cov_present_mean = bug_present["Condition Coverage"].mean()
    cov_present_median = bug_present["Condition Coverage"].median()
    cov_absent_mean = bug_absent["Condition Coverage"].mean()
    cov_absent_median = bug_absent["Condition Coverage"].median()

    # Mutation score statistics
    mut_present_mean = bug_present["Mutation Score"].mean()
    mut_present_median = bug_present["Mutation Score"].median()
    mut_absent_mean = bug_absent["Mutation Score"].mean()
    mut_absent_median = bug_absent["Mutation Score"].median()

    project_results = pd.DataFrame(
        {
            "Project": [project_name, project_name],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [pb_cov[0], pb_mut[0]],
            "P_Value": [pb_cov[1], pb_mut[1]],
            "Bug_Present_Mean": [cov_present_mean, mut_present_mean],
            "Bug_Present_Median": [cov_present_median, mut_present_median],
            "Bug_Absent_Mean": [cov_absent_mean, mut_absent_mean],
            "Bug_Absent_Median": [cov_absent_median, mut_absent_median],
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

    # Calculate point-biserial correlation
    combined_pb_cov = stats.pointbiserialr(combined_cov_array, combined_bool_array)
    combined_pb_mut = stats.pointbiserialr(combined_mut_array, combined_bool_array)

    # Calculate mean and median statistics when bug is present vs absent
    bug_present = combined_df[combined_df["Bug Present"] == True]
    bug_absent = combined_df[combined_df["Bug Present"] == False]

    # Coverage statistics
    cov_present_mean = bug_present["Condition Coverage"].mean()
    cov_present_median = bug_present["Condition Coverage"].median()
    cov_absent_mean = bug_absent["Condition Coverage"].mean()
    cov_absent_median = bug_absent["Condition Coverage"].median()

    # Mutation score statistics
    mut_present_mean = bug_present["Mutation Score"].mean()
    mut_present_median = bug_present["Mutation Score"].median()
    mut_absent_mean = bug_absent["Mutation Score"].mean()
    mut_absent_median = bug_absent["Mutation Score"].median()

    combined_results = pd.DataFrame(
        {
            "Project": ["Combined", "Combined"],
            "Metric": ["Coverage", "Mutation Score"],
            "Correlation": [combined_pb_cov[0], combined_pb_mut[0]],
            "P_Value": [combined_pb_cov[1], combined_pb_mut[1]],
            "Bug_Present_Mean": [cov_present_mean, mut_present_mean],
            "Bug_Present_Median": [cov_present_median, mut_present_median],
            "Bug_Absent_Mean": [cov_absent_mean, mut_absent_mean],
            "Bug_Absent_Median": [cov_absent_median, mut_absent_median],
        }
    )

    return pd.concat([results_df, combined_results], ignore_index=True)


def main():
    # Create an empty DataFrame to store all results
    all_results = pd.DataFrame(
        columns=[
            "Project",
            "Metric",
            "Correlation",
            "P_Value",
            "Bug_Present_Mean",
            "Bug_Present_Median",
            "Bug_Absent_Mean",
            "Bug_Absent_Median",
        ]
    )

    # Get all CSV files in the output directory
    csv_files = glob.glob("./output/*_analysis.csv")

    # Process each project individually
    for file in csv_files:
        # Extract project name from filename (remove path and *analysis.csv suffix)
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
