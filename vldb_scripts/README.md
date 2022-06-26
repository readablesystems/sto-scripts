# Scripts

## Before running

It's recommended that you use a Python3 `venv` to manage the dependencies required by the scripts.
The dependencies are listed in `requirements.txt`.

You can quickly create an `venv`, activate it, and install all python dependencies by running the following commands in the root directory of this repository:

```bash
$ python3 -m venv ./venv    # This will initialize an venv in the ./venv directory
$ source venv/bin/activate  # Activate the Python3 venv
(venv)$ pip install --upgrade pip
(venv)$ pip install -r requirements.txt
```

## How to generate graphs

1. Run `./from_william.py`.
   - This will give you the necessary json result files the graph scripts can parse.
   - Be sure to run this if any results have changed or more experiments are added.
2. Run `./plotter.py` with the proper graph names. There are many graph names, refer to paper source (tex files) for the ones cited in the paper: you can find a comment line containing a "graph id" above each `\begin{figure}` command in the paper source.
3. The above command will show graph previews only. To save graphs as PDFs, use `./plotter.py -tpdf <graph_id...>`.
   - The generated filenames by default include timestamp strings. If you don't want the timestamp strings, use `./plotter.py -tpdf -n <graph_id...>` instead.

**Paper graph short cut:** Use `./paper_graphs.sh` to generate all graphs cited in the current paper without timestamp strings. Ideally after running this command you just need a simple `cp *.pdf <paper_figure_directory>` to update the graphs in the paper.
