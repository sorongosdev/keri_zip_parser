import os
import csv
import re

def extract_case_numbers(root_directory):
    case_numbers = set()  # Use a set to avoid duplicates
    for folder_name in os.listdir(root_directory):
        if folder_name == '241203_241211':  # Check if the folder name matches '241203_241211'
            folder_path = os.path.join(root_directory, folder_name)
            if os.path.isdir(folder_path):
                for subfolder_name in os.listdir(folder_path):
                    subfolder_path = os.path.join(folder_path, subfolder_name)
                    if os.path.isdir(subfolder_path):
                        case_number_match = re.search(r'\d{5}', subfolder_name)
                        if case_number_match:
                            case_number = case_number_match.group(0)
                            case_numbers.add(case_number)
    return case_numbers

def create_csv(root_directory, output_csv):
    case_numbers = extract_case_numbers(root_directory)
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write header
        csvwriter.writerow(['증례번호', '공통이슈', 'eeg 채널L', 'eeg 채널R', '특이사항'])
        
        # Write case numbers
        for case_number in sorted(case_numbers):
            csvwriter.writerow([case_number])

# 사용 예시
root_directory = './'
output_csv = 'output_csv_xlsx/output_241203_241211.csv'
create_csv(root_directory, output_csv)