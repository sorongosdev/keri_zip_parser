import os
import zipfile
import csv

def get_e_folders(root_dir):
    e_folders = []
    for folder_name in os.listdir(root_dir):
        if folder_name.endswith('_E') and os.path.isdir(os.path.join(root_dir, folder_name)):
            e_folders.append(folder_name)
    print("e_folders: ", e_folders)
    return e_folders

def validate_eeg_channels(data):
    if not data:
        print("No data found, returning 'X', 'X'")
        return 'X', 'X'
    
    result_l = 'O'
    result_r = 'O'
    
    for i in range(1, len(data)):
        if data[i][0] == data[i-1][0]:
            result_l = 'X'
        if data[i][1] == data[i-1][1]:
            result_r = 'X'
    
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
                        print('Processing zip file: ', file_name)
                        zip_path = os.path.join(item_path, file_name)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            for txt_file_name in zip_ref.namelist():
                                if txt_file_name.endswith('.txt'):
                                    with zip_ref.open(txt_file_name) as file:
                                        lines = file.readlines()[1:]  # 두 번째 줄부터 끝까지 읽기
                                        if not lines:
                                            print(f"No lines found in {txt_file_name}, returning 'X', 'X'")
                                            validation_results[item] = ('X', 'X')
                                            continue
                                        data = []
                                        for line in lines:
                                            parts = line.decode('utf-8').strip().split('=')[1].strip().split()
                                            for i in range(0, len(parts), 2):
                                                data.append([parts[i], parts[i+1]])
                                        result_l, result_r = validate_eeg_channels(data)
                                        validation_results[item] = (result_l, result_r)
    print("validation_results: ", validation_results)
    return validation_results

def update_csv_with_validation(input_csv, output_csv, validation_results):
    # 파일이 존재하지 않으면 새로 생성
    if not os.path.exists(input_csv):
        with open(input_csv, 'w', newline='', encoding='utf-8') as infile:
            csvwriter = csv.writer(infile)
            csvwriter.writerow(['Case Number', 'Other Column', 'EEG Channel L', 'EEG Channel R'])

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
                csvwriter.writerow([case_number, '', result_l, result_r])

# 사용 예시
root_directory = './'
validation_results = process_zip_files(root_directory)
input_csv = 'common_issue_pic2_output.csv'
output_csv = 'validate_eeg_output.csv'
update_csv_with_validation(input_csv, output_csv, validation_results)