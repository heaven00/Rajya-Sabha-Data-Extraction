# Rajya Sabha Data Extraction 

With the whole lot of misinformation and misguided stats that are becoming part of our daily life I want to create a source of data
that might tell me more about what is really happening in the country. So this project is a naive attempt to make the Rajya Sabha debates 
data more accessible for people to consume.

# The data
Currently the debates from Rajya sabha are published in PDF format on their website.

- Verbatim archives, i.e. debates by time and day `http://164.100.47.5/newsite/debatenew/newshow.aspx?arch=245` This includes the un edited debates noted down during the conduct by hours of the days
- Date Wise Full day edited debates `http://164.100.47.5/newsite/floor_official_debate/floor_official_debate.aspx`

# Starting Notebooks

You will first need to create an environment using virtualenv

`virtualenv path/to/a/folder`

Activate the virtualenv using `source` command

`source path/to/the/folder/bin/activate`

Install requirements

`pip install requirements.txt`

The above command will install all the required libraries required for running the notebooks and any code in the project.

To Add the environment that we have created jupyter notebook follow the steps at 

[jupyter-venv](https://anbasile.github.io/programming/2017/06/25/jupyter-venv/)

Once you have that setup, cd into the `notebooks` directory and run the following command

`jupyter notebook`

this will start the jupyter notebook server

