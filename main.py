# import pandas as pd
# from flask import *
# import os
# import stat

# app = Flask(__name__)

# global df
# global selected_columns
# global text_col

# @app.route('/') 
# def index():
#     return render_template("index.html")

# @app.route('/', methods = ['POST'])
# def uploadFile():
#     global text_col
#     file = request.files['file']
#     if file.filename.endswith('.csv'):
#         file_path = os.path.join('tmp/', file.filename)
#         # file.save(file_path)
#         df = pd.read_csv(file_path)
#         df.to_csv(file_path, index=False)
#         os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        
#     elif file.filename.endswith('.xlsx'):
#         df = pd.read_excel(file)
#     else:
#         return "Invalid file format. Please upload a CSV or Excel file."
#     text_col = []
#     for i in df.columns:
#         if df[i].dtype == 'object':
#             text_col.append(i)
#     if len(text_col)>1:
#         return render_template('page1.html', text_col=text_col) 
#     return render_template('page1.html')


# @app.route('/preview')
# def previewData():
# # global text_col
#    df = pd.read_csv('tmp/'+'HousingData.csv')
#    data_head =df.head().to_html()
#    n_rows = df.shape[0]
#    n_cols = df.shape[1]
#    return render_template('page1.html', data_head = data_head, n_rows=n_rows, n_cols=n_cols, text_col=text_col)

# if __name__ == '__main__':  
#     app.run(debug=True)
import pandas as pd
from flask import *
import os
import stat
import tempfile

app = Flask(__name__)

global df
global selected_columns
global text_col

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
    global df
    data_head = df.head().to_html()
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    # file_path = os.path.join('tmp/', df.index.name + '.csv')
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
    global df 
    global null_count
    
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


if __name__ == '__main__':
    app.run(debug=True)
