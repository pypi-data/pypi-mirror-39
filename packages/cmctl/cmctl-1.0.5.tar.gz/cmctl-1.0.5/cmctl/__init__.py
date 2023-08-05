'''CLI module.'''

import datetime
import os
import sys
import time
import click
from .talker import Talker, TalkerException

FILTERS = ['none', 'average', 'hybrid', 'median']


def summary(text):
    click.echo(text, err=True)
    click.echo(text)


@click.group()
@click.version_option()
def cli():
    '''Conductometer Control Tool.'''


@cli.command()
def devices():
    '''Print available devices.'''
    if os.name == 'nt' or sys.platform == 'win32':
        from serial.tools.list_ports_windows import comports
    elif os.name == 'posix':
        from serial.tools.list_ports_posix import comports
    for port in sorted(comports()):
        click.echo(port[0], err=True)


@cli.command()
@click.option('--device', '-d', type=str, required=True, help='Device path.')
@click.option('--interval', '-i', default=1, type=click.IntRange(1, 86400), help='Scan interval in seconds.')
@click.option('--frequency', '-f', default=10000, type=click.IntRange(10, 1000000), help='Modulation frequency in Hz.')
@click.option('--filtering', '-q', default='none', type=click.Choice(FILTERS), help='Algorithm for filtering.')
@click.option('--samples', '-a', default=1, type=click.IntRange(1, 256), help='Number of samples for filtering.')
@click.option('--no-sync', '-s', is_flag=True, help='Disable synchronous demodulation.')
@click.option('--sequential', '-e', is_flag=True, help='Enable sequential measurement.')
@click.option('--deplete', '-x', default=0, type=click.IntRange(0, 1000), help='Depletion delay in milliseconds.')
@click.argument('channels', default='1,2,3,4,5,6,7,8,9,10,11,12')
def scan(device, interval, frequency, filtering, samples, no_sync, sequential, deplete, channels):
    '''Scan specified channels.'''
    channels = list(set(map(str.strip, channels.split(','))))
    for channel in channels:
        if not channel.isdigit() or int(channel) < 1 or int(channel) > 12:
            raise click.BadArgumentUsage('Channels must be supplied as comma-separated numbers.')
    summary('Scan interval: %d seconds' % (interval))
    summary('Modulation frequency: %d Hz' % (frequency))
    summary('Filtering algorithm: %s' % (filtering))
    summary('Number of samples: %d' % (samples))
    summary('Synchronous demodulation: %s' % ('no' if no_sync else 'yes'))
    summary('Sequential measurement: %s' % ('yes' if sequential else 'no'))
    summary('Depletion delay: %d ms' % (deplete))
    for i in range(1, 13):
        summary('Channel %d enabled: %s' % (i, 'yes' if str(i) in channels else 'no'))
    talker = Talker(device)
    talker.command('F%d' % (frequency))
    talker.command('A%d' % (samples))
    if filtering == 'average':
        talker.command('Q1')
    elif filtering == 'hybrid':
        talker.command('Q2')
    elif filtering == 'median':
        talker.command('Q3')
    else:
        talker.command('Q0')
    talker.command('D%d' % (1 if no_sync else 2))
    if not sequential:
        while True:
            now = datetime.datetime.now()
            record = now.isoformat(sep=';', timespec='seconds')
            click.echo('Scanning at %s...' % (now.isoformat(sep=' ', timespec='seconds')), err=True)
            for i in range(1, 13):
                record += ';'
                if str(i) in channels:
                    value = talker.query('R%d' % (i))
                    if not value.isdigit() or int(value) < 0 or int(value) > 65535:
                        raise TalkerException
                    record += value
                    if deplete != 0:
                        talker.command('D0')
                        time.sleep(deplete / 1000)
                        talker.command('D%d' % (1 if no_sync else 2))
            click.echo(record)
            time.sleep(interval)
    else:
        while True:
            click.echo('Scanning at %s...' % (datetime.datetime.now().isoformat(sep=' ', timespec='seconds')), err=True)
            for i in range(1, 13):
                if str(i) not in channels:
                    continue
                now = datetime.datetime.now()
                record = now.isoformat(sep=';', timespec='seconds')
                record += ';' * i
                value = talker.query('R%d' % (i))
                if not value.isdigit() or int(value) < 0 or int(value) > 65535:
                    raise TalkerException
                record += value
                record += ';' * (12 - i)
                if deplete != 0:
                    talker.command('D0')
                    time.sleep(deplete / 1000)
                    talker.command('D%d' % (1 if no_sync else 2))
                click.echo(record)
                time.sleep(interval)


def main():
    '''Application entry point.'''
    try:
        cli()
    except TalkerException:
        click.echo('Communication error occurred!', err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
