Commands to get started:

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python script.py <path-to-defects4j> <project-name> <min_id-max_id>`

Once data is collected, you can run `python analysis.py` to calculate correlation coefficients, p-values, means, and medians. This script will also generate box plots. All resulting files are located in the `/analysis` directory.

Running <i>skippedBugCheck.py</i> <br><br>
`python skippedBugCheck.py --input <path/to/analysis/file> --project <project-name>`
<br>
example of running for Math project:
<br>
`python skippedBugCheck.py --input ./output/Math_analysis.csv --project Math`
