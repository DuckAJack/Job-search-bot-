# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /opt/render/project/src

# Install system dependencies (if needed for your application)
RUN apt-get update && apt-get install -y \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libx11-xcb1 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from the requirements file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Use the Selenium Standalone Chrome image
FROM selenium/standalone-chrome:latest

# Set the working directory
WORKDIR /opt/render/project/src

# Copy the rest of the project files into the container
COPY . .

# Make sure the start.sh script is executable by modifying it locally first
# If it's still causing permission issues, try to copy it with `chmod` applied in a different way
RUN chmod +x /opt/render/project/src/start.sh || true

# Expose port if required (optional)
EXPOSE 8000

# Command to run the Python script
CMD ["python", "job_bot.py"]

# Optional: If you need to run the bot via the start.sh script, uncomment this
# CMD ["/opt/render/project/src/start.sh"]
