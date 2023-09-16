# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update && apt-get install -y python3-pip \
&& pip3 install --upgrade pip \
&& pip3 install python-dotenv hopsworks pandas \
&& pip3 install fire scikit-learn \
&& pip3 install pickle5 hsfs

