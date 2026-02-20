# Mini MLOps Pipeline – Technical Assessment

This project implements a reproducible, containerized batch processing pipeline that computes a rolling mean-based trading signal from cryptocurrency OHLCV data and outputs structured metrics.

The solution demonstrates:
- Deterministic execution using configuration-driven parameters
- Structured logging
- Machine-readable JSON metrics
- Dockerized batch job deployment
- Robust error handling

---

## Project Structure

    run.py              → Main pipeline script  
    config.yaml         → Configuration file  
    data.csv            → Input dataset (10,000 rows OHLCV data)  
    requirements.txt    → Python dependencies  
    Dockerfile          → Container definition  
    metrics.json        → Example output metrics (successful run)  
    run.log             → Example execution log (successful run)  

---

## Setup Instructions

Install dependencies locally:

    pip install -r requirements.txt

---

## Local Execution Instructions

Run the pipeline locally:
    python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
This will:

- Load configuration from config.yaml
- Process the dataset
- Generate rolling mean and signals
- Compute metrics
- Write metrics.json
- Write run.log
- Print final metrics to stdout

---

## Docker Instructions (MANDATORY)

Build the Docker image:

    docker build -t mlops-task .

Run the container:

    docker run --rm mlops-task


The container:

- Includes data.csv and config.yaml inside the image
- Automatically executes the batch job
- Generates metrics.json and run.log
- Prints metrics to standard output (stdout)
- Exits with code 0 on success
- Exits with non-zero code on failure

---

## Expected Output (metrics.json)

Example structure:

    {
    "version": "v1",
    "rows_processed": 10000,
    "metric": "signal_rate",
    "value": 0.4989,
    "latency_ms": 18,
    "seed": 42,
    "status": "success"
    }

Field descriptions:

- version → Extracted from config.yaml  
- rows_processed → Total number of dataset rows  
- metric → Always "signal_rate"  
- value → Mean of generated signals  
- latency_ms → Total execution time in milliseconds  
- seed → Extracted from config.yaml  
- status → "success" or "error"  

---

## Error Handling

The program gracefully handles:

- Missing input file
- Invalid CSV format
- Empty dataset
- Missing required columns
- Invalid configuration structure

If an error occurs, metrics.json will contain:


    {
    "version": "v1",
    "status": "error",
    "error_message": "Description of the issue"
    }


---

## Configuration (config.yaml)


    seed: 42
    window: 5
    version: "v1"


- seed → Ensures reproducibility  
- window → Rolling mean window size  
- version → Pipeline version identifier  

---

## Dependencies

- pandas
- numpy
- pyyaml

---

## Reproducibility

The pipeline execution is deterministic.  
Running the program multiple times produces identical metric values.

---

## Context

This task simulates a production-style MLOps workflow inspired by real-world trading systems:

- Rolling statistics on OHLCV data
- Signal generation
- Structured metrics emission
- Containerized deployment
- Reproducible ML-style pipelines