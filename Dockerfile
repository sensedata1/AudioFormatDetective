FROM python
COPY . /app
WORKDIR /app

RUN chmod a+x docker-build-script.sh && ./docker-build-script.sh
RUN mkdir /AJTEMP

CMD python ./AudioFormatDetectiveSTSR.py
