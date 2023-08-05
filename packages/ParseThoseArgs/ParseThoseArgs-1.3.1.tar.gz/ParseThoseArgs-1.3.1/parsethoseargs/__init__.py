import _parsethoseargs_c_parser
# Imports the C extension.


class ArgParserStructure:
    """Basically a mirror of the structure used in the C code."""
    __slots__ = ["ParsingString", "IgnoreQuotes", "HitAllArgs", "LastParse"]

    def __init__(self, parsing_string, ignore_quotes, hit_all_args, last_parse):
        self.ParsingString = parsing_string
        self.IgnoreQuotes = ignore_quotes
        self.HitAllArgs = hit_all_args
        self.LastParse = last_parse


class ArgParser:
    """The actual argument parser."""
    def __init__(self, text, ignore_quotes=False):
        self._structure = ArgParserStructure(text, int(ignore_quotes), 0, "")

    @property
    def all_args_parsed(self):
        return self._structure.HitAllArgs == 1

    @property
    def remaining(self):
        return self._structure.ParsingString

    def __next__(self):
        args = _parsethoseargs_c_parser.ArgParser_Next(
            self._structure.ParsingString, self._structure.IgnoreQuotes, self._structure.HitAllArgs
        )
        try:
            if args[2] == 1:
                raise StopIteration
            return args[3]
        finally:
            self._structure = ArgParserStructure(*args)
