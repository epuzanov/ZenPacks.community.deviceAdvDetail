################################################################################
#
# This program is part of the deviceAdvDetail Zenpack for Zenoss.
# Copyright (C) 2009-2012 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################
# Zenoss 5 no longer uses rrdtool - fixes to allow zenpack to still be used
# adapted from Zenoss 5 standards with much of the same classes - brianudwa
################################################################################

"""StatusThreshold

Make threshold comparisons dynamic by using object statusmap property rather
than just number bounds checking.

"""

import logging
log = logging.getLogger('zen.StatusThreshold')

import types

from Products.ZenModel.ZVersion import VERSION as ZENOSS_VERSION
from Products.ZenModel.ThresholdClass import ThresholdClass
from Products.ZenModel.ThresholdInstance import (
    ThresholdInstance, ThresholdContext,
    )

# Our patched mods merged orig and from cisco modified
from AccessControl import Permissions
from Globals import InitializeClass

class StatusThreshold(ThresholdClass):

    escalateCount = 0
    eventClass='/Change/Set/Status'
    severity = 3

    _properties = ThresholdClass._properties + (
        {'id':'escalateCount', 'type':'int', 'mode':'w'},
        {'id':'eventClass', 'type':'string', 'mode':'w'},
        )

    factory_type_information = (
        {
        'immediate_view' : 'editRRDStatusThreshold',
        'actions'        :
        (
          { 'id'            : 'edit'
          , 'name'          : 'Status Threshold'
          , 'action'        : 'editRRDStatusThreshold'
          , 'permissions'   : ( Permissions.view, )
          },
        )
        },
        )

    def createThresholdInstance(self, context):
        """Return the config used by the collector to process point
        thresholds. (id, escalateCount)
        """
        mmt = StatusThresholdInstance(self.id,
                                      ThresholdContext(context),
                                      self.dsnames,
                                      self.eventClass,
                                      self.escalateCount,
                                      getattr(context, "statusmap", {}),
                                      context.meta_type)
        return mmt

InitializeClass(StatusThreshold)
StatusThresholdClass = StatusThreshold

class StatusThresholdInstance(ThresholdInstance):
    def __init__(self,id,context,dpNames,eventClass,escalateCount,statusmap,mt):
        self.count = {}
        self._context = context
        self.id = id
        self.eventClass = eventClass
        self.escalateCount = escalateCount
        self.dataPointNames = dpNames
        self.statusmap = statusmap
        self.mtype = mt

    def name(self):
        return self.id

    def context(self):
        return self._context

    def dataPoints(self):
        return self.dataPointNames

    def countKey(self, dp):
        return(':'.join(self.context().key()) + ':' + dp)

    def getCount(self, dp):
        countKey = self.countKey(dp)
        if not self.count.has_key(countKey):
            return None
        return self.count[countKey]

    def incrementCount(self, dp):
        countKey = self.countKey(dp)
        if not self.count.has_key(countKey):
            self.resetCount(dp)
        self.count[countKey] += 1
        return self.count[countKey]

    def resetCount(self, dp):
        self.count[self.countKey(dp)] = 0

    def check(self, dataPoint):
        """Datapoint has been updated. Check last value."""
        return []

    def checkRaw(self, dataPoint, timeOf, value):
        """Raw value has been collected. Check it."""
        return self.checkStatus(dataPoint, value)

    def checkStatus(self, dp, value):
        'Check the value for point thresholds'
        log.debug("Checking %s %s in %s", dp, value, self.statusmap)
        try:
            status = self.statusmap[int(round(float(value)))]
            context = self.context()
            deviceName = context.deviceName
            componentName = context.componentName
        except Exception:
            return []
        msg = 'threshold of %s exceeded: current status %s' %(self.name(), status[2])
        return [dict(device=deviceName,
                    summary=msg,
                    compStatus=value,
                    compClass=self.mtype,
                    eventKey=self.id,
                    eventClass=self.eventClass,
                    component=componentName,
                    severity=status[1])]

    def getGraphElements(self, template, context, gopts, namespace, color,
                         legend, relatedGps):
        """Produce a visual indication on the graph of where the
        threshold applies."""
        unused(template, namespace)
        return gopts

    def getNames(self, relatedGps):
        legends = [ getattr(gp, 'legend', gp) for gp in relatedGps.values() ]
        return ', '.join(legends)

# This makes our threshold instance able to be serialized and sent to collectors
# in their configurations.
from twisted.spread import pb
pb.setUnjellyableForClass(StatusThresholdInstance, StatusThresholdInstance)
