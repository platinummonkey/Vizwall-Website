#!/bin/bash
# Sends daily reminders to proctors about events they are assigned for the day
#  - utilizes custom django management command
#
# Setup your crontab as follows with `crontab -e`
#  # sends reminders to proctors about events assigned today every day at 1am
#  0 1 * * * /vizwall/htdocs/system_crons/proctor_reminder.sh &>/dev/null
#

pushd /vizwall/htdocs/vizwall &> /dev/null
python manage.py cron_proctor_reminder &> /dev/null
popd &> /dev/null
