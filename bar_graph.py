import numpy as np
import plotly.graph_objects as go

def adherence_colour(df, min_wear, datatype):
    vals = df['hours_worn'].tolist()
    colours = []
    for i in vals:
        if i < min_wear and datatype != 'hours_worn':
            colours.append("orange")
        else:
            colours.append("blueviolet")
    return colours

def val_to_text(val):
    if val == "steps":
        return "Steps"
    if val == "fairly_active_minutes":
        return "Fairly Active Minutes"
    if val == "hours_worn":
        return "Hours Worn"
    else:
        return "Lightly Active Minutes"

def make_hover_text(dff, datatype):
    hover_text = []
    for i in dff.index:
        hover_text.append(f"{dff['date'][i].strftime('%a %d/%m/%Y')}<br>{val_to_text(datatype)}: {int(dff[datatype][i])}")
    return hover_text

def make_bar_graph(dff, datatype, hours_worn):
    graph_layout = go.Layout(
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0
        ), 
        height=300
    )
    graph = go.Figure(data=[go.Bar(
        x=dff['date'], y=dff[datatype if datatype != "missing_data" else "hours_worn"],
        marker_color=adherence_colour(dff, hours_worn, datatype),
        hovertemplate=("%{customdata}"),
        customdata=make_hover_text(dff, datatype if datatype != "missing_data" else "hours_worn"),
    )], layout=graph_layout)
    graph.update_xaxes(title_text="Date", title_font={"size": 16})
    graph.update_yaxes(title_text=val_to_text(datatype if datatype != "missing_data" else "hours_worn"), title_font={"size": 16})
    mean = np.mean(dff[datatype])
    graph.add_hline(y=mean, line_width=3,
                    annotation_text="Average: "+str(int(round(mean, 0))), 
                    annotation_font_size=12, annotation_bgcolor="white")
    return graph
