FROM selenium/standalone-chrome:latest
USER root
RUN apt-get update && apt-get install -y python3-pip
RUN pip install selenium && pip install Selenium-Screenshot
COPY helloworld.py /test/helloworld.py
WORKDIR /test
CMD [ "python3", "helloworld.py" ]