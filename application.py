import pyodbc
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template
app = Flask(__name__)

def fetch_cloud_data():
    server = 'visualizationserver.database.windows.net'
    database = 'visualization_data'
    username = 'hmtd1992'
    password = 'Hmtd@1992'
    driver = '{ODBC Driver 17 for SQL Server}'
    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor.execute("SELECT TOP (1000) * FROM [dbo].[visualization_points]")
    row = cursor.fetchone()
    x=[]
    y=[]
    while row:
        x.append(row[0])
        y.append(row[1])
        row = cursor.fetchone()
    return x,y

def create_figure(x,y):
    p = figure(plot_width=600, plot_height=600,
               title='Sample Bokeh Graph',
               x_axis_label='X', y_axis_label='Y')
    p.square(x, y, size=12, color='navy', alpha=0.6)
    return p

# Index page
@app.route('/')
def index():
    x = []
    y = []
    x,y=fetch_cloud_data()
    my_figure = create_figure(x, y)

    # Embed plot into HTML via Flask Render
    script, div = components(my_figure)
    return render_template("visualization.html", script=script, div=div)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)



