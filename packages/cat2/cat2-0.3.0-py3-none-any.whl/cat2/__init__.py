import os
import ntpath


class Cat2:
	"""Open file class"""

	def __init__(self, file_path: str, line_from: int=None, line_to: int=None):
		self._line_from = line_from
		if self._line_from:
			self._line_from -= 1
		self._line_to = line_to
		if self._line_to:
			self._line_to -= 1
		self._file_format = None
		self._file_path = file_path
		self._lines_count = None
		self._f = None
		self._i = 0

	def __iter__(self) -> "Cat2":
		"""Discover file format,
		set counter,
		set line from in file."""

		self._i = 0
		self._f = self._open_file()

		if self._line_from:
			for _ in range(int(self._line_from)):
				next(self._f)
			self._i = self._line_from

		return self

	def __next__(self) -> str:
		"""Watch for line to,
		set counter,
		return line."""

		if self._line_to:
			if self._i > self._line_to:
				raise StopIteration

		self._i += 1

		if self._file_format == 'b':
			return next(self._f)
		else:
			return next(self._f).replace('\n','')

	def __len__(self) -> int:
		"""Count lines."""

		if self._lines_count is None:
			with self._open_file() as f:
				self._lines_count = len(f.readlines())

		return self._lines_count

	def _open_file(self):
		"""Open the file"""

		if os.path.isdir(self._file_path):
			filename = ntpath.basename(self._file_path)
			raise Cat2Exception(f'{filename} is a directory!')

		if self._file_format is None:
			with open(self._file_path, 'r') as f:
				try:
					f.read(32)
					self._file_format = ''
				except UnicodeDecodeError:
					self._file_format = 'b'

		return open(self._file_path, f'r{self._file_format}')

	@property
	def line_number(self):
		"""Format number with leading zeros."""

		i = self._i
		number_of_digits_current_line = len(str(i))
		number_of_digits_file_len = len(str(len(self)))
		
		def add_zero(no, cl, fl):
			if fl > cl:
				no = f'0{no}'
				return add_zero(no, cl+1, fl)
			else:
				return no

		no = add_zero(str(i), 
					  number_of_digits_current_line,
					  number_of_digits_file_len)

		return no

	@property
	def is_bytes(self):
		"""Is it a bytes file"""

		return self._file_format == 'b'


class Cat2Exception(Exception):
	pass
