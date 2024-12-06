import os
import zipfile

def process_zip_files(directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            new_zip_name = f"{os.path.splitext(filename)[0]}_E.zip"
            new_zip_path = os.path.join(output_directory, new_zip_name)

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
                            temp_zip.writestr(item, zip_ref.read(item.filename))

            # Replace the original zip file with the temporary zip file
            os.remove(zip_path)
            os.rename(temp_zip_path, zip_path)
            print(f'Processed: {zip_path} -> {new_zip_path}')

# 사용 예시
directory = './8'
output_directory = './8_E'
process_zip_files(directory, output_directory)