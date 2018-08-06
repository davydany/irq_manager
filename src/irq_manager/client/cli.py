# -*- coding: utf-8 -*-

"""Console script for irq_manager."""
import sys
import click

@click.group()
@click.argument('host')
@click.argument('port')
@click.pass_context
def irq_manager_client(ctx, host, port):
    """
    View and Manage Interrupt Requests.
    """
    ctx.object = {
        'host': host,
        'port': port
    }
    return 0

@irq_manager_client.command()
def client(ctx):
    '''
    Connects and runs REST-ful calls against the IRQ Manager Information Service.
    '''
    host = ctx.object['host']
    port = ctx.object['port']
    click.secho('Connecting to IRQ Manager Information Service on {host}:{port}'.format(
        host=host,
        port=port
    ))


if __name__ == "__main__":
    sys.exit(irq_manager_client())  # pragma: no cover
