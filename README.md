# STO Scripts

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

1. Update `legend.py` and `config.py` with the appropriate values
  - `legend.py` needs to be updated with the prefixes of the experiment data (e.g. `prefix_...` or `prefix-...`) and all related mappings
  - `legend.py` also needs to be updated with plotting-related configurations, such as colors, line styles, and markers
  - `config.py` needs to be updated with preconfigured bundles. This is mostly a quality-of-life thing that allows for shorter arguments to `plotter.py`, but isn't at all necessary
2. Run `parser.py` (see all options with `./parser.py -h`)
3. Run `plotter.py` (see all options with `./plotter.py -h`)
4. Generated graphs will be in `figs/`
