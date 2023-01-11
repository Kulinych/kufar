FROM python:3.12.0a1-alpine3.16
RUN apk update && apk add git \
&& rm -rf /etc/apk/cache /var/cache/apk/* /tmp/* /var/tmp/* \
&& git clone -b v1.2 https://github.com/Kulinych/parsing.git \
&& cd parsing && pip3 install -r requirements.txt \
&& apk del git

VOLUME [ "/data" ]

ENTRYPOINT [ "python3", "/parsing/parsing.py", "-t", "TOKEN", "-i","chat-id", "-s", "search"]

