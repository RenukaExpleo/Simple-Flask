import pandas as pd
from flask import *
import os
import stat
import tempfile
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
import seaborn as sns

app = Flask(__name__)

global df
global selected_columns
global text_col
text_col = []

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def uploadFile():
    global df
    global text_col
    file = request.files['file']
    if file.filename.endswith('.csv'):
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as tmp:
            file.save(tmp.name)
            df = pd.read_csv(tmp.name)
            text_col = [i for i in df.columns if df[i].dtype == 'object']
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        text_col = [i for i in df.columns if df[i].dtype == 'object']
    else:
        return "Invalid file format. Please upload a CSV or Excel file."
    return render_template('page1.html', text_col=text_col)

@app.route('/preview')
def previewData():
    # global text_col
    df = pd.read_csv('tmp/'+'HousingData.csv')
    data_head = df.head().to_html()
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    return render_template('page1.html', data_head=data_head, n_rows=n_rows, n_cols=n_cols, text_col=text_col)

@app.route('/drop_col', methods=['POST'])
def drop_column():
    column_name = request.form['column_name']
    global df  # Use the global DataFrame
    # global up_df
    df = df.drop(columns=column_name)
    return render_template('page1.html', df=df.head().to_html(justify='left'))


@app.route('/info')
def info():
    # global df 
    global null_count
    df = pd.read_csv('tmp/'+'HousingData.csv')
    data_types = df.dtypes.reset_index()
    data_types.columns = ['Column Name', 'Data Type']
    non_null_count = df.count().reset_index()
    non_null_count.columns = ['Column Name', 'Non-Null Count']
    null_count = df.isnull().sum().reset_index()
    null_count.columns = ['Column Name', 'Null Count']
    data_types = pd.merge(data_types, non_null_count, on='Column Name')
    data_types = pd.merge(data_types, null_count, on='Column Name')
    
    d_types = df.dtypes.unique()
    df_types = pd.DataFrame({"Data types":d_types}).to_html()
    df_new = pd.DataFrame({'Total Rows': [len(df)], 'Total Columns': [len(df.columns)]})
    
    return render_template('page1.html', data=data_types.to_html(index=False, justify='left'), total=df_new.to_html(index=False, justify='left'),d_types=d_types)

@app.route('/show_describe')
def showDes():
    df = pd.read_csv('tmp/'+'HousingData.csv')
    uploaded_df=df.describe()
    uploaded_df_html =uploaded_df.to_html(justify='left')
    return render_template('page1.html', data_des = uploaded_df_html)

@app.route('/showCorr')
def showCorr():
    df = 'tmp/HousingData.csv'
    if os.path.isfile(df):
        df = pd.read_csv(df)
        corr_matrix = df.corr()
        corr_matrix_html = corr_matrix.to_html(justify='left')
        plt.figure(figsize=(10,10))
        sns.heatmap(corr_matrix, annot=True)
        plt_file = "static/img3.png"
        plt.savefig(plt_file)
        return render_template('page1.html', data_corr=corr_matrix_html, heatmap=plt_file)
    else:
        return 'Error: CSV file not found'

# @app.route('/histogram')
# def histogram():
#     # global df
#     df = pd.read_csv('tmp/'+'HousingData.csv')
#     df=df

#     num_rows = (len(df.columns) + 2) // 3  # Calculate the number of rows needed
#     fig, axes = plt.subplots(nrows=num_rows, ncols=3, figsize=(10,15))
#     extra_graphs = num_rows * 3 - len(df.columns)
#     # Create a boxplot for each column in the DataFrame
#     for i, col in enumerate(df.columns):
#         sns.histplot(data=df, x=col, ax=axes[i // 3, i % 3])
    
#     for j in range(1, extra_graphs+1):
#         fig.delaxes(axes[num_rows-1][-j])

#     plt.suptitle('Histogram For Data Frame')
#     file = "static/img4.png"
#     plt.savefig(file) 
#     # return the image file 
#     plt.tight_layout()    
#     return render_template('visualization.html', histplot_url = file)


# @app.route('/back')
# def back():

#     return render_template('page1.html')


if __name__ == '__main__':
    app.run(debug=True)
