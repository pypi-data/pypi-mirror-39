import os
import re
import click

from cat2 import Cat2, Cat2Exception


@click.command()
@click.argument('file_path')
@click.option('-q', 'query', help="Query word")
@click.option('-f', 'line_from', type=int, help="Line from")
@click.option('-t', 'line_to', type=int, help="Line to")
def cli(file_path, query, line_from, line_to):

	rows, columns = os.popen('stty size', 'r').read().split()
	
	print('Analysing file...', end="\r")
	print('                 ')

	cat2_file = Cat2(file_path, line_from, line_to)
	
	try:
		if line_from is not None:
			if line_to:
				number_of_lines = line_to-line_from
			else:
				number_of_lines = len(cat2_file)-line_from
		else:
			number_of_lines = len(cat2_file)

		if number_of_lines > 200:
			click.secho(f'You are about to print {number_of_lines} lines.', fg='red')
			if not click.confirm('Do you want to continue?'):
				click.echo()
				return

		for line in cat2_file:
			click.secho(f' {cat2_file.line_number}. ', bg='blue', bold=True, nl=False)

			if query:
				if query in line:
					line_parts = line.split(query)
					line = click.style(line_parts[0], bg='red')
					line += click.style(query, bg='yellow', fg='black')
					line += click.style(line_parts[1], bg='red')
					line += click.style(' '*(int(columns)-len(line)), bg='red')
			
			click.echo(f'  {line}  ')

			if cat2_file.is_bytes:
				click.echo()
	except Cat2Exception as e:
		click.secho(str(e), fg='red')
		
	click.echo()