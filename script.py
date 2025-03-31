import os
import argparse
from coverage import extract_real_condition_coverage
from defects4j_commands import (
    checkout_project,
    generate_coverage_report,
    generate_mutation_report,
)
from csv_helper import calculate_mutation_score, create_output_file, process_csv, process_output_csv, save_row


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = f"{SCRIPT_DIR}/output"
os.makedirs(output_dir, exist_ok=True)

def analyze_project(project_name, defects4j_path, id_range):
    bugs_csv_path = (
        f"{defects4j_path}/framework/projects/{project_name}/active-bugs.csv"
    )
    bug_info = process_csv(bugs_csv_path)

    # schema: [[bug_id, mutation_score, condition_coverage, bug_present]]
    output_csv_path = f"{SCRIPT_DIR}/output/{project_name}_analysis.csv"

    if not os.path.exists(output_csv_path):
        print(f"File {output_csv_path} not found. Creating a new one.")
        create_output_file(output_csv_path)

    history_list = process_output_csv(output_csv_path)
    id_history = {(int(bug["bug_id"]), bug["bug_present"] == "True"): bug for bug in history_list}

    for bug in bug_info:
        bug_id = bug["bug_id"]
        id_int = int(bug_id)

        if id_int < id_range[0] or id_range[1] < id_int:
            continue

        print(f"Analyzing bug {id_int}")

        if (id_int, True) in id_history:
            print(f"Skipping {id_int}b")
        else:
            print(f"Failing to Skip {id_int}b")
            project_path = checkout_project(project_name, bug_id, "b")
            os.chdir(project_path)

            generate_coverage_report()
            condition_coverage = extract_real_condition_coverage("coverage.xml")

            generate_mutation_report()
            mutation_score = calculate_mutation_score("summary.csv")

            save_row(output_csv_path, [bug_id, mutation_score, condition_coverage, True])

        # Now doing fixed version

        if (id_int, False) in id_history:
            print(f"Skipping {id_int}f")
        else:
            print(f"Failing to Skip {id_int}b")
            project_path = checkout_project(project_name, bug_id, "f")
            os.chdir(project_path)

            generate_coverage_report()
            condition_coverage = extract_real_condition_coverage("coverage.xml")

            generate_mutation_report()
            mutation_score = calculate_mutation_score("summary.csv")

            save_row(output_csv_path, [bug_id, mutation_score, condition_coverage, False])

def parse_id_range(value):
    """Parse an input in the form of 'min-max' and validate it."""
    try:
        min_id, max_id = map(int, value.split('-'))
        assert (min_id > 0)
        assert (min_id <= max_id)
        return min_id, max_id
    except Exception:
        raise argparse.ArgumentTypeError("Range must be in the format 'min-max' with min <= max and min > 0")

def main():
    parser = argparse.ArgumentParser(description='Analyze Defects4J projects')
    parser.add_argument('defects4j_path', help='Path to the Defects4J repository')
    parser.add_argument('project_name', help='Chosen project name')
    parser.add_argument('id_range', type=parse_id_range, help="Defect ID range in the format 'min-max'")
    args = parser.parse_args()

    os.chdir(args.defects4j_path)
    print(f"Analyzing {args.project_name}")
    analyze_project(args.project_name, args.defects4j_path, args.id_range)



if __name__ == "__main__":
    main()
