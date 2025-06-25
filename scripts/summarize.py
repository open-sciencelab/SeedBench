import json
import os
import pandas as pd
import argparse

task_map = {
    "1-1": "key_single_choice",
    "1-2": "key_multiple_choice",
    "1-3": "key_blank_fill",
    "1-4": "key_text_generation",
    "2-1": "prime_summary",
    "2-2": "key_info",
    "3-1": "context_single_choice",
    "3-2": "context_multiple_choice",
    "3-3": "context_blank_fill",
    "3-4": "context_text_generation",
    "3-5": "classification"
}

def map_task_type(task_type):
    """
    Map task type to task ID.
    """
    for task_id, task_name in task_map.items():
        if task_name == task_type:
            return task_id
    return None

def count_task_split_type(folder_path):
    type_count = {}
    for file in os.listdir(folder_path):
        with open(os.path.join(folder_path, file), 'r') as f:
            data = json.load(f)
        for item in data:
            split = item['split']['level1']
            task_type = item['task_type']
            if split not in type_count:
                type_count[split] = {}
            if task_type not in type_count[split]:
                type_count[split][task_type] = 0
            type_count[split][task_type] += 1
    df = pd.DataFrame(type_count)
    df.fillna(0, inplace=True)
    df['total'] = df.sum(axis=1)
    df.loc['total'] = df.sum()
    df['total'] = df['total'].astype(int)

    for col in df.columns:
        df[col] = df[col].astype(int)

    total = df.loc['total', 'total']
    df['total'] = df['total'].astype(str) + ' (' + (df['total'] / total * 100).round(2).astype(str) + '%)'
    for col in df.columns:
        if col != 'total':
            df[col] = df[col].astype(str) + ' (' + (df[col] / total * 100).round(2).astype(str) + '%)'

    df = df.reset_index().rename(columns={'index': 'task_type'})

    df['task_id'] = df['task_type'].apply(map_task_type)
    df = df[['task_id', 'task_type'] + [col for col in df.columns if col not in ['task_id', 'task_type']]]
    df = df.sort_values(by='task_id').reset_index(drop=True)

    df.to_csv('task_split_type_count.csv', encoding='utf-8-sig', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count task split types in a folder.")
    parser.add_argument('folder_path', type=str, help='Path to the folder containing JSON files.')
    args = parser.parse_args()

    count_task_split_type(args.folder_path)
 
