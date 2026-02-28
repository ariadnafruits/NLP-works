import matplotlib.pyplot as plt
import pandas as pd
pd.get_option("display.max_columns", 200)
from datetime import datetime

manifest1 = "data/sorted_manifest.tsv"
manifest2 = "data/train-clean-100_wav.tsv"

df1 = pd.read_csv(manifest1, sep='\t')
df2 = pd.read_csv(manifest2, sep='\t')

print("\ndf1\n", df1.head())
print("\ndf2\n", df2.head())

'''
for i in range(len(df2)):
    df2['id'][i] = df2['id'][i].split("-")
    df2['id'][i] = df2['id'][i][3:]
    df2['id'][i] = list(map(int, df2['id'][i]))
    df2['id'][i] = list(map(str, df2['id'][i]))
    df2['id'][i] = '-'.join(df2['id'][i])

print("\ndf2______________\n", df2.head())
'''

df_merged = pd.merge(df1, df2, how="inner", on="id", suffixes=("_1", "_2"), copy=True, indicator=True, validate="one_to_one")


df_merged['tgt_text_len'] = df_merged['tgt_text_1'].str.len()
df_merged['mean_wer'] = df_merged['wer'] / df_merged['tgt_text_len']


now=datetime.now()
file_name = 'df_merged_' + now.strftime("%FT%H%M%S") + '.tsv'

df_merged.to_csv('data/' + file_name, sep='\t', index=False)

print("\ndf_merged______________\n", df_merged.head())

#df_merged.plot(x='id', y='mean_f0')


#df_merged.plot(subplots=True, layout=(15,2))

#fig, axes = plt.subplots(11,2,figsize=(15,30))
#df_merged.plot(subplots=True, ax=axes, x='wer', linestyle="none", marker='.')

x_axe = 'mean_wer'
y_axe = ['mean_f0', 'stdev_f0', 'mean_delta_f0', 'stdev_delta_f0', 'mean_delta_intensity', 'stdev_delta_intensity', 'hnr', 'local_jitter', 'local_absolute_jitter', 'rap_jitter', 'ppq5_jitter', 'ddp_jitter', 'local_shimmer', 'localdb_shimmer', 'apq3_shimmer', 'aqpq5_shimmer', 'apq11_shimmer', 'dda_shimmer']
colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'chocolate', 'gold', 'crimson', 'cadetblue', 'slategray', 'brown', 'fuchsia', 'deepskyblue']


for i in range(len(y_axe)):
    plt.plot(df_merged[x_axe], df_merged[y_axe[i]], marker='.', markersize=1, linestyle="none", color=colors[i])
    plt.xlabel(x_axe)
    plt.ylabel(y_axe[i])
    plt.savefig(y_axe[i] + '.png')
    plt.show()

df_low_wer = df_merged[df_merged['mean_wer'] < 3]

for i in range(len(y_axe)):
    plt.plot(df_low_wer[x_axe], df_low_wer[y_axe[i]], marker='.', markersize=1, linestyle="none", color=colors[i])
    plt.xlabel(x_axe)
    plt.ylabel(y_axe[i])
    plt.savefig(y_axe[i] + '-low_wer.png')
    plt.show()

df_merged.corr().to_csv('data/corr_' + file_name, sep='\t', index=False)
