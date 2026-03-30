# Stage 1: Build the Go Gateway
FROM golang:1.22-alpine AS builder
WORKDIR /app/gateway
COPY gateway/ .
RUN go build -o /gateway-binary main.go

# Stage 2: The Final Lightweight Python Environment
FROM python:3.11-slim
WORKDIR /app

# Copy the compiled Go binary from Stage 1
COPY --from=builder /gateway-binary /usr/local/bin/gateway

# Copy your Python Brain files
COPY brain/ ./brain/

# Install Python dependencies
RUN pip install --no-cache-dir -r brain/requirements.txt

# Create a master startup script that runs both simultaneously
RUN echo '#!/bin/sh\n\
python3 brain/server.py &\n\
gateway\n\
' > start.sh && chmod +x start.sh

# Launch the bot!
CMD ["./start.sh"]