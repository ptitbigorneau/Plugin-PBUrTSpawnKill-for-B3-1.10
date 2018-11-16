# -*- coding: utf-8 -*-
#
# PBUrTSpawnKill For Urban Terror plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2015 PtitBigorneau - www.ptitbigorneau.fr
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '4'

import b3
import b3.plugin
import b3.events
import datetime, math
from math import *

class PBurtspawnkillPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _protectlevel = 20
    _minspawnkilldelay = 8
    _maxspawnkilldelay = 15
    _mindistance = 100
    _maxdistance = 400
    _noskmaps = "ut4_dressingroom, ut4_prominence, ut4_killroom, ut4_uptown, ut4_harbortown"
    _sanction = "warn"
    _tempban = 60

    def onLoadConfig(self):

        self._protectlevel = self.getSetting('settings', 'protectlevel', b3.LEVEL, self._protectlevel)
        self._minspawnkilldelay = self.getSetting('settings', 'minspawnkilldelay', b3.INT, self._minspawnkilldelay)
        self._maxspawnkilldelay = self.getSetting('settings', 'maxspawnkilldelay', b3.INT, self._maxspawnkilldelay)
        self._mindistance = self.getSetting('settings', 'mindistance', b3.INT, self._mindistance)
        self._maxdistance = self.getSetting('settings', 'maxdistance', b3.INT, self._maxdistance)
        self._noskmaps = self.getSetting('settings', 'noskmaps', b3.STRING, self._noskmaps)
        self._sanction = self.getSetting('settings', 'sanction', b3.STRING, self._sanction)
        self._tempban = self.getSetting('settings', 'tempban', b3.INT, self._tempban)

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')

        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False

        self.registerEvent('EVT_CLIENT_ALIVE', self.onClientAlive)
        self.registerEvent('EVT_CLIENT_DEAD', self.onClientDead)

        self.registerEvent('EVT_CLIENT_SUICIDE', self.onClientSuicide)

    def onClientAlive(self, event):

        client = event.client
        data = event.data
        x = data['x']
        y = data['y']
        time = data['time']

        client.setvar(self, 'spawnx', float(x))
        client.setvar(self, 'spawny', float(y))
        client.setvar(self, 'spawntime', int(time))
        client.setvar(self, 'attacker', -1)

    def onClientDead(self, event):

        if self.console.getCvar('g_gametype').getInt() != 3:
            self.debug("gametype :%s"%self.console.getCvar('g_gametype').getInt())
            return

        if self.console.game.mapName in self._noskmaps:
            self.debug("map: %s"%self.console.game.mapName)
            return

        temps = 0
        client = event.client
        attacker = event.target
        data = event.data
        x = data['x']
        y = data['y']
        time = data['time']

        if client.team == attacker.team or client == attacker:
            client.setvar(self, 'attacker', -1)
        if client.team != attacker.team and client != attacker:
            client.setvar(self, 'attacker', attacker.cid)

        sclientid = client.var(self, 'attacker').toInt()

        if sclientid != -1:

            sclient = self._adminPlugin.findClientPrompt(str(sclientid), None)

        else:
            return

        if not sclient:
            return

        d = self.calculdistance(client, x, y)

        temps = int(time) - client.var(self, 'spawntime').toInt()

        if client.team == sclient.team or client == sclient or client.ip == "0.0.0.0" or sclient.ip == "0.0.0.0":
        #if client.team == sclient.team or client == sclient:
            return

        spawntest = None

        if temps/1000 <= self._minspawnkilldelay and d <= self._maxdistance:
            spawntest = "ok"
        if temps/1000 <= self._maxspawnkilldelay and d < self._mindistance:
            spawntest = "ok"

        if spawntest == "ok":

            if sclient.maxLevel >= self._protectlevel:

                #self.console.write('%s ^7Life Time: ^5%s^7 second(s) ^7Spawn Distance: ^5%s^7'%(client.exactName, temps/1000, int(round(d,0))))
                sclient.message('^1Warning ^3SpawnKill ^1Detected !!')
                sclient.message('^3You Killed %s ^3in his Spawn (^5%ss, %s^3)!!'%(client.exactName, temps/1000, int(round(d,0))))

                return

            #self.console.write('%s ^7Life Time: ^5%s^7 second(s) ^7Spawn Distance: ^5%s^7'%(client.exactName, temps/1000, int(round(d,0))))
            if self._sanction == "warn":
                self._adminPlugin.warnClient(sclient, '^3SpawnKill ^1Detected !!', None, False, '', 60)
            elif self._sanction == "message":
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
            elif self._sanction == "slap":
                self.console.write("slap %s"%sclient.cid)
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
            elif self._sanction == "kill":
                self.console.write("smite %s"%sclient.cid)
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
            elif self._sanction == "kick":
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
                sclient.kick("SpawnKill Detected !!",  None)
            elif self._sanction == "tempban":
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
                sclient.tempban("SpawnKill Detected !!", None, self._tempban, None, False)
            else:
                self.console.say('%s ^3SpawnKill ^1Detected !!'%sclient.exactName)
                self.console.write('%s ^3 Killed %s ^3in his Spawn (^5%ss, %s^3)!!'%(sclient.exactName,client.exactName, temps/1000, int(round(d,0))))

    def onClientSuicide(self, event):

        client = event.client
        client.setvar(self, 'attacker', -1)

    def calculdistance(self, client, deadx, deady):

        X1 = float(client.var(self, 'spawnx').toInt())
        Y1 = float(client.var(self, 'spawny').toInt())
        X2 = float(deadx)
        Y2 = float(deady)

        dx = X2 - X1
        dy = Y2 - Y1
        dx2 = abs(dx * dx)
        dy2 = abs(dy * dy)
        d = sqrt(dx2 + dy2)

        return d

