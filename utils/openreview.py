"""
OpenReview API client wrapper for managing conference papers.

This module provides a base class for interacting with the OpenReview API,
handling authentication and basic conference operations.
"""
import openreview
import os


class OpenReviewPapers(object):
    """
    Base class for OpenReview paper operations.

    Handles authentication and provides a base for conference-specific
    paper retrieval and management operations.

    Attributes:
        openreview_client: Authenticated OpenReview API client instance
        conference_id: The OpenReview conference identifier (e.g., 'ICLR.cc/2026/Conference')

    Environment Variables:
        OPENREVIEW_USERNAME: Your OpenReview account email
        OPENREVIEW_PASSWORD: Your OpenReview account password
    """
    def __init__(self, conference_id):
        """
        Initialize the OpenReview client with credentials from environment variables.

        Args:
            conference_id: The OpenReview conference identifier string

        Raises:
            Exception: If authentication fails or environment variables are not set
        """
        self.openreview_client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=os.environ.get('OPENREVIEW_USERNAME'),
            password=os.environ.get('OPENREVIEW_PASSWORD'),
        )
        self.conference_id = conference_id
