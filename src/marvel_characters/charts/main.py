from bokeh.server.server import Server
from bokeh.themes import Theme
from kedro_datasets.pandas import CSVDataset

from marvel_characters.pipelines.data_processing.reporting import reporting


def modify_doc(doc):
    dataset = CSVDataset(filepath="data/02_intermediate/preprocess_characters.csv")

    col_data = reporting(preprocessed_df=dataset.load())

    doc.add_root(col_data)

    doc.theme = Theme(filename="theme.yaml")


# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.
server = Server({"/": modify_doc}, num_procs=1)
server.start()

if __name__ == "__main__":
    print("Opening Bokeh application on http://localhost:5006/")

    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
