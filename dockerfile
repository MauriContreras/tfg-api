FROM python:3.10-bullseye

RUN pip install --upgrade pip

WORKDIR /api

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy app source code folder
ADD app app

EXPOSE 8081

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]