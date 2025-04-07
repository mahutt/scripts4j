import argparse
import pandas as pd
from scipy import stats
import glob


def calculate_pb(project_name: str):
    df = pd.read_csv(f"output/{project_name}_analysis.csv")

    cov_array = df["Condition Coverage"]
    mut_array = df["Mutation Score"]
    bool_array = df["Bug Present"] == True

    pb_cov = stats.pointbiserialr(cov_array, bool_array)

    print(
    f"""
    We calculate a Point-Biserial Correlation coefficient of\n
    r = {pb_cov[0]} with p-value\n
    p = {pb_cov[1]} for coverage and bugs existing in {project_name}.
    """
    )

    pb_mut = stats.pointbiserialr(mut_array, bool_array)

    print(
    f"""
    We calculate a Point-Biserial Correlation coefficient of\n
    r = {pb_mut[0]} with p-value\n
    p = {pb_mut[1]} for mutation score and bugs existing in {project_name}.
    """
    )


def combined_pb():
    csv_files = glob.glob(".\\output\\*.csv")
    dataframes = []

    for file in csv_files:
        print(f"found file {file}")
        dataframes.append(pd.read_csv(file))

    combined_df = pd.concat(dataframes)

    combined_cov_array = combined_df["Condition Coverage"]
    combined_mut_array = combined_df["Mutation Score"]
    combined_bool_array = combined_df["Bug Present"] == True

    combined_pb_cov = stats.pointbiserialr(combined_cov_array, combined_bool_array)

    print(
    f"""
    We calculate a Point-Biserial Correlation coefficient of\n
    r = {combined_pb_cov[0]} with p-value\n
    p = {combined_pb_cov[1]} for coverage and bugs existing in the combined projects.
    """
    )

    combined_pb_mut = stats.pointbiserialr(combined_mut_array, combined_bool_array)

    print(
    f"""
    We calculate a Point-Biserial Correlation coefficient of\n
    r = {combined_pb_cov[0]} with p-value\n
    p = {combined_pb_mut[1]} for mutation score and bugs existing in the combined projects.
    """
    )


def main():
    parser = argparse.ArgumentParser(description="Find biserial correlations for Defects4J projects")
    parser.add_argument("--project_name", help="Chosen project name")
    args = parser.parse_args()

    if args.project_name:
        calculate_pb(args.project_name)
    else:
        combined_pb()


if __name__ == "__main__":
    main()