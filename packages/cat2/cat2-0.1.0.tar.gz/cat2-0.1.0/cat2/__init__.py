class Cat2:

	def __init__(self, file_path):
		self._file_format = None
		self._file_path = file_path
		self._f = None

	def __iter__(self):
		if self._file_format is None:
			with open(self._file_path, 'r') as f:
				try:
					f.read(32)
					self._file_format = ''
				except UnicodeDecodeError:
					self._file_format = 'b'

		self._f = open(self._file_path, f'r{self._file_format}')
		return self

	def __next__(self):
		if self._file_format:
			return next(self._f)
		else:
			return next(self._f).replace('\n','')

	def __len__(self):
		for i, _ in enumerate(self): pass
		self._f.close()
		return i+1
