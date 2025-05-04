# Use a lightweight Python image
FROM python:3.9-slim

# Install curl so the HEALTHCHECK can run
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variable to disable GPU use in Hugging Face Transformers
ENV USE_CPU=True

# Command to run the FastAPI app
CMD ["uvicorn", "api_rag:app", "--host", "0.0.0.0", "--port", "8000"]

# Listen-for-ready health check (follow redirects, allow longer startup)
HEALTHCHECK --interval=10s --timeout=3s --start-period=45s --retries=3 \
  CMD curl -fL http://localhost:8000/ || exit 1

