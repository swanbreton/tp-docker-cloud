FROM python:3.11-alpine
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /home/appuser/app
COPY server.py .
USER appuser
EXPOSE 9000
CMD ["python", "server.py"]