# Deploying 7secs2 Casino with Portainer

This guide explains how to deploy the 7secs2 Casino application using Portainer and Docker Compose.

## Prerequisites

1. Docker installed on your server
2. Portainer installed and running
3. Access to this GitHub repository: https://github.com/Mikerstrong/7secs2.git

## Deployment Instructions

### Option 1: Using Portainer Stack with Git Repository

1. Open your Portainer dashboard
2. Navigate to Stacks
3. Click "Add stack"
4. Fill in the following information:
   - Name: 7secs2-casino
   - Build method: Repository
   - Repository URL: https://github.com/Mikerstrong/7secs2.git
   - Repository reference: main
   - Compose file path: docker-compose.yml
5. Click "Deploy the stack"
6. Once deployed, access the application at http://YOUR_SERVER_IP:7777

### Option 2: Manual Deployment

1. Clone the repository:
   ```
   git clone https://github.com/Mikerstrong/7secs2.git
   ```
2. Navigate to the project directory:
   ```
   cd 7secs2
   ```
3. Run Docker Compose:
   ```
   docker-compose up -d
   ```
4. Access the application at http://YOUR_SERVER_IP:7777

## Configuration

The application stores user data in a JSON file located at `streamlit_app/points_db.json`. This data persists as long as the volume is preserved.

## Troubleshooting

If you encounter any issues:

1. Check the container logs in Portainer
2. Ensure port 8501 is not blocked by your firewall
3. Verify that the repository is accessible to your Portainer instance
