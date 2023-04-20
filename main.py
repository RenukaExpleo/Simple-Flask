from flask import *
import pandas as pd

app = Flask(__name__)

global df
global text_col
global selected_columns

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def uploadFile():
    global text_col
    global df
    global selected_columns
    file = request.files['file']
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        return "Invalid file format. Please upload a CSV or Excel file."
    selected_columns = []
    text_col = []
    for i in df.columns:
        if df[i].dtype == 'object':
            text_col.append(i)
    if len(text_col)>1:
        return render_template('page1.html', text_col=text_col)    

    return render_template('page1.html')

@app.route('/preview')
def previewData():
    global df
    data_head =df.head().to_html(justify='left')
    n_rows = df.shape[0]
    n_cols = df.shape[1]
    return render_template('page1.html', data_head = data_head, n_rows=n_rows, n_cols=n_cols)
    # return "preview data"

if __name__ == '__main__':  
    app.run(debug=True)