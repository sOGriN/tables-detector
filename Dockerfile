FROM python:3
RUN pip install sklearn
RUN pip install PyPDF2
ADD ./TableDetector.tar.xz /app/
EXPOSE 80/tcp
CMD cd /app/ && python3 Test.py