import os
import zipfile
import re

def rename_zip_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            parts = filename.split('_')
            if len(parts) > 2:  # 주제와 설명이 모두 포함된 경우
                topic = parts[1]
                
                new_filename = None
                if topic == '그림':
                    new_filename = f'1.{filename}'
                elif topic == '이야기':
                    new_filename = f'2.{filename}'
                elif topic == '절차':
                    new_filename = f'3.{filename}'
                elif topic == '대화형':
                    new_filename = f'10.{filename}'

                if new_filename:
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_filename)
                    os.rename(old_path, new_path)
                    print(f'Renamed: {old_path} -> {new_path}')

def process_zip_files(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            case_number_match = re.search(r'\d{5}', filename)
            
            if case_number_match:
                case_number = case_number_match.group(0)
                case_folder = os.path.join(directory, case_number)
                if not os.path.exists(case_folder):
                    os.makedirs(case_folder)
                new_zip_name = f"{os.path.splitext(filename)[0]}_E.zip"
                new_zip_path = os.path.join(case_folder, new_zip_name)
            else:
                new_zip_name = f"{os.path.splitext(filename)[0]}_E.zip"
                new_zip_path = os.path.join(directory, new_zip_name)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                txt_files = [f for f in zip_ref.namelist() if f.endswith('.txt')]
                
                with zipfile.ZipFile(new_zip_path, 'w') as new_zip:
                    for txt_file in txt_files:
                        new_zip.writestr(txt_file, zip_ref.read(txt_file))

                # Create a temporary zip file without the txt files
                temp_zip_path = zip_path + '.tmp'
                with zipfile.ZipFile(temp_zip_path, 'w') as temp_zip:
                    for item in zip_ref.infolist():
                        if item.filename not in txt_files:
                            temp_zip.writestr(item.filename, zip_ref.read(item.filename))

            # Create a zip file with the remaining files in the original directory
            remaining_zip_name = f"{os.path.splitext(filename)[0]}.zip"
            remaining_zip_path = os.path.join(case_folder, remaining_zip_name)
            with zipfile.ZipFile(remaining_zip_path, 'w') as remaining_zip:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    for item in zip_ref.infolist():
                        if item.filename not in txt_files:
                            remaining_zip.writestr(item.filename, zip_ref.read(item.filename))
            print(f'Created remaining zip: {remaining_zip_path}')

            # Replace the original zip file with the temporary zip file
            os.remove(zip_path)
            os.rename(temp_zip_path, zip_path)
            print(f'Processed: {zip_path} -> {new_zip_path}')

            # Move the new zip file to the case folder in the output directory
            case_folder_output = os.path.join(output_directory, case_number)
            if not os.path.exists(case_folder_output):
                os.makedirs(case_folder_output)
            final_zip_path = os.path.join(case_folder_output, os.path.basename(new_zip_path))
            os.rename(new_zip_path, final_zip_path)
            print(f'Moved: {new_zip_path} -> {final_zip_path}')

# 사용 예시
directories = ['./241203_241211', './241203_241211_E']
for directory in directories:
    rename_zip_files(directory)
    output_directory = './241203_241211_E'
    process_zip_files(directory, output_directory)