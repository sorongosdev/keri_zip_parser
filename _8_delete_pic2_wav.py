import os
import zipfile

# 삭제할 증례번호 목록
target_cases = {
    "60141", "60142", "60143", "60144", "60145", "60146", "60147", "60148",
    "60149", "60150", "60153", "60154", "60155", "60156", "60157", "60158",
    "60159", "60161", "60163", "60164"
}

def delete_wav_files(root_directory):
    for date_folder in os.listdir(root_directory):
        date_folder_path = os.path.join(root_directory, date_folder)
        if os.path.isdir(date_folder_path):
            for case_folder in os.listdir(date_folder_path):
                if case_folder in target_cases:
                    case_folder_path = os.path.join(date_folder_path, case_folder)
                    if os.path.isdir(case_folder_path):
                        for file_name in os.listdir(case_folder_path):
                            if file_name.endswith('.zip') and '그림_설명하기' in file_name:
                                zip_path = os.path.join(case_folder_path, file_name)
                                delete_wav_from_zip(zip_path)

def delete_wav_from_zip(zip_path):
    temp_dir = os.path.join(os.path.dirname(zip_path), 'temp_unzip')
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Delete wav files ending with '_2.wav'
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.endswith('_2.wav'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
    
    # Recreate the zip file without the deleted wav files
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
root_directory = 'delete_pic2'
delete_wav_files(root_directory)