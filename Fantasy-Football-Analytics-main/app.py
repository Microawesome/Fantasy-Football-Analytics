from markupsafe import string
import pandas as pd
import requests
import numpy as np
from flask import Flask, request, render_template, session, redirect

pd.options.display.max_columns=None
app = Flask(__name__)

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'

r = requests.get(url)  

json = r.json()

json.keys()

df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])

value_df = df[['web_name','team',]]

value_df['id'] = df.team.astype(float)

value_df['value'] = df.value_season.astype(float)

team_value_df =pd.merge(value_df, teams_df)

df3 = team_value_df[['web_name','name','value']]

value_ten_df = df3.sort_values('value',ascending=False).head(10)


selected_by_df = df[['web_name','team','selected_by_percent']]

selected_by_10_df = selected_by_df.sort_values('selected_by_percent',ascending=False).head(10)

@app.route('/', methods=("POST", "GET"))
def table():

    return render_template('index.html',  tables=[value_ten_df.to_html(classes='data')], titles=value_ten_df.columns.values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
