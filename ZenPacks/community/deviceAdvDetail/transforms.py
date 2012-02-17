################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2008, 2009, 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

from ZODB.transact import transact


@transact
def processEvent(evt, device):
    if not device:
        return

    if hasattr(evt, 'compClass') and hasattr(evt, 'compStatus'):
        for comp in device.getMonitoredComponents(type=evt.compClass):
            if comp.id != evt.component:
                continue

            new_status = int(round(float(evt.compStatus)))
            if comp.status != new_status:
                comp.status = new_status

            break
