# Pull base images.
FROM centos

# Install env
RUN yum -y install epel-release && yum clean all
RUN yum -y install python-pip git python-devel && yum clean all

# Set timezone
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

ENV LANG 'en_US.UTF-8'
ENV LC_ALL 'en_US.UTF-8'

# Pull
RUN git clone https://github.com/phinexdaz/identity_generator.git

WORKDIR identity_generator

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "src/web.py"]