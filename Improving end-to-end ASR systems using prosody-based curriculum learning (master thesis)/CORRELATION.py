import pandas as pd
import scipy.stats
from scipy import stats

data_path = "data/df_merged_2022-03-05T193240.tsv"
df = pd.read_csv(data_path, sep='\t') 

print(df.columns)

features = ['n_frames', 'mean_f0', 'stdev_f0', 'mean_delta_f0', 'stdev_delta_f0', 'mean_delta_intensity', 'stdev_delta_intensity', 'hnr', 'local_jitter', 'local_absolute_jitter', 'rap_jitter', 'ppq5_jitter', 'ddp_jitter', 'local_shimmer', 'localdb_shimmer', 'apq3_shimmer', 'aqpq5_shimmer', 'apq11_shimmer', 'dda_shimmer']


print("feature", "\t", "correlation", "\t", "p_value", "\t", "slope", "\t", "intercept", "\t", "r", "\t", "p", "\t", "std_err")

for feature in features:
    correlation, p_value = scipy.stats.pearsonr(df['wer'], abs(df[feature]))
    slope, intercept, r, p, std_err = stats.linregress(df['wer'], df[feature])
    print(feature, "\t", correlation, "\t", p_value, "\t", slope, "\t", intercept, "\t", r, "\t", p, "\t", std_err)




