# ScrapIn
This module is a selenium wrapper tailored to searching people or jobs on linkedin given a set of criteria.

### System


As of: 2019-09-20 

CPython 3.7.3  

numpy 1.16.4\
pandas 0.24.2\
selenium 3.141.0\
bs4 4.7.1

compiler   : GCC 7.3.0\
system     : Linux\
release    : 5.0.0-29-generic\
machine    : x86_64\
processor  : x86_64\
CPU cores  : 12\
interpreter: 64bit

### Setup
To get started, run the following commands:

```
pip install --upgrade pip
git clone git@github.com:maximemerabet/scrapIn.git
cd scrapIn
python3 -m venv .env
source .env/bin/activate
pip install -r requirements
```

You will also need to download the chromedriver corresponding to your OS and chrome version.\
These can be found [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
Once downloaded, please move the executable to `scrapIn/.` and run the following command: `chmod +x chromedriver`

(Please note that you can use selenium's recommended driver location but will need to overwrite the chromedriver path in `config.py` or overwrite the parameter in `scraper.Authenticator.login`)

 


### How to use:
The following is an example code for a people-specific search (can be found [here](../examples/search_people.ipynb))

```
# Append to python, import
from scraper import Authenticator, Scraper

# Credential prompt
auth = Authenticator() 

# Instantiate scraper object
scraper = Scraper(authenticator=auth)

# Execute search (return DataFrame)
people_search = scraper.search_people(job_title='Executive Chef',
                                      location=['London, 'Manchester'],
                                      industry='Hospitality')

```


