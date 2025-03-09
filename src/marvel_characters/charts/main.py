import os

from bokeh.document import Document
from bokeh.server.server import Server
from bokeh.themes import Theme
from jinja2 import Template
from kedro_datasets.pandas import CSVDataset

from marvel_characters.pipelines.data_processing.reporting import reporting_bokeh

# Load the HTML template
with open(os.path.join(os.path.dirname(__file__), "templates", "index.html")) as f:
    template = Template(f.read())


def modify_doc(doc: Document):
    dataset = CSVDataset(filepath="data/02_intermediate/preprocess_characters.csv")

    col_data = reporting_bokeh(preprocessed_df=dataset.load())

    # Assign template
    doc.template = template

    # Add the plot to the document
    doc.add_root(col_data)

    doc.theme = Theme(
        filename=os.path.join(os.path.dirname(__file__), "templates", "theme.yaml")
    )


# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.

server = Server({"/": modify_doc}, num_procs=1)
server.start()

if __name__ == "__main__":
    print("Opening Bokeh application on http://localhost:5006/")

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
