# Use an official Python runtime as a parent image
FROM python:3.9

RUN apt-get update && apt-get install -y python3-pip \
&& pip3 install --upgrade pip \
&& pip3 install pandas scikit-learn feast \
&& pip3 install yarl 
