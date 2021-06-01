FROM python:3.8-alpine
MAINTAINER Rafa Muñoz rafa93m@gmail.com (@rafa93m)

RUN apk --no-cache add tzdata && \
    cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
    echo Europe/Madrid > /etc/timezone && \
    apk del tzdata

RUN set -eux \
  && pip install pymongo \
  && pip install urllib3 \
  && pip install pytelegrambotapi \
  && pip install graypy

RUN mkdir /opt/bot
COPY ./bot /opt/bot
RUN chmod -R 644 /opt/bot

RUN echo "*/10    *       *       *       *       python3 /opt/bot/check_dataset.py" >> /etc/crontabs/root

WORKDIR /opt/bot

ENTRYPOINT ["/bin/sh","/opt/bot/docker-entrypoint.sh"]

CMD ["python3","/opt/bot/bc19cyl_interactivo.py"]