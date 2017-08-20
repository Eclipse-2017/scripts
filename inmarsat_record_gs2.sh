#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

source /home/odroid/gnuradio/target/setup_env.sh
python /home/odroid/github/waveforms/inmarsat/inmarsat_record.py --gs-name 'GS2'
