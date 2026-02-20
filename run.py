import argparse
import json
import logging
import os
import time

import pandas as pd
import numpy as np
import yaml


# ---------------- CLI ---------------- #
def parse_args():
    parser = argparse.ArgumentParser(description="Mini MLOps pipeline")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--output", required=True, help="Path to metrics JSON")
    parser.add_argument("--log-file", required=True, help="Path to log file")
    return parser.parse_args()


# ---------------- Logging ---------------- #
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# ---------------- Config ---------------- #
def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file not found")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise ValueError("Invalid config format")

    required = ["seed", "window", "version"]
    for key in required:
        if key not in config:
            raise ValueError(f"Missing config field: {key}")

    return config


# ---------------- Data ---------------- #
def load_data(input_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input file not found")

    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise ValueError("Invalid CSV format")

    if df.empty:
        raise ValueError("CSV file is empty")

    if "close" not in df.columns:
        raise ValueError("Missing required column: close")

    return df


# ---------------- Processing ---------------- #
def generate_signals(df, window):
    logging.info(f"Rolling mean calculated with window={window}")

    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    df["signal"] = df["signal"].fillna(0)

    logging.info("Signals generated")

    return df


# ---------------- Metrics ---------------- #
def compute_metrics(df, start_time, version, seed):
    rows_processed = len(df)
    signal_rate = df["signal"].mean()
    latency_ms = int((time.time() - start_time) * 1000)

    metrics = {
        "version": version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": round(float(signal_rate), 4),
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    return metrics


# ---------------- Error Output ---------------- #
def write_error(output_path, version, message):
    err = {
        "version": version,
        "status": "error",
        "error_message": message
    }

    with open(output_path, "w") as f:
        json.dump(err, f, indent=2)

    print(json.dumps(err, indent=2))


# ---------------- Main ---------------- #
def main():
    args = parse_args()
    setup_logging(args.log_file)

    start_time = time.time()

    logging.info("Job started")

    try:
        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # Load data
        df = load_data(args.input)
        logging.info(f"Data loaded: {len(df)} rows")

        # Process
        df = generate_signals(df, window)

        # Metrics
        metrics = compute_metrics(df, start_time, version, seed)

        # Write metrics
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics: signal_rate={metrics['value']}, rows_processed={metrics['rows_processed']}")
        logging.info(f"Job completed successfully in {metrics['latency_ms']}ms")

        # Print to stdout (required)
        print(json.dumps(metrics, indent=2))

    except Exception as e:
        logging.error(str(e))
        write_error(args.output, "v1", str(e))
        exit(1)


if __name__ == "__main__":
    main()