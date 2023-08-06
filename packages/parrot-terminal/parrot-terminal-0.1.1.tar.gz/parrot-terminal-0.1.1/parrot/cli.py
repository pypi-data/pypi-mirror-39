import time
import click
from pkg_resources import resource_filename


def get_file_content(file):
    with open(file, 'r') as f:
        return str(f.read())

frame = []
for i in range(10):
    frame_path = resource_filename(__name__, 'data/{}.txt'.format(str(i)))
    content = get_file_content(frame_path) + "\n\nPARTY OR DIE\n"
    frame.append(content)

ALL_COLORS = 'black', 'red', 'green', 'yellow', 'blue', 'magenta', \
             'cyan', 'white', 'bright_black', 'bright_red', \
             'bright_green', 'bright_yellow', 'bright_blue', \
             'bright_magenta', 'bright_cyan', 'bright_white'


@click.command()
@click.option('--fast', is_flag=True, help='TURN IT UP')
def cli(fast):
    """PARTY OR DIE"""
    FPS = 20
    if fast:
      FPS = 30

    for i in range(1000):
        time.sleep(1/FPS)
        click.clear()
        click.echo(click.style(frame[i % 10], fg=ALL_COLORS[i%len(ALL_COLORS)]))
