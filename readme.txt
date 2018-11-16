# PBUrTSpawnKill plugin
# Plugin for B3 (https://github.com/BigBrotherBot/)
# www.ptitbigorneau.fr

PBUrTSpawnKill plugin (v4) for B3

Requirements
------------

* BigBortherBot(3) >= version 1.10
* modified server bin -> https://github.com/ptitbigorneau/PB-ioq3-for-UrbanTerror-4.3
* modified Parser iourt43 

Installation
------------

1. Copy the 'pburtspawnkill' folder into 'b3/extplugins' and 'pburtspawnkill.ini' file into '/b3/extplugins/conf'.

2. Open your B3.ini or b3.xml file (default in b3/conf) and add the next line in the [plugins] section of the file:
    for b3.xml
        <plugin name="pburtspawnkill" config="@b3/extplugins/conf/pburtspawnkill.ini"/>
    for b3.ini
        pburtspawnkill: @b3/extplugins/conf/pburtspawnkill.ini

3.  Copy parsers/iourt43.py into b3/parsers/
