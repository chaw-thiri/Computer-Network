#!/bin/bash

# Function to test latency
test_latency() {
    host_to_ping="google.com"
    ping -c 5 "$host_to_ping" # ping google 5 times 
}

# Function to test bandwidth
test_bandwidth() {
    speedtest-cli
}

# Function to test transfer rate
test_transfer_rate() {
    file_size_mb=100  #  file size for transfer rate testing
    duration_sec=10  # duration for transfer rate testing

    # Create a temporary test file
    dd if=/dev/zero of=testfile bs=1M count="$file_size_mb" status=progress

    # Calculate transfer rate
    elapsed_time=$(($(date +%s) - start_time))
    transfer_rate_mbps=$(bc <<< "scale=2; $file_size_mb / $elapsed_time")
    
    echo "Transfer Rate: $transfer_rate_mbps Mbps"
    
    # Clean up test file
    rm -f testfile
}

echo "Latency Test:"
test_latency

echo -e "\nBandwidth Test:"
test_bandwidth

echo -e "\nTransfer Rate Test:"
start_time=$(date +%s)
test_transfer_rate
