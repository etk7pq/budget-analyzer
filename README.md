# Personal Budget Analyzer

##Executive Summary
Problem: Many individuals track expenses inconsistently and lack a clear view of how day-to-day spending choices compound over months and years. Without structured feedback, it is hard to understand opportunity costs, identify budget leaks, or see how inflation quietly erodes purchasing power. People often rely on spreadsheets or banking apps that show totals but don't translate those number into actionable insights such as savings rate, category trends, or long-term projects. This project addresses that gap by turning simple monthy inputs into interpretable metrics and forward-looking guidance.
Solution: This personal budget analyzer is an API that ingests a user's monthy income and expense categories, computes core financial indicators, and generates inflation-aware forecasts for future expenses. This API demonstrates how modest, consistent analysis can improve financial decision-making by highlighting savings rate, largest expense categories, and how a baseline inflation model shifts affordability over a five-year horizon.

## System Overview
- Course Concept: Flask API, Data Pipelines, and Logging/Metrics
- Architecture: Flask app → expense dataset → analysis endpoints
- Data: Sample monthly expenses (JSON in '/assets')

![Architecture Diagram](assets/diagram.png)

## How to Run (Docker)
'''bash
# build
docker build -t budgetanalyzer:latest .

# run
docker run --rm -p 8080:8080 --env-file .env budgetanalyzer:latest

#health check
curl http://localhost:8080/health

