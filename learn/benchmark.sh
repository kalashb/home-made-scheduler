#!/bin/bash
# Simple benchmark script to generate timing data

echo "Running benchmark - sending 20 requests..."
for i in {1..20}; do
  ./client "User$i" > /dev/null 2>&1
  sleep 0.1
done

echo "done, check timings.csv"

