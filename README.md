Commands to get started:

- `python3 -m venv venv`
- `source venv/bin/activate`
- `python script.py <path-to-defects4j> <project-name> <min_id-max_id>`

### Producing the Box Plots

1. Install the necessary libraries by running the following commands:
   <br>`pip install pandas`
   <br>`pip install matplotlib`
2. To run the script
   <br>`python DataExtraction.py`

> **Note:** `DataExtraction.py` assumes you have an 'output' directory at the root of the project.

### Calculating Biserial Correlations

1. Activate your virtual environment using

   - 1.1 `python3 -m venv venv`\
     or `python -m venv venv` (on windows)
   - 1.2 `source venv/bin/activate`\
     or `.\venv\Scripts\Activate` (on windows)

2. `pip install -r requirements.txt`
3. `python biserial_corr.py --project_name=[project_name]` (project_name is optional)

> **Note:** `biserial_corr.py` assumes you have an 'output' directory at the root of the project.
