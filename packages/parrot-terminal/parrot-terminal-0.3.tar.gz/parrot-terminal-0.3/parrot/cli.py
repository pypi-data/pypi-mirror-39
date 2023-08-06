import time
import click
from os import listdir
from pkg_resources import resource_filename

INDEXES = sorted(listdir(resource_filename(__name__, 'frames')))
def make_frame(index):
    file_path = resource_filename(__name__, 'frames/' + index)
    with open(file_path, 'r') as f:
        frame = str(f.read()) + "\n\nPARTY OR CTRL+C!!!\n"
    return frame
FRAMES = list(map(make_frame, INDEXES))
COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']


@click.command()
@click.version_option()
@click.option('--up', is_flag=True, help='TURN DOWN FOR WHAT?')
def cli(up):
    """PARTY OR DIE!!!"""
    fps = 30 if up else 20
    sleeper = 1/fps

    def select(arr, it):
        return arr[it % len(arr)]

    def draw_frame_at_time(time):
        frame = select(FRAMES, time)
        color = select(COLORS, time)
        colorized_frame = click.style(frame, fg=color)
        click.echo(colorized_frame)
        return colorized_frame

    def prepare_next_frame():
        click.clear()
        time.sleep(sleeper)

    def animate(time):
        prepare_next_frame()
        draw_frame_at_time(time)
        animate(time + 1)

    def start_animation():
        animate(0)        

    try:
        start_animation()
    except:
        click.Abort()
