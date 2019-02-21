FROM douglasmiranda/caddy

# Okay an image that simple, why not just mount
# Caddyfile as a volume or using Docker Configs?

# Well a lot of reasons:
# - you may want to customize a lot your webserver / reverse proxy
# - you may want to use comercial version of Caddy
# - you may want to build Caddy yourself: https://github.com/douglasmiranda/dockerfiles/tree/master/caddy/simple
# - you may want to build Caddy with plugins: https://github.com/douglasmiranda/dockerfiles/tree/master/caddy/plugins
# - ...
COPY Caddyfile /etc/caddy/Caddyfile
