import io
import sys
import unittest
from unittest.mock import patch, MagicMock

import requests

from sample_extract import extract_plant_details, extract_changing_plant_details

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


class CustomJSONDecodeError(JSONDecodeError):
    pass


class TestRawDataFunction(unittest.TestCase):

    @patch('requests.get')
    def test_successfully_gets_info(self, mock_requests_get):
        """Tests that essential plant details are successfully extracted"""

        mock_response = MagicMock()
        mock_response.json.return_value = sample_data

        mock_requests_get.return_value = mock_response
        result = extract_plant_details()

        self.assertIn("plant_id", result[0])
        self.assertIn("scientific_name", result[0])
        self.assertIn("temperature", result[0])
        self.assertIn("soil_moisture", result[0])

    @patch('requests.get')
    def test_json_error_handling(self, mock_requests_get):
        """Tests that nothing is returned if the JSON exception is raised"""

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "JSONDecodeError", "", 1)
        mock_requests_get.return_value = mock_response
        result = extract_plant_details()

        self.assertEqual(len(result), 0)


class TestTransientDataFunction(unittest.TestCase):

    @patch('requests.get')
    def test_returns_only_essential_values(self, mock_requests_get):
        """Tests that the function only returns the transient data"""

        mock_response = MagicMock()
        mock_response.json.return_value = sample_data

        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()

        self.assertIn("plant_id", result[0])
        self.assertIn("recording_taken", result[0])
        self.assertIn("last_watered", result[0])
        self.assertIn("temperature", result[0])
