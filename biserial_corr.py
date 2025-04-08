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
    parser = argparse.ArgumentParser(
        description="Find biserial correlations for Defects4J projects"
    )
    parser.add_argument("--project_name", help="Chosen project name")
    args = parser.parse_args()

    if args.project_name:
        calculate_pb(args.project_name)
    else:
        combined_pb()


if __name__ == "__main__":
    main()
