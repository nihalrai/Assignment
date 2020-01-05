FROM python

MAINTAINER Nihal Rai "niihalrai@gmail.com"

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "app/poll.py" ]
