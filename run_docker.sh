# This is a simple script to run the 7secs2 casino application in Docker
# It's an alternative to using docker-compose for simpler deployments

# Pull the Python image directly
docker pull python:3.10-slim

# Run the container with direct GitHub cloning
docker run -d \
  --name 7secs2-casino \
  -p 7777:8501 \
  -e STREAMLIT_SERVER_ENABLE_CORS=false \
  -e STREAMLIT_SERVER_HEADLESS=true \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  --restart unless-stopped \
  python:3.10-slim \
  bash -c "apt-get update && \
           apt-get install -y git && \
           git clone https://github.com/Mikerstrong/7secs2.git /app && \
           pip install --no-cache-dir streamlit>=1.33 streamlit-autorefresh>=1.0.1 && \
           python -m streamlit run /app/streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0"

echo "7secs2 Casino is now running at http://localhost:7777"
