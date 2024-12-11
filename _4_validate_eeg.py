import os
import csv
import zipfile

def validate_eeg_channels(data, zip_file_name, txt_file_name):
    result_l, result_r = 'O', 'O'
    # Existing check for three consecutive same values
    for i in range(2, len(data)):
        if data[i][0] == data[i-1][0] == data[i-2][0]:
            result_l = 'X'
            print(f"Left Channel Issue in {zip_file_name}/{txt_file_name} at line {i+1}")
        if data[i][1] == data[i-1][1] == data[i-2][1]:
            result_r = 'X'
            print(f"Right Channel Issue in {zip_file_name}/{txt_file_name} at line {i+1}")
        if result_l == 'X' or result_r == 'X':
            break
    
    return result_l, result_r

def process_zip_files(root_directory):
    validation_results = {}
    target_folder = '241203_241211_E'
    target_folder_path = os.path.join(root_directory, target_folder)
    
    if os.path.isdir(target_folder_path):
        for item in os.listdir(target_folder_path):
            item_path = os.path.join(target_folder_path, item)
            if os.path.isdir(item_path):
                for file_name in os.listdir(item_path):
                    if file_name.endswith('.zip'):
                        zip_path = os.path.join(item_path, file_name)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            for txt_file_name in zip_ref.namelist():
                                if txt_file_name.endswith('.txt'):
                                    with zip_ref.open(txt_file_name) as file:
                                        lines = file.readlines()[1:]  # 두 번째 줄부터 끝까지 읽기
                                        if not lines:
                                            print(f"No lines found in {zip_path}/{txt_file_name}")
                                            validation_results[item] = ('X', 'X')                                           
                                            continue
                                        data = []
                                        for line in lines:
                                            parts = line.decode('utf-8').strip().split('=')[1].strip().split()
                                            for i in range(0, len(parts), 2):
                                                data.append([parts[i], parts[i+1]])
                                        result_l, result_r = validate_eeg_channels(data, zip_path, txt_file_name)
                                        validation_results[item] = (result_l, result_r)
    return validation_results

def update_csv_with_validation(input_csv, output_csv, validation_results):
    # 파일이 존재하지 않으면 새로 생성
    if not os.path.exists(input_csv):
        with open(input_csv, 'w', newline='', encoding='utf-8') as infile:
            csvwriter = csv.writer(infile)
            csvwriter.writerow(['Case Number', 'Other Column', 'EEG Channel L', 'EEG Channel R'])

    existing_cases = set()
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)
        
        # Write header
        try:
            header = next(csvreader)
        except StopIteration:
            header = ['Case Number', 'Other Column', 'EEG Channel L', 'EEG Channel R']
        csvwriter.writerow(header)
        
        # Update rows and track existing cases
        for row in csvreader:
            case_number = row[0]
            existing_cases.add(case_number)
            if case_number in validation_results:
                # Ensure the row has at least 4 elements
                while len(row) < 4:
                    row.append('')
                row[2], row[3] = validation_results[case_number]
            csvwriter.writerow(row)
        
        # Add any missing cases from validation_results
        for case_number, (result_l, result_r) in validation_results.items():
            if case_number not in existing_cases:
                csvwriter.writerow([case_number, '', result_l, result_r])

# 사용 예시
root_directory = './'
validation_results = process_zip_files(root_directory)
input_csv = 'output_csv_xlsx/output_241203_241211.csv'
output_csv = 'output_csv_xlsx/validate_eeg_output_241203_241211.csv'
update_csv_with_validation(input_csv, output_csv, validation_results)