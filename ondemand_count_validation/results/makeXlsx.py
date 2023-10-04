import pandas as pd
import re
import os

def compute_avg_difference(log_section):
    events = {}
    for line in log_section.strip().split('\n'):
        if line.startswith('===') or line.startswith('='):
            continue

        parts = line.split()
        node_number = int(parts[0][1:-1])
        epoch_number = int(parts[1][1:-1])
        event_type = parts[2][1:-1]
        time = float(parts[3][1:-1])

        key = (node_number, epoch_number, event_type)
        events[key] = time

    diffs = []
    for (node, epoch, event) in events:
        if event == 'serialization':
            key_send = (node, epoch, 'sending')
            if key_send in events:
                diffs.append(events[key_send] - events[(node, epoch, 'serialization')])
    
    if len(diffs) >= 4:
        diffs.remove(max(diffs))
        diffs.remove(min(diffs))
    
    return sum(diffs) / len(diffs) if diffs else 0

for dirpath, _, filenames in os.walk('.'):
    for file_name in filenames:
        if file_name.startswith('extract') and file_name.endswith('.result'):
            with open(os.path.join(dirpath, file_name), 'r') as file:
                log_content = file.read()

            sections = re.split("=== (.*?) ===", log_content)[1:]
            file_names = sections[::2]
            log_data = sections[1::2]
            
            avg_times = [compute_avg_difference(log) for log in log_data]

            for idx, fn in enumerate(file_names):
                file_names[idx] = int(fn.split('_')[1].split('.')[0])

            df = pd.DataFrame({
                'filename': file_names,
                'average_time': avg_times
            })

            sorted_df = df.sort_values(by='filename')

            # xlsx 파일 저장 (같은 디렉토리에)
            output_file_path = os.path.join(dirpath, file_name.replace(".result", ".xlsx"))
            sorted_df.to_excel(output_file_path, index=False)
