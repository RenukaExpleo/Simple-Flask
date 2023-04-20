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
        file_path = os.path.join('tmp/', file.filename)
        file.save(file_path)
        df = pd.read_csv(file_path)
        df.to_csv(file_path, index=False)
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return "Invalid file format. Please upload a CSV or Excel file."
    text_col = []
    for i in df.columns:
        if df[i].dtype == 'object':
            text_col.append(i)
    if len(text_col) > 1:
        return render_template('page1.html', text_col=text_col)
    return render_template('page1.html')

@app.route('/preview')
def previewData():
    global df
    data_head = df.head().to_html()
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    # file_path = os.path.join('tmp/', df.index.name + '.csv')
    return render_template('page1.html', data_head=data_head, n_rows=n_rows, n_cols=n_cols, text_col=text_col)

if __name__ == '__main__':
    app.run(debug=True)
