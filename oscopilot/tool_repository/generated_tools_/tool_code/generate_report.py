def generate_report(report_data, report_file_path):
    """
    Generate a report with the provided data in the specified file.

    Args:
        report_data (dict): Dictionary containing the report data including the number of files detected, at risk, and the issue details.
        report_file_path (str): The absolute file path where the report will be generated.

    Returns:
        str: Information indicating that the report has been successfully generated.
    """
    try:
        with open(report_file_path, 'w') as report_file:
            report_file.write(f"Number of files detected: {report_data.get('detected_files', 0)}\n")
            report_file.write(f"Number of files at risk: {report_data.get('at_risk_files', 0)}\n")
            report_file.write("Issue Details:\n")
            for file_info in report_data.get('issue_details', []):
                report_file.write(f"File: {file_info.get('file_name')}\n")
                report_file.write(f"Issue: {file_info.get('issue_type')} in {file_info.get('issue_location')}\n\n")

        return "Report generated successfully."
    except Exception as e:
        return f"Error generating report: {str(e)}"