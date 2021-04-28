
FROM ubuntu:latest



RUN apt update
RUN apt install -y python3-pip
RUN pip3 install jupyterhub jupyter

RUN export DEBIAN_FRONTEND=noninteractive && apt install -y --no-install-recommends npm
RUN npm install -g configurable-http-proxy

RUN pip3 install PyJWT oauthenticator msal

RUN echo "how about now?"

WORKDIR /tmp/working
ADD setup.py .
ADD iclauth iclauth

RUN pip3 install .

ADD jupyterhub_config.py /etc

WORKDIR /data

CMD [ "jupyterhub", "-f", "/etc/jupyterhub_config.py"]

