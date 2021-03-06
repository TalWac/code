# https://stackoverflow.com/questions/69726519/interactive-pca-with-dropdown-menu-for-the-both-axis-with-plotly-python/69733822?noredirect=1#comment123268852_69733822

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

components_df = pd.read_csv(
    "https://raw.githubusercontent.com/TalWac/stakoverflow-Qustion/main/components_df.csv"
)

labels = {
    "0": "PC 1 (22.0%)",
    "1": "PC 2 (19.6%)",
    "2": "PC 3 (11.1%)",
    "3": "PC 4 (8.2%)",
    "4": "PC 5 (3.9%)",
    "color": "Group",
}

cmap = {
    cl: px.colors.qualitative.Plotly[i]
    for i, cl in enumerate(
        components_df.groupby("Class", as_index=False).first()["Class"]
    )
}

fig1 = go.Figure(
    go.Scatter(
        x=components_df["0"],
        y=components_df["1"],
        customdata=components_df.loc[:, ["idx", "SampleID", "Class"]],
        marker_color=components_df["Class"].map(cmap),
        mode="markers",
        hovertemplate="Class=%{customdata[2]}<br>x=%{x}<br>y=%{y}<br>idx=%{customdata[0]}<br>SampleID=%{customdata[1]}<extra></extra>",
    )
).update_layout(
    template="presentation",
    xaxis_title_text=labels["0"],
    yaxis_title_text=labels["1"],
    height=700,
)

fig1.update_layout(
    updatemenus=[
        {
            "active": 0 if ax == "x" else 1,
            "buttons": [
                {
                    "label": f"{ax}-PCA{pca+1}",
                    "method": "update",
                    "args": [
                        {ax: [components_df[str(pca)]]},
                        {f"{ax}axis": {"title": {"text": labels[str(pca)]}}},
                        [0],
                    ],
                }
                for pca in range(5)
            ],
            "y": 1 if ax == "x" else 0.9,
        }
        for ax in ["x", "y"]
    ]
).update_traces(showlegend=False)

# add a legend by using synthetic traces.  NB, this will leave markers at 0,0
fig1.add_traces(
    px.scatter(
        components_df.groupby("Class", as_index=False).first(),
        x="0",
        y="1",
        color="Class",
        color_discrete_map=cmap,
    )
    .update_traces(x=[0], y=[0])
    .data
)
