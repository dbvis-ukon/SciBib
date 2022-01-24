FROM debian
# Set configurations as environment variables
ARG SCIBIB_MYSQL_DATABASE
ARG SCIBIB_MYSQL_USER
ARG SCIBIB_MYSQL_PASSWORD
ARG SCIBIB_MYSQL_HOST
ARG SCIBIB_EMAIL_SENDER
ARG SCIBIB_BIND_ADDRESS
ARG SCIBIB_BIND_PORT
ARG MAIL_SERVER
ARG MAIL_PORT
ARG MAIL_USE_SSL
ARG MAIL_USERNAME
ARG SECURITY_PASSWORD_SALT
ARG SECRET
ARG BEHIND_PROXY
ENV SCIBIB_MYSQL_DATABASE $SCIBIB_MYSQL_DATABASE
ENV SCIBIB_MYSQL_USER $SCIBIB_MYSQL_USER
ENV SCIBIB_MYSQL_PASSWORD $SCIBIB_MYSQL_PASSWORD
ENV SCIBIB_MYSQL_HOST $SCIBIB_MYSQL_HOST
ENV SCIBIB_EMAIL_SENDER $SCIBIB_EMAIL_SENDER
ENV SCIBIB_BIND_ADDRESS $SCIBIB_BIND_ADDRESS
ENV SCIBIB_BIND_PORT $SCIBIB_BIND_PORT
ENV MAIL_SERVER $MAIL_SERVER
ENV MAIL_PORT $MAIL_PORT
ENV MAIL_USE_SSL $MAIL_USE_SSL
ENV MAIL_USERNAME $MAIL_USERNAME
ENV SECURITY_PASSWORD_SALT $SECURITY_PASSWORD_SALT
ENV SECRET $SECRET
ENV BEHIND_PROXY $BEHIND_PROXY

USER root

RUN apt-get update && apt-get install -y python3-pip \
                                         python3-dev \
                                         python3-mysqldb \
                                         default-mysql-client \
                                         python3-distutils \
                                         build-essential \
                                         libssl1.1 \
                                         default-libmysqlclient-dev \
                                         libssl-dev \
                                         curl \
                                         gnupg

RUN curl -sL https://deb.nodesource.com/setup_14.x  | bash -
RUN apt-get install -y nodejs

# add folder for the app
RUN mkdir -p /srv/scibib
RUN mkdir -p /srv/scibib/frontend/static/uploadedFiles/thumbs
# copy over code
COPY app/ /srv/scibib/
COPY requirements.txt /srv/scibib/requirements.txt

# fix permissions and switch home directory
RUN chown -R www-data:www-data /srv/scibib
USER www-data
ENV HOME=/srv/scibib
WORKDIR /srv/scibib

# add nodejs binaries to path variable
ENV PATH="${HOME}/.local/bin:/usr/local/python3/bin:${PATH}"

RUN python3 -m pip install --upgrade pip && pip3 install -r requirements.txt

# Install frontend dependencies
RUN npm --prefix frontend/static install --only=prod
RUN npm --prefix frontend/static audit fix
RUN npm --prefix frontend/static run build

# Init DB Stuff
RUN python3 init.py

# Start Gunicorn
EXPOSE $SCIBIB_BIND_PORT
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
