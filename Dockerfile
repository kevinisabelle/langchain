# Use the official Python base image
FROM python:3.11.3

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# set timezone to montreal
RUN ln -snf /usr/share/zoneinfo/America/Montreal /etc/localtime && echo America/Montreal > /etc/timezone

RUN pip3 uninstall -y pypdf
# Install the required packages
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 list

# Copy the rest of the application code
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run"]
