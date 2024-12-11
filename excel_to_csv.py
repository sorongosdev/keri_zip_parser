import pandas as pd

def excel_to_csv(excel_file_path, csv_file_path):
    # 엑셀 파일을 읽습니다.
    df = pd.read_excel(excel_file_path)
    
    # 데이터프레임을 CSV 파일로 저장합니다.
    df.to_csv(csv_file_path, index=False)

# 사용 예시
excel_file_path = 'eeg_memo_custom_2csv_src.xlsx'
csv_file_path = 'eeg_memo_custom_2csv_dist.csv'
excel_to_csv(excel_file_path, csv_file_path)