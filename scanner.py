import click
from network_scanner import NetworkScanner, Protocol

@click.command()
@click.argument('url')
@click.argument('type', type=click.Choice(['http', 'https', 'ftp', 'ssh']))
def process_url(url, type):
  scanner = NetworkScanner(url)
  if type == 'http':
    result_http = scanner.scan(Protocol.HTTP)
  elif type == 'https':
    result_https = scanner.scan(Protocol.HTTPS)
  elif type == 'ftp':
    result_ftp = scanner.scan(Protocol.FTP)
  elif type == 'ssh':
    result_ssh = scanner.scan(Protocol.SSH)


if __name__ == "__main__":
  process_url()
