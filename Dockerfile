FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install -y libxml2
COPY tiberCAD-3.0.1-x86_64-linux_installer.sh /tiberCAD-3.0.1-x86_64-linux_installer.sh
RUN /tiberCAD-3.0.1-x86_64-linux_installer.sh
COPY tiberlab.lic /usr/local/tibercad-3.0.1/license
RUN mkdir /data
WORKDIR /data
