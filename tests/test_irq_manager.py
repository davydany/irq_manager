#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `irq_manager` package."""


import unittest
from click.testing import CliRunner

from irq_manager.server.interrupt_reader import InterruptReader


class InterruptReaderTestcase(unittest.TestCase):
    """
    Tests Interrupt file Reader
    """
    def setUp(self):

        self.sample_file = """
           CPU0       CPU1       CPU2       CPU3
  0:        141          5         10         15   IO-APIC-edge      timer
  1:         10          0          0          0   IO-APIC-edge      i8042
  8:          0          0          0          0   IO-APIC-edge      rtc0
  9:          0          0          0          0   IO-APIC-fasteoi   acpi
 12:        155          0          0          0   IO-APIC-edge      i8042
 14:          0          0          0          0   IO-APIC-edge      ata_piix
 15:          0          0          0          0   IO-APIC-edge      ata_piix
 18:          0          0          0          0   IO-APIC-fasteoi   vboxvideo
 19:       3150          0          0      16683   IO-APIC-fasteoi   enp0s3
 20:     559857          0          0          0   IO-APIC-fasteoi   vboxguest
 21:      13151          0          0          0   IO-APIC-fasteoi   0000:00:0d.0, snd_intel8x0
        """.strip()
        self.interrupt_reader = InterruptReader(self.sample_file)

    def test_cpu_count(self):

        header = self.sample_file.split('\n')[0]
        self.assertEqual(4, self.interrupt_reader._get_cpu_count(header))

    def test_interrupt_parsing_vboxguest(self):

        sample_interrupt = self.sample_file.split('\n')[-2]
        parsed = self.interrupt_reader._parse_interrupt_line(sample_interrupt, 4)
        self.assertEqual(parsed[0], 20)
        self.assertEqual(parsed[1], {
            '0': 559857,
            '1': 0,
            '2': 0,
            '3': 0
        })
        self.assertEqual(parsed[2], 'IO-APIC-fasteoi')
        self.assertEqual(parsed[3], 'vboxguest')

    def test_interrupt_parsing_timer(self):

        sample_interrupt = self.sample_file.split('\n')[1]
        parsed = self.interrupt_reader._parse_interrupt_line(sample_interrupt, 4)
        self.assertEqual(parsed[0], 0)
        self.assertEqual(parsed[1], {
            '0': 141,
            '1': 5,
            '2': 10,
            '3': 15,
        })
        self.assertEqual(parsed[2], 'IO-APIC-edge')
        self.assertEqual(parsed[3], 'timer')