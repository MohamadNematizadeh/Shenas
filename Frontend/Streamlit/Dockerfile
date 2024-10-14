FROM python

WORKDIR /app

COPY ./Frontend/Streamlit  /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
