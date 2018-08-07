===========
IRQ Manager
===========

Views and Manage CPU Affinity for Interrupt Requests

Important Notes Before Starting
-------------------------------

These are important things to note before using this library.

* This application only works with interrupt request numbers that are integers,
  and not ones that are strings (like: "CAL" or "LOC"). This makes the parsing
  of the /proc/interrupts file a little easier to parse.

Usage
-----

