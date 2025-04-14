#!/bin/sh

# When invoked by docker compose, exit because we only want it to build the image
if [ "$ONLY_BUILD" = "true" ]; then
  exit 0
fi

# Auto stop after 1 minute
atd
echo "halt" | at now +1minute

cd /scanner;

nuclei $@
