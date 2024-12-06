import csv

def update_common_issues(input_csv, output_csv):
    common_issue_cases = {
        '60141', '60142', '60143', '60144', '60145', '60146', '60147', '60148',
        '60149', '60150', '60153', '60154', '60155', '60156', '60157', '60158',
        '60159', '60161', '60163', '60164'
    }
    
    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        csvreader = csv.reader(infile)
        csvwriter = csv.writer(outfile)
        
        # Write header
        header = next(csvreader)
        csvwriter.writerow(header)
        
        # Update rows
        for row in csvreader:
            if len(row) < len(header):
                row.extend([''] * (len(header) - len(row)))
            if row[0] in common_issue_cases:
                row[1] = '그림설명하기2 전사X'
            csvwriter.writerow(row)

# 사용 예시
input_csv = 'output.csv'
output_csv = 'updated_output.csv'
update_common_issues(input_csv, output_csv)