#!/usr/bin/env bash

# umbrella shell script that controls behaviors of main.py execution

# hyperparams: shift start_time and end_time
start_time="13:00"
end_time="17:00"

start_time_0="12:00"
end_time_0="16:00"

start_time_1="11:00"
end_time_1="15:00"

# hyperparams: weekly schedule (0: deactivated; 1: activated)
# Monday --> Thursday
monday=1
# Tuesday --> Friday
tuesday=1
# Wednesday --> Saturday
wednesday=1
# Thursday --> Monday
thursday=1
# Friday --> Tuesday
friday=1
# Saturday --> [None]
saturday=0
# Sunday --> Wednesday,Sunday
sunday=1

# determine whether to activate bots today (via short circuiting)
case $(date +%u) in
  1) [ $monday -eq 0 ] && exit 0;;
  2) [ $tuesday -eq 0 ] && exit 0;;
  3) [ $wednesday -eq 0 ] && exit 0;;
  4) [ $thursday -eq 0 ] && exit 0;;
  5) [ $friday -eq 0 ] && exit 0;;
  6) [ $saturday -eq 0 ] && exit 0;;
  7) [ $sunday -eq 0 ] && exit 0;;
  *) exit 1 # exit with error
esac

# check hostname, then set display_id, python_dir, bot_path, bot_count
if [ $(hostname) = "Galatea" ]; then
  display_id=:0.0
  python_dir=python3
  bot_path=/home/taiyi/sign_up_bot
elif [ $(hostname) = "eternal" ]; then
  display_id=:1
  python_dir=python3
  bot_path=/home/taiyi/sign_up_bot
elif [ $(hostname) = "raspberrypi" ]; then
  display_id=:0.0
  python_dir=python3
  bot_path=/home/taiyi/sign_up_bot
else
  exit 1 # exit with error
fi

# export display_id value to shell
export DISPLAY=$display_id

# execute main.py program
$python_dir $bot_path/main.py $start_time $end_time $start_time_0 $end_time_0 $start_time_1 $end_time_1 &> $bot_path/log/$(date +%F_%H-%M).log

# exit shell script
exit 0
