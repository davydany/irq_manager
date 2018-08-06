# -*- coding: utf-8 -*-

"""Console script for irq_manager."""
import sys
import click

from .app import ICQService


@click.group()
@click.pass_context
def irq_manager_server(ctx):
    """
    View and Manage Interrupt Requests.
    """
    
    return 0

@irq_manager_server.command()
@click.argument('host')
@click.argument('port')
def serve(ctx, host, port):
    '''
    Starts the IRQ Manager Information Service.
    '''
    click.secho('Running IRQ Manager Information Service on {host}:{port}'.format(
        host=host,
        port=port
    ))
    ICQService()



if __name__ == "__main__":
    sys.exit(irq_manager_server())  # pragma: no cover
