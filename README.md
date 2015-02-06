# Welcome to Pypethon

This is a repository for the [PyTennessee](https://www.pytennessee.org) 2015 talk [Write a Toy Language in Python 3](https://www.pytennessee.org/schedule/presentation/50/). For an even gentler introduction to the concepts in this tutorial, you may enjoy working through [Romnomnom](https://github.com/tsclausing/romnomnom) first.

The README below includes a quickstart tutorial. Please see [the wiki](https://github.com/tsclausing/pypethon/wiki) for documentation.

```bash
$ python3 pypethon
> 
> 11  # Pypethon has integers and comments.
11
> 
> = val 11  # Variables can hold values!
> val
11
>
> # And values can flow through pipes!! 
> val | times | 4 | minus | 3 | inc 
42
> 
> # We can even hold a pipe in a variable.
> |= minus6 minus | 6
> 
> # And run a value through it!
> 17 | minus6  # (°□°)
11
>
```

Yep! That's Pypethon.
