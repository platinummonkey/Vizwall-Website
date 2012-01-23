#!/bin/bash
# Sends daily reminders to proctors about events they are assigned for the day
#  - utilizes custom django management command

pushd /vizwall/htdocs/vizwall &> /dev/null
python manage.py cron_proctor_reminder &> /dev/null
popd &> /dev/null
