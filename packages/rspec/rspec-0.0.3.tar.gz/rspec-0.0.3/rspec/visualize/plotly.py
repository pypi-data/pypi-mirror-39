import plotly.graph_objs as go

def create_graph_obj(spectrum, name='Untitled', mode='lines'):
    return go.Scatter(
        name=name,
        mode=mode,
        x=spectrum['wavelength'], y=spectrum['intensity']
    )