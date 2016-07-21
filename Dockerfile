# Pull base images.
FROM centos

# Install env
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip gcc python-devel && yum clean all

# Set timezone
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV LANG 'en_US.UTF-8'
ENV LC_ALL 'en_US.UTF-8'

COPY requirements.txt /opt
COPY src /opt

WORKDIR opt

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "web.py"]