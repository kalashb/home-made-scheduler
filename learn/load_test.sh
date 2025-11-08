#!/bin/bash
# Load test to show scheduler benefits under concurrent load

echo "=== Load Test: Concurrent Requests ==="
echo "Sending 50 concurrent requests..."
echo ""

# Start timing
start_time=$(date +%s.%N)

# Send 50 requests in parallel
for i in {1..50}; do
  ./client "User$i" > /dev/null 2>&1 &
done

# Wait for all to complete
wait

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

echo "=== Results ==="
echo "Total time: ${duration} seconds"
echo "Requests: 50"
echo "Throughput: $(echo "scale=2; 50 / $duration" | bc) requests/second"
echo ""
echo "Check timings.csv for detailed metrics"

