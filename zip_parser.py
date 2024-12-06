import os

def rename_zip_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            parts = filename.split('_')
            if len(parts) > 2:  # 주제와 설명이 모두 포함된 경우
                case_number = parts[0]
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

# 사용 예시
directory = './8'
rename_zip_files(directory)