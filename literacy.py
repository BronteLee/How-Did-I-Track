import plotly.express as px
import pandas as pd

data = [[5523, 6.5], [2874, 5.0], [10543, 8.0], [9583, 7.0], [12843, 9.0], [8349, 5.5], [4725, 8.75]]

df = pd.DataFrame(data, columns=['Steps', 'Asleep'])
print(df)

fig = px.scatter(df, x="Asleep", y="Steps", labels={"Asleep":"Time Asleep (Hours)", "Steps": "Number of Steps"})
fig.update_traces(marker=dict(size=10, color="green"))
fig.show()