
# Configurations
uWSGI = "utils/uwsgi_config.ini"
NGINX = "utils/nginx_config.conf"

SSL = "utils/ssl_script.sh"
SERVICE = "utils/systemd_script.service"
DOCKER = "utils/docker_config.run"

# May need to change
NGINX_CONF1 = "/etc/nginx/sites-enabled/"
NGINX_CONF2 = "/etc/nginx/sites-available/"
SYSTEMD_CONF = "/etc/systemd/system/"

# SET ENV

DOMAIN = None
USR = None
CUR_LOC = None