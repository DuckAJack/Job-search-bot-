# Start with a Python base image
FROM python:3.11-slim

# Install required dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Install necessary libraries for headless Chrome
RUN apt-get update && apt-get install -y \
    libx11-dev \
    libgconf-2-4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libfontconfig1 \
    libglib2.0-0 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# Set the environment variable for Chromium binary
ENV CHROME_BIN=/usr/bin/chromium

# Download the correct ChromeDriver for Chromium 131 (as the current version of Chromium on the container)
RUN wget https://chromedriver.storage.googleapis.com/131.0.6778.204/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Set the environment variable for the ChromeDriver path (optional)
ENV CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the job_bot.py script into the container
COPY job_bot.py .

# Expose port (if needed for other purposes, e.g., API calls)
EXPOSE 5000

# Run the bot script
CMD ["python", "job_bot.py"]
