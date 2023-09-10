# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update && apt-get install -y python3-pip \
&& pip3 install --upgrade pip \
&& pip3 install pandas requests matplotlib seaborn python-dotenv \
&& pip3 install yarl fire hopsworks \
&& pip3 install great_expectations hdfs 

