import subprocess


def checkout_project(project_name: str, bug_id: int, type: str) -> str:
    project_path = f"/tmp/defects4j_experiment/{project_name}"
    checkout_command = (
        f"defects4j checkout -p {project_name} -v {bug_id}{type} -w {project_path}"
    )
    print(f"Running: {checkout_command}")
    try:
        result = subprocess.run(
            checkout_command, shell=True, check=True, text=True, capture_output=True
        )
        print(f"Success: {result.stdout}")
        return project_path
    except subprocess.CalledProcessError as e:
        print(f"Error with {project_name}: {e.stderr}")


def generate_coverage_report() -> None:
    test_command = "defects4j coverage"

    try:
        print(f"Running: {test_command}")
        test_result = subprocess.run(
            test_command, shell=True, check=True, text=True, capture_output=True
        )
        print(f"Coverage success: {test_result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")


def generate_mutation_report() -> None:
    test_command = "defects4j mutation"

    try:
        print(f"Running: {test_command}")
        test_result = subprocess.run(
            test_command, shell=True, check=True, text=True, capture_output=True
        )
        print(f"Coverage success: {test_result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
