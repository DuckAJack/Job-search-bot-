# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /opt/render/project/src

# Install system dependencies for Chromium, Chromium Driver, and unzip
RUN apt-get update && \
    apt-get install -y \
    wget \
    ca-certificates \
    unzip \
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

# Manually install the correct version of ChromeDriver
RUN CHROMEDRIVER_VERSION=114.0.5735.90 && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver.zip

# Install Python dependencies from the requirements file
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Set environment variables for the location of the Chromium binary and ChromeDriver
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="/usr/local/bin:${PATH}"

# Expose port if required (optional)
EXPOSE 8000

# Run the Python script directly
CMD ["python", "job_bot.py"]
