FROM python:3.7

EXPOSE 5000

WORKDIR /root/app

COPY ./req.txt ./
RUN pip install --upgrade pip
RUN pip install -r req.txt

COPY ./ ./

CMD while :; do sleep 1; done;
