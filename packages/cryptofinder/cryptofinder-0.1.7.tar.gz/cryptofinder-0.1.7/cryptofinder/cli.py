from .config import Config, APP_ENV
from .controller import Controller
from .logger import Logger
import builtins
import click
import json

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--market-cap', default=(0.0, 250000.0), show_default=True, nargs=2, type=float, help='Market cap range.', metavar='<float[]>')
@click.option('--avail-supply', default=(0.0, 50000000.0), nargs=2, show_default=True, type=float, help='Available supply range.', metavar='<float[]>')
@click.option('--avail-supply-ratio', default=0.5, show_default=True, help='This * total supply >= circulating supply.', metavar='<float>')
@click.option('--day-volume', default=(0.0, float('inf')), show_default=True, nargs=2, type=float, help='Daily volume range.', metavar='<float[]>')
@click.option('--day-volume-ratio', default=0.02, show_default=True, help='This * market cap >= day volume.', metavar='<float>')
@click.option('--force', default=False, is_flag=True, help='Force coin instance updates.')
@click.option('--drop', default=False, is_flag=True, help='Drop database.')
@click.option('--offline', default=False, is_flag=True, help='Disable ticker updates.')
@click.option('--save', default=False, is_flag=True, help='Save results to JSON file.')
@click.option('-v', '--verbose', default=False, is_flag=True, help='Enable verbose logging.')
@click.option('-q', '--quiet', default=False, is_flag=True, help='Disable stdout logging.')

def cli(**kwargs):
  Config.validate()

  builtins.ui = {k: v for k, v in kwargs.items() if v}
  builtins.logger = Logger(ui)

  Controller.main()
  
  logger.info('')
  logger.info("Exiting.")

def main():
  cli(obj={})

if __name__ == '__main__':
  main()