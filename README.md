# Galaxy cluster interactive plots

This small Dash app is used to do quick exploration of galaxy cluster images. 
The code is written in Python, and when run it launches in a webpage where
the user interacts with the figures. 

## Installation

The installation process is a matter of creating a Conda environment, cloning this directory, and running the app.  

First create a Conda environment and install the necessary Python packages. Note that you should replace \<name\> with your choice of environment name:

```
$ conda create -n <name> -c conda-forge python=3.10
$ conda activate <name>
$ conda install ipython numpy scipy pandas plotly dash dash-bootstrap-components matplotlib -c conda-forge
```

With the environment created you can clone the git repository and run the app.

```
$ git clone git@github.com:rjavila/interactive_catalog.git
$ cd interactive_catalog
$ python app.py
```

Open a browser and go to http://127.0.0.1:8050/ (or whatever address gets printed to the terminal). 
