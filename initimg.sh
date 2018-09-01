#!/usr/bin/env bash

LATEST_POST=$(ls -l _posts | tail -n 1 | awk '{print $NF}' | cut -f1 -d'.')

main() {
  # Create the image directory correspodning to the latest post
  mkdir -p assets/img/posts/$LATEST_POST
}

main $*
