# IATI Activity Details Split By Fields

A Python library for splitting IATI activity transactions by countries, regions, and sectors while maintaining correct percentage allocations. This library ensures accurate division of transaction values across multiple dimensions while preserving percentage integrity.

## Background and Methodology

This library implements the IATI transaction splitting methodology as described in:
- [IATI Country Data Methodology](https://countrydata.iatistandard.org/methodology/#24-splitting-transactions-for-multiple-sectors-and-countries)
- [IATI Transaction Breakdown](https://datasette.codeforiati.org/iati/transaction_breakdown)
- [IATI Standard Process Discussion](https://github.com/IATI/standard-process/discussions/11)
- [HDX IATI COVID-19 Dashboard](https://data.humdata.org/viz-iati-c19-dashboard/about)

### Key Principles

1. No Double Counting
   - If one activity spans multiple countries, the sum of split transactions should equal the original amount
   - Example: For an activity in countries A and B, sum(country A transactions) + sum(country B transactions) = original amount

2. Value-Only Splitting
   - Only the transaction value field is modified during splitting
   - Currency information remains unchanged
   - Percentages are used to split values

3. Transaction vs Activity Level Declarations
   - Fields can be declared at transaction level or activity level
   - Transaction-level declarations take precedence

## Overview

This library provides functionality to:
- Split transactions by countries with percentage allocations
- Split transactions by regions with percentage allocations
- Split transactions by sectors with vocabulary support
- Automatically normalise incorrect percentages
- Prevent double counting in splits
- Generate consistent JSON output

## Installation

```bash
# Clone the repository
git clone https://github.com/IATI/activity-details-split-by-fields.git
cd activity-details-split-by-fields

# Install the package
pip install -e .
```

## Detailed Splitting Rules

### Transaction-Level Declarations
When fields are declared at transaction level:
- recipient-country OR recipient-region (only one of these)
  * The whole transaction is applied to that country/region
  * No splitting occurs
- sector (one per vocabulary, but can have multiple vocabularies)
  * Transaction is repeated for each vocabulary with the same value

### Activity-Level Declarations
When fields are not declared at transaction level:
- Look for fields at activity level
- Use percentages to create new values
- Can have multiple:
  * recipient-countries
  * regions
  * sectors
- All should have percentages
- If percentages don't sum to 100%, they are normalised

### Mixed-Level Declarations
When some fields are at transaction level and others at activity level:
- Transaction-level declarations take precedence
- Activity-level declarations are used for missing fields

## Usage Examples

### Basic Country Split
```python
from iati_activity_details_split_by_fields.iati_activity import IATIActivity
from iati_activity_details_split_by_fields.iati_activity_transaction import IATIActivityTransaction
from iati_activity_details_split_by_fields.iati_activity_recipient_country import IATIActivityRecipientCountry

# Split $1000 between two countries
activity = IATIActivity(
    transactions=[IATIActivityTransaction(value=1000)],
    recipient_countries=[
        IATIActivityRecipientCountry(code="FR", percentage=60),  # France: 60%
        IATIActivityRecipientCountry(code="GB", percentage=40),  # UK: 40%
    ]
)

results = activity.get_transactions_split_as_json()
```

### Region Split
```python
from iati_activity_details_split_by_fields.iati_activity_recipient_region import IATIActivityRecipientRegion

# Split $1000 between regions
activity = IATIActivity(
    transactions=[IATIActivityTransaction(value=1000)],
    recipient_regions=[
        IATIActivityRecipientRegion(code="ASIA", percentage=70),   # Asia: 70%
        IATIActivityRecipientRegion(code="AFRICA", percentage=30), # Africa: 30%
    ]
)

results = activity.get_transactions_split_as_json()
```

### Sector Split
```python
from iati_activity_details_split_by_fields.iati_activity_sector import IATIActivitySector

# Split $1000 between sectors
activity = IATIActivity(
    transactions=[IATIActivityTransaction(value=1000)],
    sectors=[
        IATIActivitySector(vocabulary="DAC", code="HEALTH", percentage=60),    # Health: 60%
        IATIActivitySector(vocabulary="DAC", code="EDUCATION", percentage=40), # Education: 40%
    ]
)

results = activity.get_transactions_split_as_json()
```

### Complex Example: Multiple Splits
```python
# Example: $1000 transaction split between:
# - Two countries (50% each)
# - Two sectors (50% each)

activity = IATIActivity(
    transactions=[IATIActivityTransaction(value=1000)],
    recipient_countries=[
        IATIActivityRecipientCountry(code="A", percentage=50),
        IATIActivityRecipientCountry(code="B", percentage=50),
    ],
    sectors=[
        IATIActivitySector(vocabulary="DAC", code="SECTOR_A", percentage=50),
        IATIActivitySector(vocabulary="DAC", code="SECTOR_B", percentage=50),
    ]
)

# Results will be:
# 1. Country A, Sector A: $250 (25%)
# 2. Country A, Sector B: $250 (25%)
# 3. Country B, Sector A: $250 (25%)
# 4. Country B, Sector B: $250 (25%)
```

## Features in Detail

### Percentage Normalisation
The library automatically normalizes percentages that don't sum to 100%. For example:
- If country percentages sum to 70%, they're normalized to 100%
- A 30% share becomes (30/70 * 100) = 42.86%
- A 40% share becomes (40/70 * 100) = 57.14%

### Splitting Order
Transactions are split in this order:
1. Countries (if any)
2. Regions (if any)
3. Sectors (if any)

### Output Format
All outputs follow this structure:
```python
{
    "value": float,                    # Split transaction value
    "recipient_country_code": str,     # Country code or None (NOT a list)
    "recipient_region_code": str,      # Region code or None (NOT a list)
    "sectors": [                       # List of sectors (can be empty)
        {
            "vocabulary": str,         # Sector vocabulary (defaults to DAC-5 if value present)
            "code": str               # Sector code
        }
    ]
}
```

## API Reference

### IATIActivity
Main class for handling transaction splits.

#### Methods:
- `get_transactions_split()`: Returns list of split transactions
- `get_transactions_split_as_json()`: Returns list of split transactions in JSON format

### IATIActivityTransaction
Represents a single transaction.

#### Attributes:
- `value`: Transaction amount
- `sectors`: List of sectors
- `recipient_country_code`: Country code (single value)
- `recipient_region_code`: Region code (single value)

### IATIActivityRecipientCountry
Represents a country allocation.

#### Attributes:
- `code`: Country code
- `percentage`: Allocation percentage

### IATIActivityRecipientRegion
Represents a region allocation.

#### Attributes:
- `code`: Region code
- `percentage`: Allocation percentage

### IATIActivitySector
Represents a sector allocation.

#### Attributes:
- `vocabulary`: Sector vocabulary
- `code`: Sector code
- `percentage`: Allocation percentage

## Development

### Setting up Development Environment
```bash
# Install development dependencies
pip install -e .[dev]
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_at_activity_level.py -v

# Run tests with specific keyword
pytest tests/ -v -k "country"
```

### Linting
```bash
# Run all lint checks
black iati_activity_details_split_by_fields/*.py tests/*.py
isort iati_activity_details_split_by_fields/*.py tests/*.py
flake8 iati_activity_details_split_by_fields/*.py tests/*.py
mypy --install-types --non-interactive -p iati_activity_details_split_by_fields
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Run tests
5. Create a pull request





