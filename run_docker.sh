# This is a simple script to run the 7secs2 casino application in Docker
# It's an alternative to using docker-compose for simpler deployments

# Build the Docker image
docker build -t 7secs2-casino .

# Run the container
docker run -d \
  --name 7secs2-casino \
  -p 7777:8501 \
  -e STREAMLIT_SERVER_ENABLE_CORS=false \
  -e STREAMLIT_SERVER_HEADLESS=true \
  -e STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
  --restart unless-stopped \
  7secs2-casino

echo "7secs2 Casino is now running at http://localhost:7777"
