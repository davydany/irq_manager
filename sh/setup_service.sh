#!/bin/bash
cp -r ./irq_manager_poller.service /etc/systemd/system/irq_manager_poller.service
cp -r ./irq_manager_serve.service /etc/systemd/system/irq_manager_serve.service

systemctl daemon-reload
systemctl enable irq_manager_poller
systemctl enable irq_manager_serve
systemctl start irq_manager_poller
systemctl start irq_manager_serve