import os
import csv
import zipfile

def get_e_folders(root_dir):
    e_folders = []
    for folder_name in os.listdir(root_dir):
        if folder_name.endswith('_E') and os.path.isdir(os.path.join(root_dir, folder_name)):
            e_folders.append(folder_name)
    print("e_folders: ", e_folders)
    return e_folders

def validate_eeg_channels(data, zip_file_name, txt_file_name):
    if not data:
        print(f"No data found in {zip_file_name}/{txt_file_name}, returning 'X', 'X'")
        return 'X', 'X'
    
    result_l = 'O'
    result_r = 'O'
    
    # Check if all values in the left channel are the same
    if all(value[0] == data[0][0] for value in data):
        result_l = 'X'
        print(f"Left Channel Issue in {zip_file_name}/{txt_file_name}: All values are the same")
    
    # Check if all values in the right channel are the same
    if all(value[1] == data[0][1] for value in data):
        result_r = 'X'
        print(f"Right Channel Issue in {zip_file_name}/{txt_file_name}: All values are the same")
    
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
    e_folders = get_e_folders(root_directory)
    
    for case_folder_name in e_folders:
        case_folder_path = os.path.join(root_directory, case_folder_name)
        for item in os.listdir(case_folder_path):
            item_path = os.path.join(case_folder_path, item)
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
            csvwriter.writerow(['Case Number', 'Other Column', 'EEG Channel L', 'EEG Channel R', 'Memo'])
    
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)
        
        # Write header
        try:
            header = next(csvreader)
        except StopIteration:
            header = ['Case Number', 'Other Column', 'EEG Channel L', 'EEG Channel R', 'Memo']
        csvwriter.writerow(header)
        
        # Update rows
        for row in csvreader:
            case_number = row[0]
            if case_number in validation_results:
                row[2], row[3] = validation_results[case_number]
            csvwriter.writerow(row)
        
        # Add any missing cases from validation_results
        existing_cases = {row[0] for row in csvreader}
        for case_number, (result_l, result_r) in validation_results.items():
            if case_number not in existing_cases:
                csvwriter.writerow([case_number, '', result_l, result_r, ''])

def eeg_memo_hn(input_csv):
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
        csvreader = csv.reader(infile)
        rows = list(csvreader)
    
    with open(input_csv, 'w', newline='', encoding='utf-8') as outfile:
        csvwriter = csv.writer(outfile)
        header = rows[0]
        csvwriter.writerow(header)
        
        for row in rows[1:]:
            if row[2] == 'X' and row[3] == 'X':
                row[4] = 'HN'
            csvwriter.writerow(row)

# 사용 예시
root_directory = './'
validation_results = process_zip_files(root_directory)
input_csv = 'validate_eeg_output.csv'
output_csv = 'eeg_memo_hn_output.csv'
update_csv_with_validation(input_csv, output_csv, validation_results)
eeg_memo_hn(output_csv)