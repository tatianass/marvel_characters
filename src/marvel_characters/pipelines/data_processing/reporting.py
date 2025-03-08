import numpy as np
import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import (
    ColumnDataSource,
    DataTable,
    HoverTool,
    InlineStyleSheet,
    IntEditor,
    LinearColorMapper,
    Select,
    SelectEditor,
    StringFormatter,
    TableColumn,
)
from bokeh.models.layouts import Column
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
from bokeh.transform import transform

# Define dynamic table info
SIZES = list(range(3, 30, 3))
COLORS = Viridis256
N_SIZES = len(SIZES)
N_COLORS = len(COLORS)


def create_data_table(input_data, name):
    """Create data table with edit and sortable data."""
    table_cols = [
        TableColumn(
            field="name",
            title="Name",
            editor=SelectEditor(options=name),
            formatter=StringFormatter(font_style="bold"),
        ),
        TableColumn(
            field="total_comics_in_num", title="Total Comics", editor=IntEditor()
        ),
        TableColumn(field="modified", title="Modified", editor=IntEditor()),
        TableColumn(
            field="total_series_in_num", title="Total Series", editor=IntEditor()
        ),
        TableColumn(
            field="total_stories_in_num", title="Total Stories", editor=IntEditor()
        ),
        TableColumn(
            field="total_events_in_num", title="Total Events", editor=IntEditor()
        ),
        TableColumn(field="id", title="Id", editor=IntEditor()),
    ]
    tb_stylesheet_slick = InlineStyleSheet(
        css=".slick-row { background-color: #393939; }"
    )
    tb_stylesheet_selected = InlineStyleSheet(
        css=".slick-cell.selected {background-color: #897e94;}"
    )
    data_table = DataTable(
        width=700,
        height=400,
        source=input_data,
        columns=table_cols,
        editable=True,
        index_position=-1,
        index_header="#",
        index_width=60,
        selectable=True,
        scroll_to_selection=True,
        stylesheets=[tb_stylesheet_slick, tb_stylesheet_selected],
    )

    return data_table


def create_comic_chart(input_data, mapper):
    """Create scatter plot with comic information only"""
    comic_p = figure(
        title="Total Comics Distribution",
        width=700,
        height=400,
        tools="pan,box_zoom,hover,reset",
        active_drag="pan",
    )

    total_comics_in_num = comic_p.scatter(
        x="id",
        y="total_comics_in_num",
        fill_color=transform("total_comics_in_num", mapper),
        size=8,
        alpha=0.5,
        source=input_data,
    )

    comic_p.xaxis.axis_label = "Id"
    comic_p.yaxis.axis_label = "Total Comics"

    tooltips = [
        ("Name", "@name"),
        ("Total Comics", "@total_comics_in_num"),
        ("Modified", "@modified"),
        ("Id", "@id"),
        ("Total Series", "@total_series_in_num"),
        ("Total Stories", "@total_stories_in_num"),
        ("Total Events", "@total_events_in_num"),
    ]
    comics_hover_tool = HoverTool(
        renderers=[total_comics_in_num],
        tooltips=[*tooltips, ("Total Comics", "@total_comics_in_num")],
    )

    comic_p.add_tools(comics_hover_tool)

    return comic_p


def comic_dashboard(df: pd.DataFrame):
    source = ColumnDataSource(df)

    colors = Viridis256
    mapper = LinearColorMapper(
        palette=colors,
        low=df.total_comics_in_num.min(),
        high=df.total_comics_in_num.max(),
    )

    name = sorted(df["name"].unique())

    # Add columns
    scatter_chart_comics = column(create_comic_chart(input_data=source, mapper=mapper))
    table_chart = column(create_data_table(input_data=source, name=name))

    dashboard = row(scatter_chart_comics, table_chart)
    return dashboard


def comparison_dashboard(df: pd.DataFrame):
    """Creating comparison dashboard based on: https://github.com/bokeh/bokeh/blob/branch-3.8/examples/server/app/crossfilter/main.py"""
    # Adjust column values
    columns = sorted(df.columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]

    # Adding variables
    x = Select(title="X-Axis", value="total_series_in_num", options=columns)
    y = Select(title="Y-Axis", value="total_stories_in_num", options=columns)
    size = Select(
        title="Size", value="total_comics_in_num", options=["None", *continuous]
    )
    color = Select(title="Color", value="id", options=["None", *continuous])

    def create_marvel_comparison_chart():
        """Create comparison for the different count variables."""
        xs = df[x.value].values
        ys = df[y.value].values
        x_title = x.value.title()
        y_title = y.value.title()

        kw = dict()
        if x.value in discrete:
            kw["x_range"] = sorted(set(xs))
        if y.value in discrete:
            kw["y_range"] = sorted(set(ys))
        kw["title"] = f"{x_title} vs {y_title}"

        p = figure(width=700, height=400, tools="pan,box_zoom,hover,reset", **kw)
        p.xaxis.axis_label = x_title
        p.yaxis.axis_label = y_title

        if x.value in discrete:
            p.xaxis.major_label_orientation = np.pi / 4

        sz = 9
        if size.value != "None":
            if len(set(df[size.value])) > N_SIZES:
                groups = pd.qcut(df[size.value].values, N_SIZES, duplicates="drop")
            else:
                groups = pd.Categorical(df[size.value])
            sz = [SIZES[xx] for xx in groups.codes]

        c = "#31AADE"
        if color.value != "None":
            if len(set(df[color.value])) > N_COLORS:
                groups = pd.qcut(df[color.value].values, N_COLORS, duplicates="drop")
            else:
                groups = pd.Categorical(df[color.value])
            c = [COLORS[xx] for xx in groups.codes]

        p.scatter(
            x=xs,
            y=ys,
            color=c,
            size=sz,
            line_color="white",
            alpha=0.6,
            hover_color="white",
            hover_alpha=0.5,
        )

        return p

    def update_marvel_comparison_chart(attr, old, new):
        """Update comparison table."""
        layout_comparison.children[1] = create_marvel_comparison_chart()

    ct_stylesheet_slick = InlineStyleSheet(
        css=".bk-input { background-color: #393939; }"
    )
    controls = row(x, y, color, size, width=200, stylesheets=[ct_stylesheet_slick])
    layout_comparison = column(controls, create_marvel_comparison_chart())

    # Adding update functions
    x.on_change("value", update_marvel_comparison_chart)
    y.on_change("value", update_marvel_comparison_chart)
    size.on_change("value", update_marvel_comparison_chart)
    color.on_change("value", update_marvel_comparison_chart)

    return layout_comparison


def reporting(preprocessed_df) -> Column:
    # Load data

    preprocessed_df["modified"] = pd.to_datetime(preprocessed_df["modified"]).dt.year
    preprocessed_df = preprocessed_df.sort_values(
        "total_comics_in_num", ascending=False
    )

    comic = comic_dashboard(df=preprocessed_df)
    comparison = comparison_dashboard(df=preprocessed_df)

    return column(comic, comparison)
