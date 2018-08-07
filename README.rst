===========
IRQ Manager
===========

Views and Manage CPU Affinity for Interrupt Requests

Important Notes Before Starting
-------------------------------

These are important things to note before using this library.

* This application only works with interrupt request numbers that are integers,
  and not ones that are strings (like: **"CAL"** or **"LOC"**). This makes the 
  parsing of the /proc/interrupts file a little easier to parse.

* This application assumes that your environment is Centos 7. It has been tested
  on Centos 7.5. 

Environment Setup
-----------------

A test environment is provided with this project in the **Vagrantfile**. You can
launching if you have **Vagrant** and **VirtualBox** installed on your system by
calling:

.. code:: bash

  vagrant up

This will take a few minutes, but once the system is up and provisioned, you can
login using **vagrant ssh**, and run the commands.

The Provisioning code sets up a virtualenv in **/irq_manager/venv/**. You will 
need to activate it by running the following command before proceeding.

.. code:: bash

  source /irq_manager/venv/bin/activate 

Application Architecture
------------------------

This application **(IRQ Manager)** has 2 major components: The Server Side 
component and the client side component. The Server side has 2 sub components:
**The Poller** and **The Service**. The Client side has a simple command line 
interface **Client**.

This allows you to run the IRQ Manager on remote systems, and poll these remote
systems from a different system. 

Installation
------------

To install IRQ Manager and it's different components, simply run:

.. code:: bash

  pip install --upgrade git+https://github.com/davydany/irq_manager

**IRQ Manager** requires MongoDB to store the data that it polls, and access the
historic data that it polls. This is installed in the Vagrant box that you launched
when running **vagrant up**.

Usage
-----

**The Poller:** The poller sits in the background and polls **/proc/interrupts**
at the specifivied intervals, for new interrupts data, and populates a Mongo 
database with what it finds. 

Here is a simple way to start the Poller manually, and poll every 60 seconds, 
run:

.. code:: bash

  irq_manager poll 60 


**The Service:** The service connects to the Mongo backend and provides historic
data of what the Poller found, along with the ability to set CPU affinity for any 
give interrupt.

Here is a simple way to start the Service manually, and have it's different
API endpoints available to access from a client.

.. code:: bash

  irq_manager serve 0.0.0.0 8080

**The Client:** The client can be installed on any machine, and only needs to be
provided the host and port where the Service is running, and it'll take care of
the rest.

.. code:: bash

  irq_client 192.168.1.123 8000 <ACTION>

You can access the different commands by running:

.. code:: bash

  (venv) [vagrant@localhost irq_manager]$ irq_client --help
  Usage: irq_client [OPTIONS] HOST PORT COMMAND [ARGS]...

    Connects and runs REST-ful calls against the IRQ Manager Information
    Service.

  Options:
    --help  Show this message and exit.

  Commands:
    cpu_affinity   Gets and Sets the CPU Affinity for the given...
    cpu_count      Returns the number of CPUs running on the...
    device_detail  Returns all the collected details of the...
    list_devices   Lists the available devices found on the...

Distribution
------------

You can distribute individual wheel files of this entire project by running:

.. code:: bash

  make wheel


What this does is simply run:

.. code:: bash

  python setup.py bdist_wheel

The generated **whl** file will be generated and left in **./dist** as 
**irq_manager-0.1.0-py2.py3-none-any.whl**.


Automating
----------

This project has a built-in setup script to enable it to have the **Poller** and
the **Service** start automatically on boot. To enable it, run:

.. code:: bash

  vagrant ssh 
  cd /irq_manager/sh
  ./setup_service.sh

This will configure **systemctl** on Centos systems to run the **Poller** and 
**Service** on boot, enable it, and launch it. To verify that it is working 
properly, run:

.. code:: bash

    ps -ef | grep irq_manager

You will see something like this:

.. code:: bash

    (venv) [vagrant@localhost irq_manager]$ ps -ef | grep irq_manager
    root     12566     1  0 06:04 ?        00:00:03 /irq_manager/venv/bin/python3 /irq_manager/venv/bin/irq_manager poll 60
    root     12581     1  0 06:04 ?        00:00:02 /irq_manager/venv/bin/python3 /irq_manager/venv/bin/irq_manager serve 0.0.0.0 8080
    vagrant  12602 12406  0 06:19 pts/0    00:00:00 grep --color=auto irq_manager