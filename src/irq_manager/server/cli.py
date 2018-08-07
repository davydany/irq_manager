# -*- coding: utf-8 -*-

"""Console script for irq_manager."""
import sys
import click

from mongoengine import connect
from .app import IRQService
from .poller import Poller


@click.group()
@click.option('--mongo-host', help='Mongo Host', default='localhost')
@click.option('--mongo-port', help='Mongo Port', default='27017')
@click.option('--mongo-user', help='Mongo User', default=None)
@click.option('--mongo-pass', help='Mongo Pass', default=None)
@click.option('--mongo-db', help='Mongo Database', default='irq_manager')
@click.pass_context
def irq_manager(ctx, mongo_host, mongo_port, mongo_user, mongo_pass, mongo_db):
    """
    View and Manage Interrupt Requests.
    """
    if mongo_user and mongo_pass:
        mongodb_uri = 'mongodb://{user}:{passwd}@{host}:{port}/{db}'.format(
            user=mongo_user,
            passwd=mongo_pass,
            host=mongo_host,
            port=mongo_port,
            db=mongo_db
        )
    else:
        mongodb_uri = 'mongodb://{host}:{port}/{db}'.format(
            host=mongo_host,
            port=mongo_port,
            db=mongo_db
        )
    connect(host=mongodb_uri)
        
    ctx.obj = {
        'mongodb_uri': mongodb_uri
    }
    return 0

@irq_manager.command()
@click.argument('host')
@click.argument('port')
@click.pass_context
def serve(ctx, host, port):
    '''
    Starts the IRQ Manager Information Service.
    '''
    click.secho('Running IRQ Manager Information Service on {host}:{port}'.format(
        host=host,
        port=port
    ))
    service = IRQService(host, port)
    service.configure()
    service.run()

@irq_manager.command()
@click.argument('interval_secs')
@click.pass_context
def poll(ctx, interval_secs):
    '''
    Polls the /proc/interrupts file every 'interval_secs' seconds, and stores 
    it's contents to the database.
    '''
    poller = Poller()
    poller.poll(interval_secs)


if __name__ == "__main__":
    sys.exit(irq_manager())  # pragma: no cover
