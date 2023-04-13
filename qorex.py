from dataclasses import dataclass
from dash import Dash, dash_table, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import click
import os

@dataclass
class Metric:
    name: str
    rename: str = None
    reverse: bool = False
    derive: callable = None

@dataclass
class Group:
    name: str
    metrics: list[Metric]
    is_run_search: bool = False
    is_hidden: bool = False

@dataclass
class Config:
    groups: list[Group]

    def run_info_metric_names(self) -> list[str]:
        run_info_metric_names = []
        for group in self.groups:
            if group.is_run_search:
                for metric in group.metrics:
                    run_info_metric_names.append(metric.name)
        return run_info_metric_names

    def reverse_metrics(self)  -> list[str]:
        reverse_metrics = []
        for group in self.groups:
            for metric in group.metrics:
                if metric.reverse:
                    reverse_metrics.append(metric.name)
        return reverse_metrics

    def key_name_map(self)  -> dict[str,str]:
        name_map = {}
        for group in self.groups:
            for metric in group.metrics:
                if metric.rename:
                    name_map[metric.name] = metric.rename
        return name_map
    
    def all_group_metrics(self) -> list[Metric]:
        metrics = []
        for group in self.groups:
            for metric in group.metrics:
                metrics.append(metric)
        return metrics
    
    def derived_metrics(self) -> list[Metric]:
        return [metric for metric in self.all_group_metrics() if metric.derive is not None]

def start_server(csv: str, config: Config, debug: bool = False):

    df = pd.read_csv(csv)
    
    for metric in config.derived_metrics():
        df = df.assign(**{metric.name:metric.derive})

    app = Dash(title="QOR Explorer", external_stylesheets=[dbc.themes.BOOTSTRAP])

    non_hidden_group_names = [group.name for group in config.groups if not group.is_hidden]

    metric_names_by_group = {}
    for group in config.groups:
        metric_names_by_group[group.name] = [metric.name for metric in group.metrics]

    reverse_metrics = config.reverse_metrics()

    name_map = config.key_name_map()

    app.layout = dbc.Container(
        html.Div(
            [
                html.Br(),
                html.H1("QOR EXPLORER", style={"font-size": "4em", "color": " #0a4172"}),
                html.H6("BY VERIEST", style={"margin-left": "0.5em"}),
                html.Br(),
                dash_table.DataTable(
                    id="select-run-table",
                    columns=[
                        {"name": i, "id": i} for i in df.columns if i in  config.run_info_metric_names()
                    ],
                    data=df.sort_values(by=["Timestamp"], ascending=False).to_dict(
                        "records"
                    ),
                    filter_action="native",
                    row_selectable="multi",
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                    page_size=10,
                ),
                html.Br(),
                dbc.Form(group_selectors(non_hidden_group_names)),
                html.Br(),
                html.Div(id="comparison-results-container"),
            ]
        ),
        fluid=True,
    )

    @app.callback(
        Output("comparison-results-container", "children"),
        Input("select-run-table", "derived_virtual_data"),
        Input("select-run-table", "derived_virtual_selected_rows"),
        Input("switches-input", "value"),
    )
    def update_comparison(rows, derived_virtual_selected_rows, group_selector_value):
        if derived_virtual_selected_rows is None:
            derived_virtual_selected_rows = []

        # Select rows
        selected_rows = [rows[i] for i in derived_virtual_selected_rows]

        # Show a message if no rows are selected
        if len(selected_rows) == 0:
            return dbc.Alert(
                "Select rows in the table above, to compare results", color="primary"
            )

        # Figure out which keys to show
        selected_keys = []
        for i, n in enumerate(non_hidden_group_names):
            if n == "Hidden":
                continue
            if -1 in group_selector_value or i in group_selector_value:
                for key in metric_names_by_group[n]:
                    if key not in selected_keys:
                        selected_keys.append(key)

        comparison_data = []
        for key in selected_keys:
            comparison_row = []
            comparison_row.append(key)
            for i, row in enumerate(selected_rows):
                if key in row.keys():
                    comparison_row.append(row[key])
                else:
                    comparison_row.append("")

            comparison_data.append(comparison_row)

        comparison_table = []
        for row in comparison_data:
            table_row = []
            base_value = None
            key = None
            for i, cell in enumerate(row):
                styled_cell = html.Div(
                    cell, style={"text-align":"center", "font-size": "1.5em", "min-width": "100px"}
                )

                if i == 0:
                    # Key name
                    key = cell
                    if cell in name_map.keys():
                        cell = name_map[cell]
                    table_row.append(html.Th(cell))
                elif i == 1:
                    # Base column
                    base_value = convert_str(cell)
                    if type(base_value) == str or base_value is None:
                        table_row.append(html.Td(cell))
                    else:
                        table_row.append(html.Td(styled_cell))
                else:
                    # Compare to base column
                    value = convert_str(cell)
                    if type(value) == str or value is None:
                        table_row.append(html.Td(cell))
                    else:
                        delta = round(value - base_value)

                        if (delta > 0 and key not in reverse_metrics) or (delta < 0 and key in reverse_metrics):
                            cell_style = {"color":"#f00"}
                        else:
                            cell_style = {}

                        if base_value != 0:
                            pct = abs(round(delta * 100 / base_value))
                        else:
                            pct = "Inf"
                        
                        if abs(delta) >= 1000:
                            suffix = "k"
                            delta = round(delta / 1000.0)
                        else:
                            suffix = ""

                        delta_s = str(delta) + suffix
                        if not delta_s.startswith("-"):
                            delta_s = f"+{delta_s}"

                        fancy_cell = [
                            styled_cell,
                            html.Div(f"{pct}%", style={"float":"right","color": "#888"}),
                            html.Div(f"{delta_s}", style={"color": "#888"}),
                        ]
                        table_row.append(html.Td(fancy_cell, style=cell_style))

            comparison_table.append(html.Tr(table_row))

        return [
            dbc.Table(
                html.Tbody(comparison_table),
                bordered=True,
                hover=True,
                responsive=True,
                style={"width": "auto"},
            )
        ]
    app.run_server(debug=debug)

def group_selectors(group_names):
    options = []
    for i, n in enumerate(group_names):
        if n == "Hidden":
            continue
        options.append({"label": n, "value": i})

    return dbc.Checklist(
        options=options, value=[1], id="switches-input", switch=True, inline=True
    )

def convert_str(s: str) -> any:
    try:
        if s.endswith("%"):
            s = s.removesuffix("%")

        f = float(s)
        i = int(f)
        if f == i:
            return i
        else:
            return f
    except:
        return s

@click.command()
@click.option('--csv', help='Name of CSV file to read')
@click.option('--config', help='Name of config file to read')
@click.option('--debug', is_flag=True, default=False, help='Run server in debug mode')
def cli(csv, config, debug):
    config_file = os.path.splitext(config)[0]
    try:
        config_module = __import__(config_file)
    except ImportError:
        print(f'Error: could not import configuration from {config_file}.py')
        return
    config_data = getattr(config_module, f'CONFIG', None)
    if not config_data:
        print(f'Error: {config_file}.py does not define a CONFIG variable')
        return

    start_server(csv, config_data, debug)

if __name__ == "__main__":
    cli()
