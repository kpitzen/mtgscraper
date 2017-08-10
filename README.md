# MTGScraper

### This project is designed to provide easier access to MTG data for analysis.  Currently, only the ETL portion of this project is being explored, but stretch goals include data analysis tools, as well.
---

## Getting started:
---

### Requirements:
  - [Python 3.6](http://www.python.org/)
  - Modules included in requirements.txt
  - AWS account

### Steps for your first run:
  0. Recursively clone this repository to your workspace
  0. Create a dynamodb table named mtgdecks with two keys:
     - Primary: deck_id
     - Sort Key: row_id
  0. Run the command: <code> pip install -r requirements.txt </code>
  0. Run an extract (currently, only [MTGGoldfish](http://www.mtggoldfish.com/) is supported):
    > python main.py extract -gf
  4. Run a load:
    > python main.py load -d

This will populate your existing dynamodb table with 20 randomly chosen decklists.

### TODO:
--- 
- [ ] Add more sources

- [ ] Improve load performance

- [ ] Benchmark and optimize payload creation