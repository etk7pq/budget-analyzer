#!/bin/bash
docker build -t budgetanalyzer:latest .
docker run --rm -p 8080:8080 --env-file .env budgetanalyzer:latest

