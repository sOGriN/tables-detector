FROM python:3
RUN pip install sklearn
RUN pip install PyPDF2
ADD ./TableDetector.tar.xz /app/
EXPOSE 80/tcp
WORKDIR /app/
CMD python3 Test.py