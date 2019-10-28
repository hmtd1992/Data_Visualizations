import pyodbc
from bokeh.plotting import figure
from bokeh.embed import components
from flask import Flask, render_template
from bokeh.server.server import Server
app = Flask(__name__)

# Index page
@app.route('/')
def index():
    x = []
    y = []
    
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
        
    p = figure(plot_width=600, plot_height=600,
               title='Sample Bokeh Graph',
               x_axis_label='X', y_axis_label='Y')
    p.square(x, y, size=12, color='navy', alpha=0.6)
    
    # Embed plot into HTML via Flask Render
    script, div = components(p)
    server.start()
    return render_template("visualization.html", script=script, div=div)


