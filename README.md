# Personal Budget Analyzer API

## 1) Executive Summary

**Problem:** Many individuals track expenses inconsistently and lack a clear view of how day-to-day spending choices compound over months and years. Without structured feedback, it is hard to understand opportunity costs, identify budget leaks, or see how inflation quietly erodes purchasing power. People often rely on spreadsheets or banking apps that show totals but don't translate those numbers into actionable insights such as savings rate, category trends, or long-term projections. This project addresses that gap by turning simple monthly inputs into interpretable metrics and forward-looking guidance.

**Solution:** This personal budget analyzer is a RESTful API built with Flask that ingests a user's monthly income and expense categories, computes core financial indicators (savings rate, total expenses, largest expense category), and generates inflation-aware forecasts for future expenses. The API demonstrates how modest, consistent analysis can improve financial decision-making by highlighting savings rate, largest expense categories, and how a baseline inflation model shifts affordability over a five-year horizon. The system is containerized with Docker for easy deployment and reproducibility.

## 2) System Overview

### Course Concept(s)

This project integrates multiple concepts from the course modules:

- **Flask API Development**: RESTful endpoints (`/health`, `/upload`, `/summary`, `/forecast`) with proper HTTP methods and status codes
- **Logging/Metrics**: Structured logging using Python's `logging` module to track API operations and data uploads
- **Containerization**: Docker-based deployment for reproducible, isolated execution environments
- **Environment Configuration**: Environment variable management via `.env` files for port configuration

### Architecture Diagram

```
┌─────────────────┐
│   Client/User   │
│  (HTTP Client)  │
└────────┬────────┘
         │ HTTP Requests
         │ (GET/POST)
         ▼
┌─────────────────────────────────────┐
│      Flask Application              │
│  ┌───────────────────────────────┐ │
│  │  /health  (GET)               │ │
│  │  /upload  (POST)              │ │
│  │  /summary (GET)               │ │
│  │  /forecast (GET)              │ │
│  └───────────────────────────────┘ │
│         │                           │
│         ▼                           │
│  ┌───────────────────────────────┐ │
│  │  In-Memory Data Store         │ │
│  │  (expenses_data list)         │ │
│  └───────────────────────────────┘ │
│         │                           │
│         ▼                           │
│  ┌───────────────────────────────┐ │
│  │  Business Logic               │ │
│  │  - Savings calculation        │ │
│  │  - Inflation forecasting      │ │
│  │  - Expense analysis           │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  JSON Response  │
│  (Financial     │
│   Metrics)      │
└─────────────────┘
```

### Data/Models/Services

- **Input Format**: JSON objects with `income` (required) and expense categories (e.g., `rent`, `food`, `transport`, `entertainment`)
- **Sample Data**: Provided in `assets/sample_expenses.json` for testing
- **Data Storage**: In-memory list (ephemeral, resets on container restart)
- **Inflation Model**: Simple 3% annual inflation rate for 5-year forecasting
- **License**: Sample data is synthetic and provided for demonstration purposes

## 3) How to Run (Local)

### Docker

```bash
# Build the Docker image
docker build -t budgetanalyzer:latest .

# Run the container (using the provided run.sh script)
./run.sh

# Or run manually:
docker run --rm -p 8080:8080 --env-file .env budgetanalyzer:latest

# Health check
curl http://localhost:8080/health

# Upload sample expenses
curl -X POST http://localhost:8080/upload \
  -H "Content-Type: application/json" \
  -d @assets/sample_expenses.json

# Get summary
curl http://localhost:8080/summary

# Get forecast
curl http://localhost:8080/forecast
```

### Prerequisites

- Docker installed and running
- `.env` file created from `.env.example` (contains `PORT=8080`)

## 4) Design Decisions

### Why Flask API?

Flask was chosen as the framework because it provides a lightweight, flexible foundation for building RESTful APIs. It aligns with the course module on Flask API development and offers:
- Simple routing and request handling
- Built-in JSON support
- Easy integration with containerization
- Minimal dependencies for fast container builds

**Alternatives considered:**
- **FastAPI**: More modern with automatic OpenAPI docs, but Flask was the focus of the course module
- **Django REST Framework**: More features but heavier and overkill for this simple use case
- **Express.js (Node.js)**: Different language ecosystem, not aligned with course Python focus

### Tradeoffs

