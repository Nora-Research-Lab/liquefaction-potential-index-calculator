FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY liquefaction_potential_index_calculator.py .
COPY app.py .

EXPOSE 7860

CMD ["python", "app.py"]
