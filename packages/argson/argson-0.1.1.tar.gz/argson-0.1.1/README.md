# argson
Arguments from JSON

Deploy arguments into a python program from a JSON config file

## Installation
`python3 setup.py install`

Currently not supporting Python 2. Should work on all Python 3 versions. Tested with Python 3.7.1

## Basic usage
**config/arguments.json**
```
[
  {
    "flags": ["--string-to-print"]
  }
]
```
**config/defaults.json**
```
{
  "string_to_print": "foo"
}
```
**main.py**
```
import argson

arguments = argson.parse_file_and_arguments()
print(arguments.string_to_print)
```

`$ python main.py # -> foo`

`$ python main.py --string bar # -> bar`

## Documentation
**argson.parse_file_and_arguments**

Used to automatically parse the arguments file, self file and defaults file, generating an object with the flags from the arguments file

*Arguments*:

| Argument  | Type | Default | Description |
| - | - | - | - |
| config_file | str | config/arguments.json | where arguments are read |
| self_file | str | config/self.json | configurations for [argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html#argumentparser-objects) |
| defaults_file | str | config/defaults.json | default values for arguments |
| working_dir | str | os.getcwd() | where the program will look for files to load |
| no_builtins | bool | False | disables built-in flags |
| verbose | bool | False | disables error messages |

*Returns*: object with attributes from `config_file` flags

**argson.parse_config_file**

Used when there is need to manipulate the instance of `ArgumentParser` and the array of remaining arguments to parse

*Arguments*: same as `argson.parse_file_and_arguments`

*Returns*: Tuple[ArgumentParser, List[string]]. The instance of ArgumentParser and a list of the remaining arguments to be parsed. If the return value is assigned like `argument_parser, remaining_args = argson.parse_config_file()` the remaining args can be then parsed as in `arguments = argument_parser.parse_args(remaining_args)`, which is basically what `parse_file_and_arguments` does.

**config_file**

A json file containing an array of objects with at least one key called `flags`. Those are the flags with which the program will be called in "hyphen-case" starting with `--`, like in the example. Extra keys can be passed to express the flag behaviour or help string that will be displayed when the program is called with `--help`. Those are the same attributes that can be passed to [ArgumentParser.add_argument](https://docs.python.org/3/library/argparse.html#the-add-argument-method)

**self_file**

A json file containing information about the main ArgumentParser instance. Those are the same attributes supported by [argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html#argumentparser-objects)

**defaults_file**

A json file with the default values of the flags in `snake_case`. That is, if an argument has a flag `string-to-parse`, the default value must be read as `string_to_parse`. Refer to the example above.

### why decouple configs_file and defaults_file?
It is best to decouple those files so we can programatically select the defaults source, maintaining the same configurations for the flags. That is sometimes necessary when deploying scripts that have different defaults when running in development and in production environments.

### Contributing

* fork and clone this repo
* install pipenv
* `pipenv install`
* code like there is no tomorrow
* submit PR
* ??
* we profit together

Open for suggestions!