**Performance:**
- **In-memory storage**: Fast reads/writes but data is lost on container restart. Suitable for demo/prototype, but production would need a database (PostgreSQL, MongoDB, etc.)
- **Single-threaded Flask dev server**: Fine for development/testing, but production requires a WSGI server (Gunicorn, uWSGI) behind a reverse proxy (Nginx)

**Complexity:**
- **Simple inflation model**: Fixed 3% rate is easy to understand but doesn't account for category-specific inflation or economic volatility
- **No authentication**: Keeps the API simple but means no multi-user support or data isolation

**Maintainability:**
- **Modular structure**: `src/` directory separates application code from configuration
- **Environment variables**: Port configuration externalized for flexibility
- **Docker**: Ensures consistent execution environment across machines

### Security/Privacy

**Current Implementation:**
- No authentication/authorization (demo only)
- Input validation: Basic check for `income` field presence
- No PII handling: All data is financial aggregates, not personal identifiers
- Secrets management: Environment variables via `.env` (not committed to repo)

**Production Considerations:**
- Add input validation (e.g., ensure numeric values, reasonable ranges)
- Implement rate limiting to prevent abuse
- Add HTTPS/TLS for encrypted communication
- Consider authentication (API keys, OAuth) for multi-user scenarios
- Use a database with proper access controls instead of in-memory storage

### Operations

**Logging:**
- Python `logging` module configured at INFO level
- Logs expense uploads for audit trail
- Container logs accessible via `docker logs`

**Scaling:**
- Current design is single-container, single-instance
- Horizontal scaling would require:
  - Shared database (Redis, PostgreSQL) instead of in-memory storage
  - Load balancer (Nginx, HAProxy)
  - Container orchestration (Kubernetes, Docker Swarm)

**Known Limitations:**
- Data persistence: All data lost on container restart
- No concurrent user isolation: All users share the same in-memory data store
- Fixed inflation rate: Doesn't adapt to economic conditions or category-specific trends
- No historical tracking: Only the latest uploaded expenses are analyzed

## 5) Results & Evaluation

### Sample Outputs

**Health Check:**
```json
{
  "status": "ok"
}
```

**Summary (after uploading sample data):**
```json
{
  "income": 3000,
  "total_expenses": 2000,
  "savings": 1000,
  "savings_rate": 33.33,
  "largest_expense": "rent"
}
```

**Forecast:**
```json
{
  "inflation_forecast": {
    "2026": 2060.0,
    "2027": 2121.8,
    "2028": 2186.45,
    "2029": 2252.05,
    "2030": 2319.61
  }
}
```

### Performance Notes

- **Container Build Time**: ~2-3 seconds (cached layers)
- **API Response Time**: <10ms for all endpoints (local testing)
- **Memory Footprint**: ~50-100MB (Python 3.11-slim base image + Flask)
- **Container Size**: ~150MB (compressed)

### Validation/Tests

Basic smoke tests are provided in `tests/test_app.py`:
- Health endpoint returns 200 OK
- Upload and summary endpoints work correctly
- Savings rate calculation is included in summary

Run tests (requires pytest):
```bash
pip install pytest
pytest tests/test_app.py
```

## 6) What's Next

**Planned Improvements:**
1. **Database Integration**: Replace in-memory storage with PostgreSQL or MongoDB for persistence
2. **User Authentication**: Add API key or JWT-based authentication for multi-user support
3. **Historical Analysis**: Track expenses over time and provide trend analysis
4. **Category-Specific Inflation**: Use different inflation rates per expense category
5. **Budget Alerts**: Notify users when expenses exceed thresholds
6. **Export Functionality**: Generate CSV/PDF reports of financial summaries

**Refactors:**
- Extract business logic into separate modules (e.g., `calculations.py`, `forecasting.py`)
- Add configuration management class for better env var handling
- Implement proper error handling with custom exception classes
- Add request validation using a library like `marshmallow` or `pydantic`

**Stretch Features:**
- Machine learning model for expense prediction based on historical patterns
- Integration with banking APIs for automatic expense import
- Web dashboard (React/Vue frontend) for visual budget analysis
- Mobile app (React Native) for on-the-go expense tracking

## 7) Links

**GitHub Repo:** https://github.com/etk7pq/budget-analyzer

**Public Cloud App (optional):** [INSERT-CLOUD-URL]

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Flask framework: https://flask.palletsprojects.com/
- Python Docker image: https://hub.docker.com/_/python
- Sample expense data: Synthetic data created for demonstration purposes
