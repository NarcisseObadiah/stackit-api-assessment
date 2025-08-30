FROM python:3.11-slim

#Set working directory
WORKDIR  /app

#Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy the application
COPY . .

#expose the flask port
EXPOSE 5000

ENV FLASK_APP=app.python
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
