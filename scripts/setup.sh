#!/usr/bin/env bash
set -e
echo "LinuxOps Monitor setup"
echo "Checking required commands..."
command -v python3 >/dev/null && echo "Python: OK" || echo "Python: missing"
command -v node >/dev/null && echo "Node: OK" || echo "Node: missing"
command -v docker >/dev/null && echo "Docker: OK" || echo "Docker: missing"
echo "For the complete environment run: docker compose up --build"
