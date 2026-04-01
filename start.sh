#!/bin/bash

# 1. Force the script to run from the correct directory
cd ~/GoPy || exit

# 2. Kill any zombies from previous crashes
pkill -f python3
pkill -f termux_gateway

# 3. Ensure the Go binary has permission to run
chmod +x gateway/termux_gateway

# 4. Start Python Brain
echo "🧠 Starting Brain..."
nohup python3 brain/server.py > brain.log 2>&1 &
sleep 3 # Give it time to bind port 8000

# 5. Start Go Gateway
echo "🛰️ Starting Gateway..."
nohup ./gateway/termux_gateway > gateway.log 2>&1 &
sleep 2 # Wait a second to see if it instantly crashes

echo "------------------------"
echo "✅ System check:"
ps -e | grep -E "python|termux_gateway"
echo "------------------------"

# 6. The Detective: Check if the Go bot died
if ! pgrep -f "termux_gateway" > /dev/null; then
    echo "❌ ERROR: The Go Gateway crashed immediately!"
    echo "🔍 Here is what went wrong (from gateway.log):"
    cat gateway.log
fi
