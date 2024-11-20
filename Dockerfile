FROM fedora:42

RUN dnf update -y

RUN dnf install python3-3.13.0-1.fc42 -y
RUN dnf install python3-pip-24.3.1-1.fc42 -y
RUN dnf install python3-devel-3.13.0-1.fc42 -y

RUN dnf install gcc-14.2.1-6.fc42 -y

RUN dnf install 3.0-41.fc41 -y

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 9191

ENTRYPOINT ["tail", "-f", "/dev/null"]