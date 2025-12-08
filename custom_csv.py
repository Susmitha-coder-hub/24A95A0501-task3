# custom_csv.py
from typing import List, TextIO, Iterable

# ----------------- CSV Reader -----------------
class CustomCsvReader:
    """A streaming CSV reader that yields rows as lists of strings."""

    def __init__(self, file: TextIO):
        self.f = file
        self.eof = False

    def __iter__(self):
        return self

    def __next__(self) -> List[str]:
        if self.eof:
            raise StopIteration

        row = []
        field_chars = []
        in_quotes = False

        while True:
            ch = self.f.read(1)
            if ch == '':
                # EOF
                self.eof = True
                if in_quotes:
                    raise ValueError("Unexpected EOF inside quoted field")
                if field_chars or row:
                    row.append(''.join(field_chars))
                    return row
                raise StopIteration

            if ch == '"':
                if not in_quotes:
                    if field_chars:
                        field_chars.append('"')
                    else:
                        in_quotes = True
                else:
                    next_ch = self.f.read(1)
                    if next_ch == '"':
                        field_chars.append('"')
                    else:
                        in_quotes = False
                        if next_ch != '':
                            try:
                                self.f.seek(self.f.tell() - 1)
                            except Exception:
                                if next_ch not in [',', '\n', '\r']:
                                    field_chars.append(next_ch)
                continue

            if in_quotes:
                field_chars.append(ch)
                continue

            if ch == ',':
                row.append(''.join(field_chars))
                field_chars = []
                continue
            if ch == '\n':
                row.append(''.join(field_chars))
                return row
            if ch == '\r':
                next_ch = self.f.read(1)
                if next_ch != '\n':
                    try:
                        self.f.seek(self.f.tell() - 1)
                    except Exception:
                        pass
                row.append(''.join(field_chars))
                return row

            field_chars.append(ch)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.f.close()
        except Exception:
            pass

# ----------------- CSV Writer -----------------
class CustomCsvWriter:
    """Write rows (lists of strings) to a file in CSV format."""

    def __init__(self, file: TextIO):
        self.f = file

    def _needs_quote(self, s: str) -> bool:
        return ',' in s or '"' in s or '\n' in s or '\r' in s

    def _quote_field(self, s: str) -> str:
        if '"' in s:
            s = s.replace('"', '""')
        if self._needs_quote(s):
            return f'"{s}"'
        return s

    def writerow(self, row: List[str]):
        processed = [self._quote_field('' if cell is None else str(cell)) for cell in row]
        self.f.write(','.join(processed) + '\n')

    def writerows(self, rows: Iterable[List[str]]):
        for r in rows:
            self.writerow(r)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.f.close()
        except Exception:
            pass
