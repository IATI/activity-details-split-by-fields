import pytest

from iati_activity_details_split_by_fields.iati_activity import IATIActivity

test_from_iati_xml_data = [
    (
        "<iati-activity></iati-activity>",
        {
            "recipient_countries": [],
            "recipient_regions": [],
            "sectors": [],
            "transactions": [],
        },
    ),
    (
        "<iati-activity>"
        + '    <recipient-region code="489" vocabulary="1" percentage="50" />'
        + "</iati-activity>",
        {
            "recipient_countries": [],
            "recipient_regions": [
                {
                    "code": "489",
                    "percent": 50,
                    "vocabulary": "1",
                }
            ],
            "sectors": [],
            "transactions": [],
        },
    ),
    (
        "<iati-activity>"
        + '    <recipient-country code="489" percentage="50" />'
        + "</iati-activity>",
        {
            "recipient_countries": [
                {
                    "code": "489",
                    "percent": 50,
                }
            ],
            "recipient_regions": [],
            "sectors": [],
            "transactions": [],
        },
    ),
    (
        "<iati-activity>"
        + '    <sector code="489" vocabulary="1" percentage="50" />'
        + "</iati-activity>",
        {
            "recipient_countries": [],
            "recipient_regions": [],
            "sectors": [
                {
                    "code": "489",
                    "percent": 50,
                    "vocabulary": "1",
                }
            ],
            "transactions": [],
        },
    ),
    (
        "<iati-activity>"
        + "    <transaction>"
        + "        <value>1000</value>"
        + '        <sector code="489" vocabulary="1" />'
        + '        <recipient-country code="489"  />'
        + '        <recipient-region code="489" vocabulary="1" percentage="50" />'
        + "    </transaction>"
        + "</iati-activity>",
        {
            "recipient_countries": [],
            "recipient_regions": [],
            "sectors": [],
            "transactions": [
                {
                    "recipient_country": {
                        "code": "489",
                    },
                    "recipient_region": {
                        "code": "489",
                        "vocabulary": "1",
                    },
                    "sectors": [
                        {
                            "code": "489",
                            "vocabulary": "1",
                        },
                    ],
                    "value": 1000.0,
                }
            ],
        },
    ),
]


@pytest.mark.parametrize("data, expected_value", test_from_iati_xml_data)
def test_from_iati_xml(data, expected_value):
    assert expected_value == IATIActivity.from_iati_xml(data).get_as_json()
