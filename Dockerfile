FROM python:3.12-slim

# Set Working directory
WORKDIR /app

#copy ypur application code
COPY app.py /app

#install flask
RUN pip install flask

#Run the app
CMD [ "python", "app.py" ]
