## Installing JUPYTER (OPTIONAL)

First I would recommend to install JUPYTER because it looks more appealing than VS for python.

You can either install it with your python console using the command:

```python
jupyter notebook
```

Or do it like I did and install it using *Docker* using the bash command:

```bash
docker run -p 8888:8888 -v /path/on/host:/path/in/container jupyter/base-notebook
```

## Importing the various Dictionaries 

```python
!pip install pandas matplotlib numpy
```

For installing the dictionaries and make it be avalaible for import

```python
Import pandas as pd
Import mathplotlib.pyplot as plt
Import numpy as mp
```

For importing Pandas, Mathplotlib and Numpy respectively.

*Pandas* is used for databases to access, modify and delete them.

*Numpy* is used for variables for databases.

*Mathplotlib* is used for graphic representation for the database.
