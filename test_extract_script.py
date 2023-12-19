import io
import sys
import unittest
from unittest.mock import patch, MagicMock, Mock

import requests

from sample_extract import (extract_plant_details, extract_changing_plant_details,
                            write_to_csv)

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


class TestRawDataFunction(unittest.TestCase):
    """Tests involving extract_plant_details()."""

    @patch('requests.get')
    def test_successfully_gets_info(self, mock_requests_get):
        """Tests that essential plant details are successfully extracted."""

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
        """Tests that nothing is returned if the JSON exception is raised."""

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "JSONDecodeError", "", 1)
        mock_requests_get.return_value = mock_response
        result = extract_plant_details()

        self.assertEqual(len(result), 0)


class TestTransientDataFunction(unittest.TestCase):
    """Tests involving extract_changing_plant_details()."""

    @patch('requests.get')
    def test_returns_only_essential_values(self, mock_requests_get):
        """Tests that the function only returns the transient data."""

        mock_response = MagicMock()
        mock_response.json.return_value = sample_data

        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()

        self.assertIn("plant_id", result[0])
        self.assertIn("recording_taken", result[0])
        self.assertIn("last_watered", result[0])
        self.assertIn("temperature", result[0])

    @patch('requests.get')
    def test_json_error_handling(self, mock_requests_get):
        """Tests that nothing is returned if the JSON exception is raised."""

        mock_response = MagicMock()
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "JSONDecodeError", "", 1)
        mock_requests_get.return_value = mock_response
        result = extract_changing_plant_details()

        self.assertEqual(len(result), 0)


class TestWriteToCSVFunction(unittest.TestCase):

    @patch('csv.DictWriter')
    def test_write_to_csv(self, mock_csv_writer):
        """csv.DictWriter().writerow should be called when the function is called."""

        # Create fake data
        data_sample = [{
            "botanist": {
                "name": "fake name"
            },
            "name": "fake_plant",
            "plant_id": 1
        }]
        write_to_csv(data_sample, "test_file.csv")

        # Expected written data
        expected_data = {
            "botanist": {
                "name": "fake name"
            },
            "name": "fake_plant",
            "plant_id": 1
        }

        # Assert writerow is called once with the passed in entry
        mock_csv_writer.return_value.writerow.assert_called_once_with(
            expected_data)

    @patch('csv.DictWriter')
    def test_write_to_csv_multiple(self, mock_csv_writer):
        """csv.DictWriter().writerow should be called twice when the function is called."""

        # Create fake data
        data_sample = [{
            "botanist": {
                "name": "fake name"
            },
            "name": "fake_plant",
            "plant_id": 1
        },
            {
            "botanist": {
                "name": "fake name2"
            },
            "name": "fake_plant2",
            "plant_id": 2
        }]

        write_to_csv(data_sample, "test_file.csv")

        # Expected written data
        expected_data = [
            {
                "botanist": {
                    "name": "fake name"
                },
                "name": "fake_plant",
                "plant_id": 1
            },
            {
                "botanist": {
                    "name": "fake name2"
                },
                "name": "fake_plant2",
                "plant_id": 2
            }
        ]

        print(expected_data[0], expected_data[1])

        # Assert writerow is called once with the passed in entry
        mock_csv_writer.return_value.writerow.assert_has_calls([
            unittest.mock.call(expected_data[0]),
            unittest.mock.call(expected_data[1])
        ])

    @patch('csv.DictWriter')
    def test_write_to_csv_empty(self, mock_csv_writer):
        """
        csv.DictWriter().writerow should be not be called when
        the function is called using an empty details_list.
        """

        # Create fake data
        data_sample = []
        write_to_csv(data_sample, "test_file.csv")

        # Expected written data
        expected_data = {}

        # Assert writerow is called once with the passed in entry
        mock_csv_writer.return_value.writerow.assert_not_called()
