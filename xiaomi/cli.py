# -*- coding: UTF-8 -*-
import logging
import click
import pretty_cron
import ast
import sys

if sys.version_info < (3, 4):
    print("To use this script you need python 3.4 or newer, got %s" %
          sys.version_info)
    sys.exit(1)

import xiaomi  # noqa: E402

_LOGGER = logging.getLogger(__name__)
pass_dev = click.make_pass_decorator(xiaomi.Device)


@click.group(invoke_without_command=True)
@click.option('--ip', envvar="Xiaomi_IP", required=False)
@click.option('--token', envvar="Xiaomi_TOKEN", required=False)
@click.option('-d', '--debug', default=False, count=True)
@click.pass_context
def cli(ctx, ip, token, debug):
    """A tool to command Xiaomi Device robot."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        _LOGGER.info("Debug mode active")
    else:
        logging.basicConfig(level=logging.INFO)

    # if we are scanning, we do not try to connect.
    if ctx.invoked_subcommand == "discover":
        return

    if ip is None or token is None:
        click.echo("You have to give ip and token!")
        sys.exit(-1)

    dev = xiaomi.Device(ip, token, debug)
    _LOGGER.debug("Connecting to %s with token %s", ip, token)

    ctx.obj = dev

    if ctx.invoked_subcommand is None:
        ctx.invoke(status)


@cli.command()
def discover():
    """Search for robots in the network."""
    xiaomi.Device.discover()


@cli.command()
@pass_dev
def status(dev):
    """Returns the state information."""
    res = dev.status()
    if not res:
        return  # bail out
    click.echo(res)
#    if res.error_code:
#        click.echo(click.style("Error: %s !" % res.error,
#                               bold=True, fg='red'))
#    click.echo(click.style("State: %s" % res.state, bold=True))
#    click.echo("Battery: %s %%" % res.battery)
#    click.echo("Fanspeed: %s %%" % res.fanspeed)
#    click.echo("Cleaning since: %s" % res.clean_time)
#    click.echo("Cleaned area: %s m²" % res.clean_area)
#    click.echo("DND enabled: %s" % res.dnd)
    # click.echo("Map present: %s" % res.map)
    # click.echo("in_cleaning: %s" % res.in_cleaning)


@cli.command()
@pass_dev
def consumables(dev):
    """Return consumables status."""
    res = dev.consumable_status()
    click.echo("Main brush:   %s (left %s)" % (res.main_brush,
                                               res.main_brush_left))
    click.echo("Side brush:   %s (left %s)" % (res.side_brush,
                                               res.side_brush_left))
    click.echo("Filter:       %s (left %s)" % (res.filter,
                                               res.filter_left))
    click.echo("Sensor dirty: %s" % res.sensor_dirty)


@cli.command()
@pass_dev
def start(dev):
    """Start."""
    click.echo("Starting: %s" % dev.start())

@cli.command()
@pass_dev
def aqi(dev):
    """Return consumables status."""
    res = dev.getInfo()
    click.echo("Current AQI: %s" % res.aqi)

@cli.command()
@pass_dev
def temperature(dev):
    """Return indoor temperature."""
    res = dev.getInfo()
    click.echo("Current Temperature: %s" % res.temperature)

@cli.command()
@pass_dev
def humidity(dev):
    """Return humidity."""
    res = dev.getInfo()
    click.echo("Current humidity: %s" % res.humidity)


@cli.command()
@pass_dev
def spot(dev):
    """Start spot cleaning."""
    click.echo("Starting spot cleaning: %s" % dev.spot())


@cli.command()
@pass_dev
def pause(dev):
    """Pause cleaning."""
    click.echo("Pausing: %s" % dev.pause())


@cli.command()
@pass_dev
def stop(dev):
    """Stop."""
    click.echo("Stop: %s" % dev.stop())


@cli.command()
@pass_dev
def home(dev):
    """Return home."""
    click.echo("Requesting return to home: %s" % dev.home())


@cli.command()
@click.argument('cmd', required=False)
@click.argument('start_hr', required=False)
@click.argument('start_min', required=False)
@click.argument('end_hr', required=False)
@click.argument('end_min', required=False)
@pass_dev
def dnd(dev, cmd, start_hr, start_min, end_hr, end_min):
    """Query and adjust do-not-disturb mode."""
    if cmd == "off":
        click.echo("Disabling DND..")
        print(dev.disable_dnd())
    elif cmd == "on":
        click.echo("Enabling DND %s:%s to %s:%s" % (start_hr, start_min,
                                                    end_hr, end_min))
        click.echo(dev.set_dnd(start_hr, start_min, end_hr, end_min))
    else:
        x = dev.dnd_status()[0]
        click.echo("DND %02i:%02i to %02i:%02i (enabled: %s)" % (
            x['start_hour'], x['start_minute'],
            x['end_hour'], x['end_minute'],
            x['enabled']))


@cli.command()
@click.argument('speed', type=int, required=False)
@pass_dev
def fanspeed(dev, speed):
    """Query and adjust the fan speed."""
    if speed:
        click.echo("Setting fan speed to %s" % speed)
        dev.set_fan_speed(speed)
    else:
        click.echo("Current fan speed: %s" % dev.fan_speed())


@cli.command()
@click.argument('timer', required=False, default=None)
@pass_dev
def timer(dev, timer):
    """Schedule Device, times in GMT."""
    if timer:
        raise NotImplementedError()
        # dev.set_timer(x)
        pass
    else:
        timers = dev.timer()
        for idx, timer in enumerate(timers):
            color = "green" if timer.enabled else "yellow"
            #  Note ts == ID for changes
            click.echo(click.style("Timer #%s, id %s (ts: %s)" % (
                idx, timer.id, timer.ts), bold=True, fg=color))
            print("  %s" % timer.cron)
            min, hr, x, y, days = timer.cron.split(' ')
            # hr is in gmt+8 (chinese time), TODO convert to local
            hr = (int(hr) - 8) % 24
            cron = "%s %s %s %s %s" % (min, hr, x, y, days)
            click.echo("  %s" % pretty_cron.prettify_cron(cron))


@cli.command()
@click.argument('stop', required=False)
@pass_dev
def find(dev, stop):
    """Finds the robot."""
    if stop:
        click.echo("Stopping find calls..")
        click.echo(dev.find_stop())
    else:
        click.echo("Sending find the robot calls.")
        click.echo(dev.find())


@cli.command()
@pass_dev
def map(dev):
    """Returns the map token."""
    click.echo(dev.map())


@cli.command()
@pass_dev
def cleaning_history(dev):
    """Query the cleaning history."""
    res = dev.clean_history()
    click.echo("Total clean count: %s" % res.count)
    click.echo("Cleaned for: %s (area: %s m²)" % (res.total_duration,
                                                  res.total_area))
    click.echo()
    for idx, id_ in enumerate(res.ids):
        for e in dev.clean_details(id_):
            color = "green" if e.complete else "yellow"
            click.echo(click.style(
                "Clean #%s: %s-%s (complete: %s, unknown: %s)" % (
                    idx, e.start, e.end, e.complete, e.unknown),
                bold=True, fg=color))
            click.echo("  Area cleaned: %s m²" % e.area)
            click.echo("  Duration: (%s)" % e.duration)
            click.echo()


@cli.command()
@click.argument('cmd', required=True)
@click.argument('parameters', required=False)
@pass_dev
def raw_command(dev, cmd, parameters):
    """Run a raw command."""
    params = []
    if parameters:
        params = ast.literal_eval(parameters)
    click.echo("Sending cmd %s with params %s" % (cmd, params))
    click.echo(dev.raw_command(cmd, params))


if __name__ == "__main__":
    cli()
