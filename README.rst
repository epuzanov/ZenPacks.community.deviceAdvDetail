==================================
ZenPacks.community.deviceAdvDetail
==================================

About
=====

This ZenPack is extends Zenoss with possibility to display additional hardware
details and could be used by other ZenPacks as well. Examples of details
include:

- dynamic deviceHardwareDetail tab
- dynamic deviceOsDetail tab
- dynamic deviceSoftwareDetail tab
- Number of CPU Cores
- Memory Modules section
- Logical Drives sections
- status indication for all hardware components

It also make changes deviceOSDetail tab to show only monitored Network Interfaces

Requirements
============

Zenoss
------

You must first have, or install, Zenoss 2.5.2 or later. This ZenPack was tested
against Zenoss 2.5.2, Zenoss 3.2 and Zenoss 4.2. You can download the free Core
version of Zenoss from http://community.zenoss.org/community/download.

Installation
============

Normal Installation (packaged egg)
----------------------------------

Download the `Advanced Device Details ZenPack <http://community.zenoss.org/docs/DOC-3452>`_.
Copy this file to your Zenoss server and run the following commands as the zenoss
user.

    ::

        zenpack --install ZenPacks.community.deviceAdvDetail-2.9.0.egg
        zenoss restart

Developer Installation (link mode)
----------------------------------

If you wish to further develop and possibly contribute back to the Advanced
Device Details ZenPack you should clone the git
`repository <https://github.com/epuzanov/ZenPacks.community.deviceAdvDetail>`_,
then install the ZenPack in developer mode using the following commands.

    ::

        git clone git://github.com/epuzanov/ZenPacks.community.deviceAdvDetail.git
        zenpack --link --install ZenPacks.community.deviceAdvDetail
        zenoss restart


Usage
=====

Installing the ZenPack will add the following items to your Zenoss system.


Event Class
-----------

- /Change/Set/Status

Threshold Class
---------------

- StatusThreshold
