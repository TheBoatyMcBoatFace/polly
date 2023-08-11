# Use alpine with Python pre-installed
FROM python:3.10.11

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src /app/src

# Env Variables
ENV APP_PORT 3090

# Logging Level
ENV LOG_LEVEL INFO

# Values to Set
ENV OPENAI_API_KEY SET_ME
ENV GITHUB_TOKEN SET_ME

# Expose the app port
EXPOSE $APP_PORT

# Run the application
CMD ["python3", "src/api.py"]