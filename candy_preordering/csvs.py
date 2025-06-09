from io import TextIOWrapper

class CSVFile:
    def _header_setup(self, file: TextIOWrapper):
      self.file = file
      file_content = file.read()
      condition = (len(file_content) == 0)
      if condition:
        temp = [f"{header}," for header in self.headers]
        content = "".join(temp)
        content = content[:len(content)-1]
        self.file.write(content)
        self.content = file_content
      else: 
        headers = (file_content.splitlines()[0]).split(",")
        self.headers = [h.strip() for h in headers]
        self.headers
        self.content = file_content

    def __init__(self, file, headers = []):
      self.headers = headers
      if type(file) is TextIOWrapper:
        self._header_setup(file)

      if type(file) is str:
        file = open(file, "r+")
        self._header_setup(file)

    def get_column(self, column: str) -> list[str]:
      index = self.headers.index(column)
      content = self._to_list()[1:]
      return [line[index] for line in content]

    def __str__(self):
      return self.content

    def __repr__(self):
      return self.content

    def __len__(self):
      return len(self.content.splitlines())

    def write_line(self, **kwargs: dict[str: str]):
          items = {header: kwargs[header] for header in self.headers} # Header mapped to value for every header in the self.headers list

          # Create a CSV row string
          items = [str(items[header]) for header in self.headers]

          to_append =  "\n" + ",".join(items)
          # Update in-memory content
          self.content += to_append
          

          # Write to the file
          self.file.seek(0, 2)  # Move to end of file
          self.file.write(to_append)
          self.file.flush()

    def _to_list(self) -> list[list[str]]:
      content = self.content.splitlines()
      content = [line.strip().split(",") for line in content]
      return content

    def __getitem__(self, index):
      return self._to_list()[index]

    def __iter__(self):
      return iter(self._to_list())

    def clear(self):
      self.file.seek(0)
      self.file.truncate(len(self.content.splitlines()[0]))
      self.file.flush()
      self.content = ""

    def get_headers(self) -> list[str]:
      return self.headers
    
    def repeats_per_item_in_column(self, column: str) -> dict[str: int]:
      if column not in self.headers:
        raise KeyError(f"Column {column} not in headers")
      col = self.get_column(column)
      repeats = dict()
      for i in col:
        if i in repeats.keys():
          repeats[i] += 1
        else:
          repeats[i] = 1
      
      return repeats

    def map_two_columns(self, key_column:str, value_column:str) -> list[tuple[str, str]]:
      if key_column not in self.headers:
        raise KeyError(f"Column {key_column} not in headers")
      if value_column not in self.headers:
        raise KeyError(f"Column {value_column} not in headers")
      key = self.get_column(key_column)
      value = self.get_column(value_column)
      return list(zip(key, value))

    def close(self):
      self.file.close()