import csv
import sys


def process_csv(file_path) -> list:
    try:
        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            bugs = []
            for row in csv_reader:
                bug_info = {
                    "bug_id": row["bug.id"],
                    "revision_buggy": row["revision.id.buggy"],
                    "revision_fixed": row["revision.id.fixed"],
                }
                bugs.append(bug_info)
            return bugs

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        sys.exit(1)


def calculate_mutation_score(csv_path):
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        row = next(reader)

        mutants_killed = int(row["MutantsKilled"])
        mutants_retained = int(row["MutantsRetained"])

        return (
            0.0 if mutants_retained == 0 else (mutants_killed / mutants_retained) * 100
        )


def create_output_file(path: str):
    with open(path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Bug ID", "Mutation Score", "Condition Coverage", "Bug Present"])

def save_row(path: str, row: list):
    with open(path, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(row)