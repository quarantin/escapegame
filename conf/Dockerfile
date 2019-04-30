FROM ubuntu:16.04
COPY . /opt/escapegame
RUN apt-get update && apt-get -y install apt-utils avahi-daemon libterm-readline-gnu-perl sudo wget
ENV TERM linux
ENV DEBIAN_FRONTEND noninteractive
#RUN /opt/escapegame/scripts/provision.sh escapegame
RUN /opt/escapegame/scripts/set-hostname.sh escapegame
