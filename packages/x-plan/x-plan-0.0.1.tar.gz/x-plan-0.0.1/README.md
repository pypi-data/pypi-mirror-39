<h1 align = "center">:rocket: X-plan :facepunch:</h1>

---

## Install
```
pip install xplan
```

## `from xplan.iterable import *`
```python
@X
def xfunc1(x):
    _ = x.split()
    print(_)
    return _
@X
def xfunc2(x):
    _ = '>>'.join(x)
    print(_)
    return _

'I am very like a linux pipe' | xfunc1 | xfunc2
```
- xtqdm

    ![tqdm](pic/tqdm.png)

- xseries
- xdataframe
```python
iterable | xseries
iterable | xdataframe

0        I
1       am
2     very
3     like
4        a
5    linux
6     pipe
Name: iterable, dtype: object
```

- xcounts
- xsummary
```python
iterable | xcounts

counts               7
uniques              7
missing              0
missing_perc        0%
types           unique
Name: iterable, dtype: object

iterable | xsummary

am       1
very     1
linux    1
like     1
I        1
a        1
pipe     1
Name: iterable, dtype: int64
```

- xsort
- xmap
- xreduce
- xfilter
```python
iterable | xfilter(lambda x: len(x) > 1) | xmap(str.upper) | xsort | xreduce(lambda x, y: x + '-' + y)

'AM-LIKE-LINUX-PIPE-VERY'
```
- ...

