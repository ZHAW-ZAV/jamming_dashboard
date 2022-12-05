FROM python:3.10

ENV DASH_DEBUG_MODE False
COPY ./app /app
WORKDIR /app
RUN set -ex && \
    pip install -r requirements.txt
EXPOSE 8050
# CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]
CMD exec gunicorn --bind 0.0.0.0:8050 app:server --timeout 600