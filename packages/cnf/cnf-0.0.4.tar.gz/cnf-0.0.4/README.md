CNF is short for Conjunctive Normal Form, which is a way of grouping logical statements; namely, but grouping or statements together separated by and statements:

```
(a or b or ...) and (x or y or...) and ...
```

For simplicity, let us refer to each statement as a "filter", as most likely one will be applying CNF to some data to find what passes the statements.

Currently, we implement a filter in `python3` via the `dict` type:

```
{
  'logic':    a string which is either 'and' or 'or'
  'lambda':   a lambda function to be applied to something
  'name':     a name which can help with keeping things clear
}
```

Thus given a `list` of such filters, one can call:

```
cnf.apply(cnf.group(filters), *lambda_args)
```
