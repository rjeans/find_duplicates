# Company Name Similarity Grouping

This project groups similar company names based on fuzzy matching and outputs a CSV file showing duplicates and their common name.

## Project Structure

- `process_names.py`: Main script to process company names and find similar ones.
- `names.csv`: Sample input file (can be replaced with your own data).
- `output_names.csv`: Output file containing duplicate names and their common name.

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python3 process_names.py

   ```
