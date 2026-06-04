# 20260601-DEM5 — Library Books Data Pipeline

A Python data engineering project for ingesting, processing, and analysing library book data. The pipeline reads from a SQLite database, applies transformations, and tracks pipeline run metrics.

## Overview

This project provides an end-to-end data pipeline for library book records. It uses SQLAlchemy to interact with a SQLite database (`DE5M5_Library_Books.db`), processes data with pandas, and logs pipeline activity via loguru. Pipeline performance metrics are recorded to `pipeline_metrics.csv`. The project is containerised with Docker and includes a CI/CD workflow via GitHub Actions.

## Repository Structure

```
.
├── .github/
│   └── workflows/          # GitHub Actions CI/CD configuration
├── adhoc/
│   └── docker/             # Docker setup for ad-hoc runs
├── app/                    # Main application source code
├── tests/                  # Unit and integration tests
├── DE5M5_Library_Books.db  # SQLite database of library books
├── pipeline_metrics.csv    # Logged metrics from pipeline runs
├── requirements.txt        # Python dependencies
└── README.md
```

## Prerequisites

- Python 3.8+
- Docker (optional, for containerised runs)

## Installation

```bash
git clone https://github.com/annaokes/20260601-DEM5.git
cd 20260601-DEM5
pip install -r requirements.txt
```

## Dependencies

| Package      | Purpose                              |
|--------------|--------------------------------------|
| `pandas`     | Data manipulation and transformation |
| `loguru`     | Structured logging                   |
| `sqlalchemy` | Database access (SQLite)             |

## Running the Pipeline

```bash
python app/main.py
```

Or using Docker:

```bash
cd adhoc/docker
docker build -t dem5-pipeline .
docker run dem5-pipeline
```

## Running Tests

```bash
pytest tests/
```

## Pipeline Metrics

Each pipeline run appends a row to `pipeline_metrics.csv`, capturing run-level statistics such as record counts, durations, and status. This file can be used for monitoring pipeline health over time.

## Database

`DE5M5_Library_Books.db` is a SQLite database containing library book records. It serves as the primary data source for the pipeline.

## CI/CD

GitHub Actions workflows in `.github/workflows/` automate testing and linting on every push and pull request to `main`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes and push
4. Open a pull request against `main`
