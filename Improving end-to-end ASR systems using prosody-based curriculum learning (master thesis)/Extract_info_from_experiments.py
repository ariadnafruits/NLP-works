import os
import pandas as pd

path = "E:/220607-compare"

col_names = ["experiment", "manifest", "audio_first", "audio_last", "wer_first", "wer_last", \
  "tgt_text_first", "tgt_text_last", "mean_delta_f0_first", "mean_delta_f0_last", "mean_delta_f0_avg", \
  "mean_delta_int_first", "mean_delta_int_last", "mean_delta_int_avg"]


df_exp = pd.DataFrame(columns = col_names)

for root,dirs,files in os.walk(path):
    for file in files:
        if file.endswith(".tsv"):
            df = pd.read_csv(os.path.join(root,file), sep='\t')
            if 'n_frames' in df.columns:
                df = df.sort_values('n_frames')
                n_frames_avg = df['n_frames'].mean()
            if 'mean_delta_f0' in df.columns:
                mean_delta_f0_avg = df['mean_delta_f0'].mean()
            if 'mean_delta_intensity' in df.columns:
                mean_delta_int_avg = df['mean_delta_intensity'].mean()
            
            row_first = df.iloc[0]
            row_last = df.iloc[-1]
            new_row_exp = {'experiment':os.path.basename(root), 'manifest':file, \
              'audio_first':row_first.get('audio'), 'audio_last':row_last.get('audio'), \
              'tgt_text_first':row_first.get('tgt_text'), 'tgt_text_last':row_last.get('tgt_text'), \
              'wer_first':row_first.get('wer'), 'wer_last':row_last.get('wer'), \
              'mean_delta_f0_first':row_first.get('mean_delta_f0'), 'mean_delta_f0_last':row_last.get('mean_delta_f0'), \
              'mean_delta_f0_avg':mean_delta_f0_avg, \
              'mean_delta_int_first':row_first.get('mean_delta_intensity'), 'mean_delta_int_last':row_last.get('mean_delta_intensity'), \
              'mean_delta_int_avg':mean_delta_int_avg, \
              'n_frames_first':row_first.get('n_frames'), 'n_frames_last':row_last.get('n_frames'), \
              'n_frames_avg':n_frames_avg \
              }
            #print(new_row_exp)
            df_exp = df_exp.append(new_row_exp, ignore_index=True)
        

df_exp.to_csv('experiments.csv', sep='\t')
            
