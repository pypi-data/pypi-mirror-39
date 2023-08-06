# How to Run

**Before you do anything, make sure you've followed [this play](https://edusource.atlassian.net/wiki/spaces/PLAYB/pages/510460716/Create+AWS+Access+Credentials+and+Configure+AWS+CLI).**

### Create virtual environment or install to global pip packages

In this directory, to create a virtual environment and install dependencies, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can also install dependencies globally to your pip packages with:

```bash
sudo pip3 install -r requirements.txt
```

If you do the latter, you won't need to reactivate your virtual environment whenever you need to use the script.

### Run

Once you've followed these steps, you should be able to run the script, using (it may take a few seconds to run, depending on the size of the file):

`./matillion_column_gen.py [OPTIONS] csv_file.csv`

For more help info, run:

`./matillion_column_gen.py -h`
