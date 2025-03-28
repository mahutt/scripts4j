import os
import argparse
from coverage import extract_real_condition_coverage
from defects4j_commands import (
    checkout_project,
    generate_coverage_report,
    generate_mutation_report,
)
from csv_helper import calculate_mutation_score, create_output_file, process_csv, save_row


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = f"{SCRIPT_DIR}/output"
os.makedirs(output_dir, exist_ok=True)

SELECTED_PROJECT_NAMES = ["Closure", "Math", "JacksonDatabind"]

def analyze_project(project_name, defects4j_path):
    bugs_csv_path = (
        f"{defects4j_path}/framework/projects/{project_name}/active-bugs.csv"
    )
    bug_info = process_csv(bugs_csv_path)

    # schema: [[bug_id, mutation_score, condition_coverage, bug_present]]
    output_csv_path = f"{SCRIPT_DIR}/output/{project_name}_analysis.csv"
    create_output_file(output_csv_path)

    for bug in bug_info:
        bug_id = bug["bug_id"]
        print(f"Analyzing bug {bug_id}")

        project_path = checkout_project(project_name, bug_id, "b")
        os.chdir(project_path)

        generate_coverage_report()
        condition_coverage = extract_real_condition_coverage("coverage.xml")

        generate_mutation_report()
        mutation_score = calculate_mutation_score("summary.csv")

        save_row(output_csv_path, [bug_id, mutation_score, condition_coverage, True])

        # Now doing fixed version

        project_path = checkout_project(project_name, bug_id, "f")
        os.chdir(project_path)

        generate_coverage_report()
        condition_coverage = extract_real_condition_coverage("coverage.xml")

        generate_mutation_report()
        mutation_score = calculate_mutation_score("summary.csv")

        save_row(output_csv_path, [bug_id, mutation_score, condition_coverage, False])


def main():
    parser = argparse.ArgumentParser(description='Analyze Defects4J projects')
    parser.add_argument('defects4j_path', help='Path to the Defects4J repository')
    args = parser.parse_args()

    os.chdir(args.defects4j_path)
    for project_name in SELECTED_PROJECT_NAMES:
        print(f"Analyzing {project_name}")
        analyze_project(project_name, args.defects4j_path)



if __name__ == "__main__":
    main()
