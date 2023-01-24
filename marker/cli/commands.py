import click
from marker.core import Extractor, Simulator
import importlib
import pandas as pd
import importlib.util
import sys


@click.command(help='Extract movie name from images')
@click.option('-f', '--folder', type=str, help="the folder containing images")
@click.option('-p', '--post-process-file', type=str, default=None, help="the post process file for customization")
@click.option('-o', '--output', type=str, default='list.xlsx', help="the output file for the text extracted")
@click.option('-s', '--star', type=int, default=4, help="assign a star to each movie")
def extract(folder, post_process_file, output, star):
    if post_process_file:
        spec = importlib.util.spec_from_file_location("helper", post_process_file)
        helper = importlib.util.module_from_spec(spec)
        sys.modules["helper"] = helper
        spec.loader.exec_module(helper)
        print(helper.post_process)
        post_process = helper.post_process
    else:
        post_process = None

    extractor = Extractor(folder, post_process=post_process)
    extractor.extract(output, star)


@click.command(help='Sync your watch list with Douban')
@click.option('-f', '--file', type=str, default='list.xlsx')
def sync(file):
    df = pd.read_excel(file)

    simulator = Simulator()
    simulator.login()

    for _, row in df.iterrows():
        star = row['score']
        name = row['name']
        print(f"Marking {name}")
        try:
            simulator.search(name)
            simulator.mark(star)
        except Exception as e:
            print(f'Exception occurs for {name}, reason: {e}')
