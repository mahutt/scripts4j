import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path

data_path = Path("./output")
box_plot_dir = f"./output/box_plot"
os.makedirs(box_plot_dir, exist_ok=True)


def create_dataframe(file_path):
    df = pd.read_csv(file_path)
    buggy_df = df[df["Bug Present"]]
    non_buggy_df = df[df["Bug Present"] == False]
    return buggy_df, non_buggy_df

def extract_project_name(file_name):
        return file_name.split("_")[0]

def create_box_plot(buggy_df, non_buggy_df, project_name):
    # Conditional Coverage
    plt.figure()
    plt.boxplot([buggy_df["Condition Coverage"], non_buggy_df["Condition Coverage"]], tick_labels=["Pre-fix", "Post-fix"])
    plt.ylabel("Condition Coverage (%)")
    plt.title(f"{project_name} Condition Coverage Box Plot")
    plt.savefig(f'{box_plot_dir}/{project_name}_conditional_coverage_box_plot.pdf')

    # Mutation Score
    plt.figure()
    plt.boxplot([buggy_df["Mutation Score"], non_buggy_df["Mutation Score"]], tick_labels=["Pre-fix", "Post-fix"])
    plt.ylabel("Mutation Score (%)")
    plt.title(f"{project_name} Mutation Score Box Plot")
    plt.savefig(f'{box_plot_dir}/{project_name}_mutation_score_box_plot.pdf')

def get_csv_files():
      return [f.name for f in data_path.glob("*.csv") if f.is_file()]

def main():
    csv_files = get_csv_files()

    for file in csv_files:
        buggy_df, non_buggy_df = create_dataframe(f"{data_path}/{file}")

        project_name = extract_project_name(file)
        create_box_plot(buggy_df, non_buggy_df, project_name)


if __name__ == "__main__":
    main()