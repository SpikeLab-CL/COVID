import json
import plotly.graph_objs as go

red = "#E07182"
green = "#96D6B4"
blue = "#4487D3"
grey = "#87878A"


def send_parameters_to_r(file_name: str, parameters: dict) -> None:
    """
    Collects relevant parameters and sends them to r as a json
    """
    with open(file_name, "w") as outfile:
        json.dump(parameters, outfile)
        
        
def plot_statistics(data, lower_col="cum.effect.lower", upper_col='cum.effect.upper', mean_col='cum.effect', 
                    index_col="date", dashed_col=None, show_legend=False,
                    xaxis_title='Date', yaxis_title='Sales', title=None, name='Mean effect'):


    color_lower_upper_marker = "#C7405A"
    color_fillbetween = 'rgba(88, 44, 51, 0.3)'
    color_lower_upper_marker = color_fillbetween#"#C7405A"
    color_median = red
    fig_list = [
    go.Scatter(
        name=name,
        x=data[index_col],
        y=data[mean_col],
        mode='lines',
        line=dict(color=color_median),
        showlegend=show_legend,

    ),
        
    go.Scatter(
        name=f'Upper effect',
        x=data[index_col],
        y=data[upper_col],
        mode='lines',
        marker=dict(color=color_lower_upper_marker),
        line=dict(width=0),
        showlegend=False
    ),
    go.Scatter(
        name=f'Lower effect',
        x=data[index_col],
        y=data[lower_col],
        marker=dict(color=color_lower_upper_marker),
        line=dict(width=0),
        mode='lines',
        fillcolor=color_fillbetween,
        fill='tonexty',
        showlegend=False
    )
    ]
    
    if dashed_col is not None:
        dashed_fig = go.Scatter(
            name='Actual',
            x=data[index_col],
            y=data[dashed_col],
            mode='lines',
            line=dict(color='black', dash='dash'),
            showlegend=show_legend,    
        )
        fig_list = [dashed_fig] + fig_list
        
    fig = go.Figure(fig_list)

    fig.update_layout(
        yaxis=dict(title=yaxis_title, showgrid=False),
        xaxis=dict(title=xaxis_title, showgrid=False),
        title=title,
        hovermode="x",
        paper_bgcolor='white',
        plot_bgcolor='white',
        hoverlabel_align = 'right',
        #margin=dict(l=50, r=50, t=50, b=50)
    )
    
    return fig
            