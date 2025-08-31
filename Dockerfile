FROM python:3.10-slim

WORKDIR /app

# Install required packages directly
RUN pip install --no-cache-dir streamlit>=1.33 streamlit-autorefresh>=1.0.1

# Copy the application files
# No need for requirements.txt as we've installed dependencies directly
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Command to run the application
CMD ["python", "-m", "streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
