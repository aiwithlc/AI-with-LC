# Use a Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the correct port
ENV PORT=8080
EXPOSE 8080

# Start the bot
CMD ["gunicorn", "-b", "0.0.0.0:8080", "chatbot:app"]
