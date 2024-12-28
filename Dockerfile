# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /opt/render/project/src

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
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

# Copy the rest of the project files into the container
COPY . .

# Set environment variable for the location of the Chromium binary
ENV CHROME_BIN=/usr/bin/chromium

# Expose port if required (optional)
EXPOSE 8000

# Command to run the Python script
CMD ["python", "job_bot.py"]

#run the bot
RUN chmod +x start.sh
