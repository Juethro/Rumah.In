FROM fedora:39

RUN dnf update -y

# Install mysql-server and python3.10
RUN dnf install -y mysql-server python3.10 python3.10-devel mysql-devel pkgconfig python3.10-pip

# Install pip and Django
RUN pip3 install -r requirements.txt -y

# Install Chrome


# Copy crontab config


# Copy 


