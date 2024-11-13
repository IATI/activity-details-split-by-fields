import setuptools

setuptools.setup(
    name="iati_activity_details_split_by_fields",
    version="0.0.0",
    url="https://github.com/IATI/activity-details-split-by-fields",
    project_urls={
        "Issues": "https://github.com/IATI/activity-details-split-by-fields/issues",
        "Source": "https://github.com/IATI/activity-details-split-by-fields",
    },
    license="BSD 3-clause",
    packages=setuptools.find_packages(exclude=["test"]),
    install_requires=[],
    extras_require={
        "dev": [
            "pytest==8.3.3",
            "black==24.10.0",
            "isort==5.13.2",
            "flake8==7.1.1",
            "mypy==1.13.0",
        ]
    },
    python_requires=">=3.9",
)
