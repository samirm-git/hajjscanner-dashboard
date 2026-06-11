FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    streamlit-carousel
    # boto3 \
    # altair \

COPY . .

EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]