"""
Testing suite for the extract script, including base and edge cases in the script.
"""

import io
import unittest
from unittest.mock import patch, MagicMock

import requests

from sample_extract import (extract_changing_plant_details)

sample_data = {
    "botanist": {
        "email": "carl.linnaeus@lnhm.co.uk",
        "name": "Carl Linnaeus",
                "phone": "(146)994-1635x35992"
    },
    "images": {
        "license": 45,
        "license_name": "Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)"
    },
    "last_watered": "Mon, 18 Dec 2023 14:03:04 GMT",
    "name": "Epipremnum Aureum",
            "origin_location": [
                "-19.32556",
                "-41.25528",
                "Resplendor",
                "BR",
                "America/Sao_Paulo"
    ],
    "plant_id": 0,
    "recording_taken": "2023-12-18 15:25:19",
    "scientific_name": [
                "Epipremnum aureum"
    ],
    "soil_moisture": 95.22236107163602,
    "temperature": 13.171628371788849
}


class TestTransientDataFunction(unittest.TestCase):
    """Tests involving extract_changing_plant_details()."""

    @patch('requests.get')
    def test_returns_only_essential_values(self, mock_requests_get):
        """Tests that the function only returns the transient data."""

        mock_response = MagicMock()
        mock_response.json.return_value = sample_data

        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()

        assert result["recording_taken"][0] == "2023-12-18 15:25:19"
        assert result["recording_taken"].count() == 51
        assert result["plant_id"].count() == 51
        assert result["plant_id"][0] == 0

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @patch('requests.get')
    def test_json_error_handling(self, mock_requests_get, mock_stdout):
        """
        Tests that nothing is returned if the JSONDecodeError exception is raised
        and that the expected console output is produced.
        """

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "JSONDecodeError", "", 1)
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()
        console_output = mock_stdout.getvalue()
        print(console_output)

        self.assertEqual(len(result), 0)
        assert "Error, Plant not found: " in console_output

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @patch('requests.get')
    def test_http_error_handling(self, mock_requests_get, mock_stdout):
        """
        Tests that nothing is returned if the HTTPError exception is raised
        and that the expected console output is produced.
        """

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.HTTPError
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()
        console_output = mock_stdout.getvalue()
        print(console_output)

        self.assertEqual(len(result), 0)
        assert "An Http Error occurred: " in console_output

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @patch('requests.get')
    def test_connection_error_handling(self, mock_requests_get, mock_stdout):
        """
        Tests that nothing is returned if the ConnectionError exception is raised
        and that the expected console output is produced.
        """

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.ConnectionError
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()
        console_output = mock_stdout.getvalue()
        print(console_output)

        self.assertEqual(len(result), 0)
        assert "An Error Connecting to the API occurred: " in console_output

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @patch('requests.get')
    def test_timeout_error_handling(self, mock_requests_get, mock_stdout):
        """
        Tests that nothing is returned if the Timeout exception is raised
        and that the expected console output is produced.
        """

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.Timeout
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()
        console_output = mock_stdout.getvalue()
        print(console_output)

        self.assertEqual(len(result), 0)
        assert "A Timeout Error occurred: " in console_output

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    @patch('requests.get')
    def test_request_error_handling(self, mock_requests_get, mock_stdout):
        """
        Tests that nothing is returned if the RequestException is raised
        and that the expected console output is produced.
        """

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.RequestException
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()
        console_output = mock_stdout.getvalue()
        print(console_output)

        self.assertEqual(len(result), 0)
        assert "An Unknown Error occurred: " in console_output
