from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.express as px
import pandas as pd
import json
import sys


# cons
no_red = 3

# labels
pc1 = 'pc1'
pc2 = 'pc2'
pc3 = 'pc3'


# config
data_str = 'data'
columns_str = 'columns'
label_str = 'label'
method_str = 'method'
out_file_str = 'output_csv'
default_op_csv = 'dim_reduction_out.csv'


conf_file = sys.argv[1]

with open(conf_file) as f:
    in_data = dict(json.load(f))


# available methods
avail_methods = ['pca', 'tsne']
if in_data[method_str] not in avail_methods:
    sys.exit('Not available method : ' + in_data[method_str])


data = pd.read_csv(in_data[data_str])
result_df = pd.DataFrame()
red_method = None

if in_data[method_str] is 'pca' :
    red_method = PCA
else:
    red_method = TSNE

red_method = red_method(n_components=no_red)
result = red_method.fit_transform(data[in_data.get(columns_str)])
result_df = pd.DataFrame(result, columns=[pc1, pc2, pc3])

label_col = in_data[label_str]
result_df[label_col] = data[label_col]


if out_file_str in in_data.keys():
    default_op_csv = in_data[out_file_str]

result_df.to_csv(default_op_csv)
fig = px.scatter_3d(result_df, x=pc1, y=pc2, z=pc3, color=label_col, title='Dim Reduction')
fig.show()
