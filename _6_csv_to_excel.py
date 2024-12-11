import pandas as pd

def csv_to_excel(csv_file_path, excel_file_path):
    df = pd.read_csv(csv_file_path)
    # 데이터프레임을 엑셀 파일로 저장합니다.
    df.to_excel(excel_file_path, index=False)

# 사용 예시
csv_file_path = 'output_csv_xlsx/validate_eeg_output_241203_241211_2.csv'
excel_file_path = 'output_csv_xlsx/validate_eeg_output_241203_241211_2.xlsx'
csv_to_excel(csv_file_path, excel_file_path)