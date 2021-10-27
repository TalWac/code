import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


components_df = pd.read_csv(
    "https://raw.githubusercontent.com/TalWac/stakoverflow-Qustion/main/components_df.csv"
)

fig1 = go.Figure(
    go.Scatter(
        x=components_df["0"],
        y=components_df["1"],
        
        customdata=components_df.loc[:, ["idx", "SampleID", "Class"]],
        marker_color=components_df["Class"].map(
            {"After": "#1F77B4", "Before": "#FF7F0E", "QC": "#2CA02C"}
        ),
        
        mode="markers",
        hovertemplate="Class=%{customdata[2]}<br>x=%{x}<br>y=%{y}<br>idx=%{customdata[0]}<br>SampleID=%{customdata[1]}<extra></extra>",
    )
).update_layout(
    template="presentation",
    xaxis_title_text=labels["0"],
#     color=components_df['Class'],
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
                        {
                            ax: [components_df[str(pca)]],
                        },
                        {f"{ax}axis": {"title": {"text": labels[str(pca)]}}},
                    ],
                }
                for pca in range(5)
            ],
            "y": 1 if ax == "x" else 0.9,
        }
        for ax in ["x", "y"]
    ]
)
