FROM python:3.11-slim
COPY api/ /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh build.sh
EXPOSE 10000
ENTRYPOINT ["./entrypoint.sh"]