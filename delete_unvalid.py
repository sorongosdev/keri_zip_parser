import os
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
        # print(f"Left Channel Issue in {zip_file_name}/{txt_file_name}: All values are the same")
    
    # Check if all values in the right channel are the same
    if all(value[1] == data[0][1] for value in data):
        result_r = 'X'
        # print(f"Right Channel Issue in {zip_file_name}/{txt_file_name}: All values are the same")
    
    # Existing check for three consecutive same values
    for i in range(2, len(data)):
        if data[i][0] == data[i-1][0] == data[i-2][0]:
            result_l = 'X'
            # print(f"Left Channel Issue in {zip_file_name}/{txt_file_name} at line {i+1}")
        if data[i][1] == data[i-1][1] == data[i-2][1]:
            result_r = 'X'
            # print(f"Right Channel Issue in {zip_file_name}/{txt_file_name} at line {i+1}")
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
                                    try:
                                        with zip_ref.open(txt_file_name) as file:
                                            lines = file.readlines()[1:]  # 두 번째 줄부터 끝까지 읽기
                                            if not lines:
                                                print(f"No lines found in {zip_path}/{txt_file_name}")
                                                delete_unvalid(zip_path, txt_file_name)
                                                continue
                                            data = []
                                            for line in lines:
                                                parts = line.decode('utf-8').strip().split('=')[1].strip().split()
                                                for i in range(0, len(parts), 2):
                                                    data.append([parts[i], parts[i+1]])
                                            result_l, result_r = validate_eeg_channels(data, zip_path, txt_file_name)
                                            validation_results[item] = (result_l, result_r)
                                    except zipfile.BadZipFile as e:
                                        print(f"BadZipFile error for {txt_file_name} in {zip_path}: {e}")
                                        delete_unvalid(zip_path, txt_file_name)
    return validation_results

def delete_unvalid(zip_path, txt_file_name):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        temp_dir = os.path.join(os.path.dirname(zip_path), 'temp_unzip')
        os.makedirs(temp_dir, exist_ok=True)
        zip_ref.extractall(temp_dir)
    
    txt_file_path = os.path.join(temp_dir, txt_file_name)
    if os.path.exists(txt_file_path):
        os.remove(txt_file_path)
        print(f"Deleted invalid file: {txt_file_path}")
    
    # Recreate the zip file without the invalid text file
    with zipfile.ZipFile(zip_path, 'w') as zip_ref:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zip_ref.write(file_path, arcname)
    
    # Clean up the temporary directory
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_dir)

# 사용 예시
root_directory = './delete_unvalid'
validation_results = process_zip_files(root_directory)