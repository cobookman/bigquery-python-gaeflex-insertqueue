#!/bin/bash
while true
do
  curl "localhost:8080?some_string_field=MY_AWESOME_STRING"
  echo ""
done
