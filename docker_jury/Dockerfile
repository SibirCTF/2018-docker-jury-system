FROM debian:9.5

EXPOSE 8080
COPY ./fhq-jury-ad/debian/9.5/fhq-jury-ad /usr/bin/fhq-jury-ad
RUN mkdir /usr/share/fhq-jury-ad

RUN apt-get update && apt-get install -y libcurl3 zlibc zlib1g libpng16-16 libmariadbclient18

RUN apt-get install -y python python-requests python-pip libssl-dev
RUN pip install pwm
RUN apt-get install -y python3-pip
RUN pip3 install Faker
RUN pip3 install requests

RUN apt-get install -y dnsutils exiftool
# Fix for building on debian system (mysqlclient library)
# RUN ln -s /usr/lib/x86_64-linux-gnu/pkgconfig/mariadb.pc /usr/lib/x86_64-linux-gnu/pkgconfig/mysqlclient.pc

COPY ./apply_new_config.sh /root/apply_new_config.sh

CMD /root/apply_new_config.sh && fhq-jury-ad start


