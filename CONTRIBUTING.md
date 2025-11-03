# Contributing to OpenReview AC Workflow Automation

Thank you for your interest in contributing to this project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (Python version, OS, conference name)
- Any relevant error messages or logs

### Suggesting Enhancements

We welcome feature requests and enhancements! Please open an issue with:
- A clear description of the proposed feature
- Use cases and benefits
- Any implementation ideas (optional)

### Adding Support for New Conferences

One of the most valuable contributions is adding support for new conferences. To add a new conference:

1. **Study the OpenReview API structure** for your target conference
2. **Add a new entry** to the `CONFERENCE_INFO` dictionary in `main.py`
3. **Test thoroughly** with real data from the conference
4. **Update the README** to include the new conference in the supported list
5. **Submit a pull request** with your changes

Example conference configuration:
```python
"YourConf2026": dict(
    CONFERENCE_ID = 'yourconf.org/2026/Conference',
    PAPER_NUMBER_EXTRACTOR = lambda paper: paper.number,
    RATING_EXTRACTOR = lambda review: (
        int(review.content["rating"]['value'])
        if "rating" in review.content and "value" in review.content["rating"]
        else None
    ),
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

### Pull Request Process

1. **Fork the repository** and create a new branch from `main`
2. **Make your changes** with clear, descriptive commit messages
3. **Test your changes** to ensure they work as expected
4. **Update documentation** if you're adding or changing features
5. **Submit a pull request** with:
   - A clear title and description
   - Reference to any related issues
   - Screenshots or examples (if applicable)

### Code Style Guidelines

- Follow [PEP 8](https://pep8.org/) style guide for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Add comments for complex logic

### Development Setup

1. Clone your fork of the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/OpenReviewAC.git
   cd OpenReviewAC
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file for testing:
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

### Testing

Before submitting a pull request:
- Test with real OpenReview data (use a conference you have access to)
- Verify that existing functionality still works
- Check that your code doesn't introduce security vulnerabilities
- Ensure no sensitive data is committed

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Provide constructive feedback
- Focus on what is best for the community

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the "question" label
- Reach out to the maintainers

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

