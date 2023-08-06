# CliRAINBOW
Easily print colored text.

## Example usage
```python
>>> from clirainbow import Colorizer, RED, GREEN
>>> c = Colorizer()
>>> c.print('<hello> <world!>', RED, GREEN)
```

## Additional info

* If you want to insert a literal bracket, double it (e.g. write `<<` instead of `<`)
    * (this is the same behavior as Python's builtins)
* Angle brackets are used instead of the traditional curly brackets in order to prevent clashes with Python's builtin string formatting facilities


## Exceptions

At the moment, three possible exceptions may occur while using the library : 
1. A color bracket is opened, but never closed (`ColorBracketOpenedButNotClosed`)
2. More brackets than colors are given (`MoreBracketsThanColors`)
3. More colors than brackets are given (`MoreColorsThanBrackets`)

In each case, a readable error message is produced

## Disclaimer
Colors may not appear on certain systems (e.g., Windows) or with certain terminals.

## Dependencies
CliRAINBOW is built on top of colorama : https://github.com/tartley/colorama

## Future plans
* Generate code in `colors.py` with a script instead of at runtime
    * Allow code completion
    * Remove annoying error messages
* Add support for reusing colors by index, e.g. `c.print('<0:oh> <1:hai> <0:there>', colors.RED, colors.BLACK)`
    * Make it more similar to Python's `format`


