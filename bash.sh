#!/usr/bin/sh

#location
# main.py etc.py
LOC=/home/afiq/Brands-Monitoring/project/
SPLUNK_HOME=/opt/splunk/
dt=$(date '+%d-%m-%Y');
filename="result_$dt.json";

uploadtosplunk() {
	$SPLUNK_HOME/bin/splunk add oneshot "$LOC/json/$filename" -index main -sourcetype json -hostname kali -auth "admin:admin1234"
}

# ?
#cp /root/Malware-Lake/main.py $SPLUNK_HOME/bin/splunk

# run scrapping script
runScript

#upload to splunk
uploadtosplunk

