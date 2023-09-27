# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update && apt-get install -y python3-pip librdkafka-dev \
&& pip3 install --upgrade pip \
&& pip3 install pandas requests matplotlib python-dotenv hopsworks \
&& pip3 install fire hsfs \
# difference each container
&& pip3 install pickle5 statsmodels scikit-learn pmdarima wandb

