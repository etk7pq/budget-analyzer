# Quick Start Guide - Running the Budget Analyzer

## Prerequisites Check

First, make sure Docker is running on your machine:

```bash
docker --version
docker info
```

If Docker isn't running, start Docker Desktop.

## Step-by-Step Instructions

### Step 1: Navigate to the Project Directory

```bash
cd /Users/clairenewsom/budget-analyzer
```

### Step 2: Verify Your .env File Exists

```bash
cat .env
```

You should see:
```
PORT=8080
```

If the file doesn't exist or is missing, create it:
```bash
cp .env.example .env
```

### Step 3: Build and Run (One Command)

**Option A: Using the run.sh script (Recommended)**
```bash
./run.sh
```

**Option B: Manual commands**
```bash
# Build the Docker image
docker build -t budgetanalyzer:latest .

# Run the container
docker run --rm -p 8080:8080 --env-file .env budgetanalyzer:latest
```

### Step 4: Test the API (In a New Terminal Window)

Open a **new terminal window** (keep the Docker container running in the first one) and run:

```bash
# Health check
curl http://localhost:8080/health
```

Expected response:
```json
{"status":"ok"}
```

### Step 5: Upload Sample Expenses

```bash
curl -X POST http://localhost:8080/upload \
  -H "Content-Type: application/json" \
  -d @assets/sample_expenses.json
```

Expected response:
```json
{"message":"Expenses uploaded successfully"}
```

### Step 6: Get Summary

```bash
curl http://localhost:8080/summary
```

Expected response:
```json
{
  "income": 3000,
  "total_expenses": 2000,
  "savings": 1000,
  "savings_rate": 33.33,
  "largest_expense": "rent"
}
```

### Step 7: Get Forecast

```bash
curl http://localhost:8080/forecast
```

Expected response:
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

## Stopping the Server

In the terminal where the Docker container is running, press:
```
Ctrl + C
```

## Troubleshooting

### "Permission denied" when running ./run.sh
```bash
chmod +x run.sh
```

### "Cannot connect to Docker daemon"
- Make sure Docker Desktop is running
- Check with: `docker info`

### "Port 8080 already in use"
- Change the port in `.env` to something else (e.g., `PORT=8081`)
- Update the docker run command: `docker run --rm -p 8081:8081 --env-file .env budgetanalyzer:latest`
- Update curl commands to use the new port

### "No such file or directory: .env"
```bash
cp .env.example .env
```

## Testing with Your Own Data

You can upload your own expenses:

```bash
curl -X POST http://localhost:8080/upload \
  -H "Content-Type: application/json" \
  -d '{
    "income": 5000,
    "rent": 1500,
    "food": 600,
    "transport": 300,
    "entertainment": 200,
    "utilities": 150
  }'
```

Then get the summary:
```bash
curl http://localhost:8080/summary
```

