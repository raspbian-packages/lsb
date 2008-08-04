#!/bin/sh -e

echo "Importing $1/init-functions"
. $1/init-functions

log_warning_msg "Only a warning"

echo "OK!"
