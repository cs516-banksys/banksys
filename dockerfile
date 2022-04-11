# Python 3 image as base
FROM python:3

# Set the working directory
WORKDIR /usr/src/app

# Copy all the files
COPY . .

# Install the dependencies
RUN apt-get -y update
RUN pip3 install -r requirements.txt

# Expose default flask port
EXPOSE 5000

# Commands to run
ENTRYPOINT FLASK_APP=bank.py flask run --host=0.0.0.0
