#!/bin/sh

# Local and production health checks.
# https://docs.docker.com/compose/compose-file/#healthcheck

set -o errexit
set -o pipefail

# Just checking if our homepage is 200
# So, if you plan to never have a view for /, just change
# localhost:5000/ to some available endpoint, otherwise the health check will fail.
# For example: localhost:5000/admin
# IMPORTANT: In Docker Swarm if a health check fail, the container will be restarted.
wget --spider localhost:5000/ || exit 1
