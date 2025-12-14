# Final Review from hw

## To Remember by Heart

### Data Science Process

1. Question Definition
2. Data Collection
3. Data Annotation
4. Data Analysis
5. Interpretation
6. Communication

## Topology

### A Topology is:

- Comprehensive
- Well-defined
- Objective-ish

### Building a Topology

### Document:

- Motivation / Context
- Overview of types and their relations
- List of types with:
  - Concise definition
  - Examples with rationale (both positive and negative)
  - Edge cases with rationale
- Argument / Evidence for comprehensiveness

### Building a Topology:

1. Get representative data
2. Get topology (existing or through open coding)
3. Sanity check by yourself
4. Human test
5. Does it work? if not goto 2 or 3

### Open Coding Process:

1. Sample data
2. Come up with categories with sample
3. Validate categories with more data

### Code Book

Extends topology document and includes challenging examples.

### Human coding process

1. Preparation phase
   - Decide coding group
   - Develop code book
   - Develop annotation software (if needed)

2. Annotation phase
   - Recruit annotators
   - Train annotators
   - Coding exercises

3. Validation phase
   - Throughout, assess quality and level of agreement

### TF-IDF

### Network Analysis

Closeness: how close to any node
Betweenness: how many shortest paths pass through a node

### Network Structure

- Microscale
- Mesoscale
- Macroscale

### Key Interpretative Techniques

1. Assert contextualized answers
2. Include negative outcomes
3. Support by combining results
4. Support by extrapolating from results
5. Use point to make the meta point

### Tricky cases in data annoatation

- Tricky edge cases
- Bad annotators
- Human error
- Ambiguous guidelines

What perceptual constraints does the audience have?

- Resolution
- Color perception

### Centrality

- Degree
- Closeness -> how close to any other node
- Betweenness -> how many shortest paths pass through a node

### Structure of a written report

1. Motivation
2. Objective / Problem
3. Data / Design
4. Results
5. Findings
6. Conclusion

## HW1

### Pandas (can skip)

## HW2 - The Data Science Process

### My Little Pony annotation (can skip)

## HW3 - Unix server and command-line exercises

### Bash User Management

```bash
# create a user
sudo adduser newuser

# add user to sudo group
sudo usermod -aG sudo newuser

# change user password
sudo passwd newuser

# switch into user
su newuser

# put public key into authorized_keys file
ssh-copy-id -i ~/.ssh/id_ed25519 mimi
```

### SSH config

```
Host mimi
  HostName 192.168.1.100
  User newuser
  IdentityFile ~/.ssh/id_ed25519
```

## HW4 - Unix commands and MLP

### Push to GitHub

```bash
git remote add origin git@github.com:denis-tsariov/hehehehaw.git
git branch -M main
git push -u origin main
```

### CLI tools

```bash
head -n 5 filename.txt

tail -n 20 filename.txt
tail -f logfile.txt # follow the log file

less filename.txt # view file content

wget -O newname.txt https://example.com/file.txt # download file to newname.txt

curl -o newname.txt https://example.com/file.txt # download file to newname.txt
# wget is for downloading files, curl is for transferring data and testing connections.

grep -i "pattern" filename.txt # case-insensitive search

wc -l filename.txt # count lines
wc -w filename.txt # count words
wc -c filename.txt # count characters
```

## HW5 - Data Analysis

### argparse

```python
parser = argparse.ArgumentParser(description="Process some NYC complaints.")
parser.add_argument(
    "-i", type=str, required=True, help="Input csv file", metavar="input_file"
)
parser.add_argument(
    "-s", type=str, required=True, help="Start date", metavar="start_date"
)
parser.add_argument(
    "-e", type=str, required=True, help="End date", metavar="end_date"
)
parser.add_argument(
    "-o",
    type=str,
    required=False,
    help="Output file",
    metavar="output_file",
    default=None,
)

args = parser.parse_args()
```

### bokeh dashboard

```python
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

# Create a ColumnDataSource
data = {'x': [1, 2, 3], 'y': [4, 5, 6]}
source = ColumnDataSource(data)

# Create a figure
p = figure(title="Bokeh Dashboard", x_axis_label='X', y_axis_label='Y')

# Add a line plot
p.line('x', 'y', source=source)

# Show the plot
show(p)
```

## HW6

Similar to HW5, with questiuon building

## HW7

### BeautifulSoup

```python
from bs4 import BeautifulSoup
import requests

# Fetch a web page
response = requests.get('https://example.com')
html = response.text

# Create a BeautifulSoup object
soup = BeautifulSoup(html, 'html.parser')

# More powerful selection using CSS selectors
elements = soup.select('.class-name')
element = soup.select_one('#id-name')
nested = soup.select('div.container > p')
```

## HW8 - Data Sampling

Snowball sampling vs systematic sampling

## HW9 - Topology Creation

```python
# Optional argument with flag
parser.add_argument('-o', '--output',
                    dest='out_file',
                    required=True,
                    help='Output TSV file path')

# Positional arguments
parser.add_argument('json_file',
                    help='Input JSON file path')

parser.add_argument('num_posts_to_output',
                    type=int,
                    help='Number of posts to extract')

args = parser.parse_args()
```

## HW10 - Data Annotation

### Taxonomy (coding) guide:

1. Motivation - why this taxonomy was built
2. Each taxonomy category
   1. Definition
   2. Examples (positive and negative)
   3. Edge cases (what's in, but might not look like it; what's out, but might look like it)

## HW11 - Automated Data Annotation

Precision = TP / (TP + FP)
Recall = TP / (TP + FN)

### LLM Annotation

```python

import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(f"Classify this: {text}")
label = response.text.strip()

```
