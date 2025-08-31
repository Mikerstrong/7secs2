FROM python:3.10-slim

WORKDIR /app

# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir streamlit>=1.33 streamlit-autorefresh>=1.0.1

# Clone the repository (will be used if not using volume mount)
RUN git clone https://github.com/Mikerstrong/7secs2.git /tmp/app && \
    cp -r /tmp/app/* /app/ && \
    rm -rf /tmp/app
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
