# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update && apt-get install -y python3-pip librdkafka-dev ca-certificates \
&& pip3 install --upgrade pip \
&& pip3 install pandas requests matplotlib python-dotenv hopsworks \
&& pip3 install fire hdfs pyyaml wandb \ 
# difference each container
&& pip3 install great_expectations seaborn yarl scikit-learn

