[![Build Status](https://travis-ci.com/JakeMakesStuff/ParseThoseArgs.svg?branch=master)](https://travis-ci.com/JakeMakesStuff/ParseThoseArgs)

# ParseThoseArgs
A extremely light Python library (written in mainly C) in order to parse arguments, designed for chatbot libraries.

## Usage
The argument parser can be initialised with the following:
```python
from parsethoseargs import ArgParser
parser = ArgParser(<text>, [ignore_quotes (defaults to False)])
```

In order to get the next argument from it, simply call `next` with the parser as a argument. The parser will raise `StopIteration` when all arguments have been parsed:
```python
arg_count = 1
while True:
    try:
        print("Argument {}: {}".format(arg_count, next(parser)))
    except StopIteration:
        break
    arg_count += 1
```

If you want to get the remaining bit of the string being parsed, you can use the property `parser.remaining`.

The parser will split arguments at spaces unless there are quotes. If there are quotes, it will include everything (including spaces) inside of them. If there is one quote, everything after it will be a argument.
