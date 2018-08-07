# -*- coding: utf-8 -*-

import datetime
import sys
import click

from terminaltables import AsciiTable
from irq_manager.constants import DEFAULT_DATE_TIME_FORMAT
from irq_manager.client.client import IRQClient

client = None

@click.group()
@click.argument('host')
@click.argument('port')
@click.pass_context
def irq_client(ctx, host, port):
    """
    Connects and runs REST-ful calls against the IRQ Manager Information Service.
    """
    ctx.obj = {}
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    client = IRQClient(host, port)
    return 0

@irq_client.command()
@click.pass_context
def list_devices(ctx):
    '''
    Lists the available devices found on the given host.
    '''
    host = ctx.obj.get('host')
    port = ctx.obj.get('port')
    client = IRQClient(host, port)

    devices = client.list_devices()
    click.secho("There are %d devices on '%s:%s'" % (len(devices), host, port))
    for device in devices:
        click.secho("    - %s" % device)

@irq_client.command()
@click.pass_context
def cpu_count(ctx):
    '''
    Returns the number of CPUs running on the server.
    '''
    host = ctx.obj.get('host')
    port = ctx.obj.get('port')
    client = IRQClient(host, port)

    cpu_count = client.get_cpu_count()
    click.secho("Number of CPUs on %s is: %s" % (host, client.get_cpu_count()))

@irq_client.command()
@click.argument('device')
@click.option('-s', '--start-datetime', default=None, help='YYYYMMDD-HHMMSS Format ONLY - Filter results to show only values that were created after "start-datetime"')
@click.option('-s', '--end-datetime', default=None, help='YYYYMMDD-HHMMSS Format ONLY - Filter results to show only values that were created before "end-datetime"')
@click.pass_context
def device_detail(ctx, device, start_datetime, end_datetime):
    '''
    Returns all the collected details of the provided device.
    '''
    host = ctx.obj.get('host')
    port = ctx.obj.get('port')
    client = IRQClient(host, port)

    all_devices = client.list_devices()
    if device not in all_devices:
        click.secho("Invalid Device Name: %s. Allowed Values: %s" % (device, all_devices), fg='red')
        return

    # if start_datetime and end_datetime are provided, 
    # ensure that their format is valid
    if start_datetime:
        try:
            start_datetime = datetime.datetime.strptime(start_datetime, DEFAULT_DATE_TIME_FORMAT)
        except ValueError:
            raise click.BadParameter("Start Date Time is not in format %s (YYYYMMDD-HHMMSS)" % DEFAULT_DATE_TIME_FORMAT)
    if end_datetime:
        try:
            end_datetime = datetime.datetime.strptime(end_datetime, DEFAULT_DATE_TIME_FORMAT)
        except ValueError:
            raise click.BadParameter("End Date Time is not in format %s (YYYYMMDD-HHMMSS)" % DEFAULT_DATE_TIME_FORMAT)

    
    details = client.get_device_detail(device, start_dt=start_datetime, end_dt=end_datetime)
    table_data = []

    # setup the header
    table_data.append(['irq_no', 'cpu_interrupts', 'interrupt_type', 'device', 'created_at'])

    # fill out the rows
    if details != None:
        for item in details:

            data = [
                item.get('irq_no'), 
                item.get('cpu_interrupts'),
                item.get('interrupt_type'),
                item.get('device'),
                item.get('created_at')]
            table_data.append(data)
    
    table = AsciiTable(table_data)
    print(table.table)

@irq_client.command()
@click.argument('device')
@click.option('-a', '--affinity', help="Sets the CPU Affinity, or gets it if just called without this flag.")
@click.pass_context
def cpu_affinity(ctx, device, affinity):
    '''
    Gets and Sets the CPU Affinity for the given device.
    '''
    host = ctx.obj.get('host')
    port = ctx.obj.get('port')
    client = IRQClient(host, port)
    
    all_devices = client.list_devices()
    if device not in all_devices:
        click.secho("Invalid Device Name: %s. Allowed Values: %s" % (device, all_devices), fg='red')
        return
    
    if affinity:

        old_affinity = client.get_cpu_affinity(device)
        new_affinity = client.set_cpu_affinity(device, affinity)
        click.secho("CPU Affinity has been changed from '%s' to '%s'" % (old_affinity, new_affinity), fg='green')
    
    current_affinity = client.get_cpu_affinity(device)
    click.secho("CPU Affinity has been set to '%s'" % (current_affinity), fg='green')









if __name__ == "__main__":
    sys.exit(irq_client())  # pragma: no cover
