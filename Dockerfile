
FROM python:3.8-slim-buster

# Install the security updates.
RUN apt-get update
RUN apt-get -y upgrade

# Dependencies to build requires packages
RUN apt-get -y install gcc

# Remove all cached file. Get a smaller image.
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

EXPOSE 3978

# Copy the application.
COPY . /opt/app
WORKDIR /opt/app

# Install the app librairies.
RUN pip install -r requirements.txt

# Install SpaCy small model
RUN python -m spacy download en_core_web_sm

# Start the app.
ENTRYPOINT [ "python" ]
CMD [ "main.py" ]