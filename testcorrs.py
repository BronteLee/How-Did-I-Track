import plotly.express as px
import pandas as pd

df = pd.read_json("data/daily-data-2.json", convert_dates=False)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)
"""
dataf = df.corr(method="spearman")
print(df.corr(method="spearman"))
dataf.loc['steps','steps']=None
dataf.loc['fairly_active_minutes']=None
print(dataf)"""
t = df[['steps', 'fairly_active_minutes', 'lightly_active_minutes',
     'calories', 'resting-heart-rate', 'minutes_asleep', 'minutes_awake']]
#t = t.corr(method="spearman")
#t.loc['fairly_active_minutes']=None
fig = px.imshow(t.corr(method="spearman"))
fig.show()