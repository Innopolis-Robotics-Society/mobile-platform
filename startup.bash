#!/bin/bash

set -e &&
sudo chown -R mobile:mobile /home/ws &&
exec "$@"
