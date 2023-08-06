# Influ
[![pipeline status](https://gitlab.com/chgrzegorz/dyplom-code/badges/develop/pipeline.svg)](https://gitlab.com/chgrzegorz/dyplom-code/commits/develop)
Finding influencers in social network

An application created as part of the project
#### Kto na kogo wpływa w sieci społecznej - aplikacja do wyszukiwania kluczowych węzłów
#### Who influences whom in social network - an application for finding key nodes
Author: **Grzegorz Chilczuk**

Supervisor: **dr inż. Radosław Michalski**

## Installation
Only Python 3.6 or higher are supported.

It should be as simple as 
```bash
pip install influ
```

### Dependencies
All dependencies will be installed automatically.
However one of most important dependencies is cool python library called [igraph](https://github.com/igraph/python-igraph/) which core is written in C.
Sometimes it may cause some problem, [igraph documentation](https://igraph.org/python/#pyinstall) should help.
##### Debian / Ubuntu and derivatives
If you encounter
> Could not download and compile the C core of igraph

then installing those dependencies should help:
```bash
 sudo apt install build-essential python-dev libxml2 libxml2-dev zlib1g-dev
```
##### Windows
If you are using Windows you have to download unofficial installer of igraph [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-igraph)
and install it by executing:
```bash
pip install <python_igraph-[igraph-version]-[python-version]-[windows version]>.whl
```
Despite that's unofficial it's recommended by maintainers of igraph library. 

Another problematic dependency is `pycairo` library which need `Microsoft Visual C++ 14.0` to be installed.

## Konect Reader
In order to test your concepts quickly there is a `KonectReader` which simplifies downloading and extracting datasets and loading them into Graph object. 
```python
from influ import reader

kr = reader.KonectReader()
print(kr.list) # list available datasets
graph = kr.load('manufacturing_emails')  # load dataset
```
Currently there is only few datasets available but you can provide your own config file with other datasets specified. Currently only datasets from [Konect](http://konect.uni-koblenz.de) are supported.

#### Your own config file
```yaml
# Content of my_custom_config.yaml
example_dataset:  # name that will be used to access dataset
  name: Example Dataset 1
  url: http://konect.uni-koblenz.de/networks/dataset_examle  # url where dataset is described [optional]
  download: http://konect.uni-koblenz.de/downloads/tsv/dataset_examle.tar.bz2  # url where dataset can be downloaded directly
  file: out.dataset_example_example  # name of file with 
  directed: False  # does graph should be considered as directed?
  edge_attributes:  # list of names attributes
    - distance      # if this list will be empty or there will be more attributes
    - another_attr  # it will be named `attrX` where X is index counted from 0
  vertex_attributes:                # list of vertex attributes with files where they are stored
    - name: alias                   # name of attribute
      file: ent.vertex_alias_name   # file with attribute
```

Loading your custom config extends (does not override) those previously loaded.
```python
from influ import reader

kr = reader.KonectReader('./my_custom_config.yaml')  # loading at creation time
kr.add_config('./my_custom_config.yaml')      # adding config after creation
```

## Working example
```python
from influ import reader, finder

kr = reader.KonectReader()
graph = kr.load('manufacturing_emails')

sfinder = finder.SeedFinder(graph)
sfinder.configure(number=5, unit='number')
result = sfinder.greedy(model=finder.Model.IndependentCascade, depth=1)
sfinder.plot_influence(result, model=finder.Model.IndependentCascade, depth=1)
```
