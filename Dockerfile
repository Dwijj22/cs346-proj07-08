# proj07_08/Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# 1) Install OS packages (Apache’s mod_cgid is included by default)
RUN apt-get update && apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    sqlite3 \
    curl \
    gnupg \
    ca-certificates \
    apt-transport-https \
 && rm -rf /var/lib/apt/lists/*

# 2) Add Google Cloud SDK apt repository and key, then install SDK
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
     | apt-key add - \
 && echo "deb https://packages.cloud.google.com/apt cloud-sdk main" \
     > /etc/apt/sources.list.d/google-cloud-sdk.list \
 && apt-get update \
 && apt-get install -y google-cloud-sdk \
 && rm -rf /var/lib/apt/lists/*

# 3) Install Python GCP libraries
RUN pip3 install --no-cache-dir \
    google-api-python-client \
    google-auth \
    google-auth-httplib2 \
    google-auth-oauthlib \
    google-cloud-compute

# 4) Enable CGI (mod_cgid) and allow .py scripts
RUN a2enmod cgid \
 && printf '<Directory /var/www/html>\n  Options +ExecCGI\n  AddHandler cgi-script .py\n</Directory>\n' \
      >> /etc/apache2/sites-enabled/000-default.conf

# 5) Copy your application code into Apache webroot
COPY . /var/www/html/

# 6) Make all Python scripts executable
RUN find /var/www/html -type f -name '*.py' -exec chmod +x {} \;

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
