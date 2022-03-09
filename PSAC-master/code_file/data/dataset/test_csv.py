import csv
import pandas as pd
with open('/mnt/project_vqa_2/PSAC-master1.0/code_file/data/dataset/Train_action_question.csv','rt', encoding='utf-8')as csvfile:
    reader = csv.DictReader(csvfile,fieldnames=('gif_name', 'question', 'a1','a2','a3','a4','a5','answer','vid_id','key'),delimiter='\t')
    for row in reader:
        if row.get('key')=='101969':
                print(row)


