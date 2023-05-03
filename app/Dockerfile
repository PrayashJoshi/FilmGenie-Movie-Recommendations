# FROM python:3.6
# COPY . /app
# WORKDIR /app
# RUN pip install -r requirements.txt
# ENTRYPOINT ["python"]
# CMD ["app.py"]

# Use the official lightweight Python image.
FROM python:3.10-slim

# logs
# ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


# Install nltk library
RUN python3.10 -m pip install nltk
RUN python3.10 -m nltk.downloader all

# Install en_core_web_sm library
RUN pip install -U spacy
RUN python3.10 -m spacy download en_core_web_sm

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

RUN python3.10 -m pip install tensorflow-cpu

# Expose port 5000
# EXPOSE 5000
# ENV PORT 5000

# Install curl
RUN apt-get update && apt-get install -y curl

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

RUN gcloud auth activate-service-account pj-778@movie-recommender-webapp.iam.gserviceaccount.com --key-file=service-account.json

RUN gsutil -m cp -r gs://pretrained-bert-model/binary_sa_bert_final .

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 ML.app:app