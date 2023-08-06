import os
import uuid

import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-translate')
chrome_options.add_argument('--window-size=1280,780')
chrome_options.add_argument('--enable-font-antialiasing')
chrome_options.add_argument('--font-cache-shared-handle[6]')


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx, *args, **kwargs):
    if ctx.invoked_subcommand is None:
        click.echo('Use --help command')


@cli.command('screenshot')
@click.option('--p', prompt='Path to screenshot', type=click.Path(exists=True))
@click.option('--url', prompt='URL')
def make_screenshot(p, url):
    filename = os.path.join(p, '%s.png' % uuid.uuid4())

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.get_screenshot_as_file(filename)
    driver.quit()
    return filename
