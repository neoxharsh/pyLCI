#########################
Future plans
#########################

.. note:: This list is not by any means complete. What's listed here is bound to appear sooner or later. What's not listed is either not yet considered or not going to be implemented.

=====================
Global system changes
=====================

* Make hotplug of input/output devices possible
* Make nested folders for applications

.. rubric:: Hardware

* Make a simple Arduino setup with screen&buttons and a firmware+drivers for it to act as pyLCI I/O device over serial
* Make a wireless (ESP8266?) setup

==============
Input devices
==============

* Make a "passthrough" driver for HID so that a single keyboard can both be used for X and pyLCI
* Make an input emulator for development tasks

==============
Output devices
==============

* Make an output emulator for development tasks

.. rubric:: Supporting graphical displays

* Get/make fonts
* Include compatibility layers

============
Applications
============

* Bluetooth app (involves a lot of DBus work)
* "Quick reading" app (word-by-word)
* Camera app
* Stopwatch/timer app
* UCI management app
* Counter app
* Calculator app
* Mount/unmount partitions app
* OpenHAB console
* Twitter reader
* NMap app

============
UI elements
============

.. rubric:: Adding input elements

* Date/time picker
* Simple number input
* Character input using left/down/up/right
* Character input using keypads
* File choice dialog (possibly, assisted by character input)