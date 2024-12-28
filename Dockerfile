FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libx11-dev \
    libglib2.0-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libappindicator3-1 \
    libxtst6 \
    libxss1 \
    libgbm-dev \
    libsecret-1-0 \
    libgtk-3-0 \
    ca-certificates \
    fonts-liberation \
    libu2f-udev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN playwright install

# Expose the necessary port
EXPOSE 8080

# Command to run the bot
CMD ["python", "job_bot.py"]
