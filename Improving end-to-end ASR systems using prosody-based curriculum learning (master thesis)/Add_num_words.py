import pandas as pd
import os

def count_words(sentence):
    n_words = sentence.apply(lambda x: len(str(x).split(' ')))
    return n_words


data = "data/df_merged_2022-03-16T231811.tsv-Absolute_values.tsv"

print(os.path.basename(data))

df = pd.read_csv(data, sep='\t')

df['n_words'] = count_words(df['tgt_text'])

df.to_csv('data/' + os.path.basename(data) + '+Num_words.tsv', sep='\t', index=False)

