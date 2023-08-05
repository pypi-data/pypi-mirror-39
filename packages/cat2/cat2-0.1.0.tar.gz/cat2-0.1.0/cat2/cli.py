import os
import re
import click

from cat2 import Cat2


@click.command()
@click.argument('file_path')
@click.option('-q', 'query', help="Query word")
@click.option('-f', 'line_from', type=int, help="Line from")
@click.option('-t', 'line_to', type=int, help="Line to")
def cli(file_path, query, line_from, line_to):

	rows, columns = os.popen('stty size', 'r').read().split()
	
	click.echo()

	cat2_file = Cat2(file_path)

	if line_from:
		if line_from < 0:
			cat2_file_len = len(cat2_file)
			line_from = cat2_file_len+line_from

	for i, line in enumerate(cat2_file):
		i = i+1
		
		if line_from:
			if i < line_from:
				continue

		no = i
		if i <= 9:
			no = f'0{i}'
		click.secho(f' {no}. ', bg='blue', bold=True, nl=False)

		if query:
			if query in line:
				line_parts = line.split(query)
				line = click.style(line_parts[0], bg='red')
				line += click.style(query, bg='yellow', fg='black')
				line += click.style(line_parts[1], bg='red')
				line += click.style(' '*(int(columns)-len(line)), bg='red')
		
		click.echo(f'  {line}  ')

		if line_to:
			if i > line_to:
				break
		
	click.echo()