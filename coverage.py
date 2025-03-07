import xml.etree.ElementTree as ET


def extract_real_condition_coverage(coverage_file_path):
    tree = ET.parse(coverage_file_path)
    root = tree.getroot()

    condition_coverage_values = []

    condition_elements = root.findall(".//condition")
    for condition in condition_elements:
        coverage_str = condition.get("coverage")
        coverage_value = float(coverage_str[:-1])
        condition_coverage_values.append(coverage_value)

    return sum(condition_coverage_values) / len(condition_coverage_values)

