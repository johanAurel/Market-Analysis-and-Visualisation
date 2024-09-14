## MARKET ANALYSIS AND VISUALISATION

 Create an application that can perform trades in your given broker.
Install pip and python if you do not have them already
```bash
sudo apt install pip
sudo apt install python3
```
 ```bash
pip install pandas matplotlib numpy
```

For installing the library and making it be available for import

__Technologies Used__

- Python
- Panda
- Matplotlib
- APIs
- Docker

__INSTALLATION JUPYTER (OPTIONAL)__

First I would recommend to install __JUPYTER__ because it looks more appealing than __VSCode__ for __Python__.

You can either install it with your __Python__ console using the command:

```python
jupyter notebook
```

Or do it like I did and install it using *Docker* using the bash command:

```bash
docker run -p 8888:8888 -v /path/on/host:/path/in/container jupyter/base-notebook
```

__IMPORT THE VARIOUS LIBRARY__ 

```python
Import pandas as pd
Import mathplotlib.pyplot as plt
Import numpy as np
%matplotlib inline
```

For importing __Pandas__, __Mathplotlib__ and __Numpy__ respectively.

__Pandas__ is used for databases to access, modify and delete them.

__Numpy__ is used for variables for databases.

__Mathplotlib__ is used for graphic representation for the database.

__SEGMENT CODE TO MAKE IT MORE READABLE AND REUSABLE__

Create a code Directory containing a __model__ folder, a __controller__ file and a __Dockerfile__.

The __model.py__ file contains the different functions for indicators to use and those create resistance and support levels.

The __controller.py__ file contains the API

The __Dockerfile__ is an image of the app
