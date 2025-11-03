# OpenReview AC Workflow Automation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

Automate your Area Chair (AC) workflow for OpenReview conferences. This tool retrieves all papers assigned to you as an AC, extracts review scores and discussion activity, and organizes everything in a Google Sheet for easy tracking and management.

## Features

- **Automatic Paper Retrieval**: Fetches all papers assigned to you as an Area Chair
- **Review Tracking**: Extracts review scores (initial and final ratings)
- **Discussion Monitoring**: Counts rebuttals, comments, and AC letters
- **Google Sheets Integration**: Writes all data to a structured spreadsheet
- **Multi-Conference Support**: Works with ICLR, NeurIPS, ICCV, and ICML
- **Incremental Updates**: Can update existing sheets without clearing previous data

## Supported Conferences

- ICLR 2026
- NeurIPS 2025
- ICCV 2025
- ICML 2025

Additional conferences can be easily added by extending the `CONFERENCE_INFO` dictionary (see [Adding New Conferences](#adding-new-conferences)).

## Prerequisites

- Python 3.11 or higher
- OpenReview account with Area Chair role
- Google Cloud project with Sheets API enabled
- Google service account credentials

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/coallaoh/OpenReviewAC.git
   cd OpenReviewAC
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
OPENREVIEW_USERNAME=your_email@example.com
OPENREVIEW_PASSWORD=your_password
GSHEET_CREDENTIALS_PATH=your-service-account-key.json
```

**Note**:
- The script automatically loads these values from the `.env` file using `python-dotenv`
- Keep your `.env` file secure and never commit it to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits

### 2. Google Sheets API Setup

To write data to Google Sheets, you need a service account:

1. **Create a Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable the Google Sheets API**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

3. **Create a Service Account**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Fill in the service account details and create
   - Click on the created service account
   - Go to the "Keys" tab
   - Click "Add Key" → "Create new key" → "JSON"
   - Download the JSON key file

4. **Save the credentials**:
   - Move the downloaded JSON file to the project directory
   - Rename it to something memorable (e.g., `gsheet-credentials.json`)
   - Add the filename to your `.env` file as `GSHEET_CREDENTIALS_PATH`

5. **Share your Google Sheet**:
   - Open the JSON credentials file
   - Find the `client_email` field (looks like `xxx@xxx.iam.gserviceaccount.com`)
   - Create a new Google Sheet or open an existing one
   - Click "Share" and add the service account email as an editor

### 3. Configuration

Edit `config.py` to customize your settings:

```python
# Choose your conference
CONFERENCE_NAME = "ICLR2026"  # Options: "ICLR2026", "NeurIPS2025", "ICCV2025", "ICML2025"

# Name of your Google Sheet
GSHEET_TITLE = f"{CONFERENCE_NAME} AC DB"

# Worksheet name (tab)
GSHEET_SHEET = "Sheet1"

# Set to True to clear the sheet and start fresh, False to update existing data
INITIALIZE_SHEET = False
```

**Important**: The `GSHEET_CREDENTIALS_PATH` is now configured in your `.env` file (see step 1).

## Usage

Once configured, simply run:

```bash
python main.py
```

The script will:
1. Connect to OpenReview using your credentials
2. Retrieve all papers assigned to you as an Area Chair
3. Extract review scores, comments, rebuttals, and other activity
4. Write/update the data in your Google Sheet

### Output Data

The Google Sheet will contain the following columns for each paper:

- **paper_title**: Title of the submission
- **paper_number**: OpenReview paper number
- **paper_url**: Direct link to the paper on OpenReview
- **num_reviewers**: Number of assigned reviewers
- **avg_score**: Average initial review score
- **reviewer1_score** through **reviewer5_score**: Individual reviewer scores
- **avg_final_score**: Average final review score (if applicable)
- **reviewer1_final_score** through **reviewer5_final_score**: Final scores
- **review_count**: Number of official reviews
- **rebuttal_count**: Number of author rebuttals
- **discussion_comment_count**: Number of reviewer-author discussion comments
- **other_comment_count**: Number of other comments
- **ac_letter_author_count**: Number of AC letters from authors
- **ac_letter_ac_count**: Number of AC letters from ACs
- **withdrawn**: Whether the paper has been withdrawn

## Adding New Conferences

To add support for a new conference:

1. Add an entry to the `CONFERENCE_INFO` dictionary in `config.py`:

```python
"YourConf2026": dict(
    # Required: Conference ID from OpenReview
    CONFERENCE_ID = 'yourconf.org/2026/Conference',

    # Required: Function to extract paper number
    PAPER_NUMBER_EXTRACTOR = lambda paper: paper.number,

    # Optional: Function to extract rating from review
    RATING_EXTRACTOR = lambda review: (
        int(review.content["rating"]['value'])
        if "rating" in review.content and "value" in review.content["rating"]
        else None
    ),

    # Required: Dictionary of note type extractors
    NOTE_EXTRACTORS = {
        'review': lambda note: any(
            invitation.endswith('Official_Review') for invitation in note.invitations
        ),
        'rebuttal': lambda note: any(
            invitation.endswith('Rebuttal') for invitation in note.invitations
        ),
        # Add more note types as needed
    }
)
```

2. Update `CONFERENCE_NAME` to match your new conference key

3. Test thoroughly with a small number of papers first

## Troubleshooting

### "You are not an area chair for this conference"
- Verify that `CONFERENCE_NAME` matches the conference where you're an AC
- Check that you're logged in with the correct OpenReview account
- Ensure your AC assignment is active in OpenReview

### "Permission denied" errors with Google Sheets
- Verify that the service account email has editor access to the Google Sheet
- Check that the service account JSON file path is correct
- Ensure the Google Sheets API is enabled in your Google Cloud project

### "Module not found" errors
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

### Script runs but no data appears in Google Sheet
- Check the sheet name in `GSHEET_TITLE` matches exactly
- Verify the worksheet tab name in `GSHEET_SHEET` is correct
- Look at the console output for error messages

## Contributing

Contributions are welcome! We especially appreciate:
- Support for new conferences
- Bug fixes and improvements
- Documentation enhancements
- Feature requests and ideas

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on how to contribute. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using the [OpenReview Python API](https://github.com/openreview/openreview-py)
- Google Sheets integration via [gsheet-manager](https://pypi.org/project/gsheet-manager/)

## Support

If you find this tool helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs via GitHub issues
- 💡 Suggesting new features
- 🤝 Contributing code or documentation

## Citation

If you use this tool in your research or workflow, please cite:

```bibtex
@software{openreview_ac_workflow,
  author = {Oh, Seong Joon},
  title = {OpenReview AC Workflow Automation},
  year = {2025},
  url = {https://github.com/coallaoh/OpenReviewAC}
}
```

## Contact

For questions or issues, please open an issue on [GitHub](https://github.com/coallaoh/OpenReviewAC/issues).

