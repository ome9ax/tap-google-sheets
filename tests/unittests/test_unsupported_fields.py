from tap_google_sheets.client import GoogleClient
import unittest
from unittest.case import TestCase
from unittest import mock
from tap_google_sheets import schema

class TestUnsupportedFields(unittest.TestCase):
    @mock.patch('tap_google_sheets.GoogleClient.get')
    def test_unsupported_fields(self, mocked_get):
        """
        Test whether the incusion property for the skipped property is changed to `unsupported`
        and the description is added in the schema
        """
        sheet = {
            "sheets": [{
                "properties": {
                    "sheetId": 0,
                    "title": "Sheet1",
                    "index": 0,
                    "sheetType": "GRID",
                    "gridProperties": {
                        "rowCount": 3,
                        "columnCount": 26
                    }
                },
                "data": [
                    {
                        "rowData": [
                            {
                                "values": [
                                    {},
                                    {
                                        "formattedValue": "abc"
                                    },
                                    {
                                        "formattedValue": "def"
                                    }
                                ]
                            },
                            {
                                "values": [
                                    {
                                        "formattedValue": "A"
                                    },
                                    {
                                        "formattedValue": "B"
                                    },
                                    {
                                        "formattedValue": "4"
                                    }
                                ]
                            }
                        ]
                    }
                ]}
            ]
        }
        expected_schema = {
            "type": "object",
            "additionalProperties":False,
            "properties": {
                "__sdc_spreadsheet_id": {
                    "type": [
                        "null",
                        "string"
                    ]
                },
                "__sdc_sheet_id": {
                    "type": [
                        "null",
                        "integer"
                    ]
                },
                "__sdc_row": {
                    "type": [
                        "null",
                        "integer"
                    ]
                },
                "__sdc_skip_col_01": {
                    "type": [
                        "null",
                        "string"
                    ],
                    "description": "Column is unsupported and would be skipped because header is not available"
                },
                "abc": {
                    "type": [
                        "null",
                        "string"
                    ]
                },
                "def": {
                    "type": [
                        "null",
                        "string"
                    ]
                }
            }
        }
        mocked_get.return_value = sheet
        schemas, field_metadata = schema.get_schemas(GoogleClient('client_id', 'client_secret', 'refresh_token'), 'sheet_id')
        # check if the schemas are equal, hence verifying if the description is present
        self.assertEqual(expected_schema, schemas["Sheet1"])
        for each in field_metadata["Sheet1"]:
            if each["breadcrumb"] and '__sdc_skip_col_01' in each["breadcrumb"]:
                # check if the inclusion property is updated to `unsupported`
                self.assertEqual(each["metadata"]["inclusion"], "unsupported")