# Py-thumbnail

What is Py-thumbnail?
---------------------

Py-thumbnail is a quick thumbnail creator for python codes. You can get an overview of the available functions, for/while loops and if conditions without even running the code.

Suppose you have the following python file:

```python
class someclass:
    def __init__(self):
        self.a = 10

    def do_something(self):
        for i in range(len(self.a)):
            if i == 2:
                print(i)

    def do_something_else(self, num):
        while self.a < 100:
            self.a += num
```


Here is a small example to show what Py-thumbnail could do (Python 3):

```python
from thumbnail import pythumbnail

file = pythumbnail('some_file.py')
file.scan()
print(file.tree)
```

The output will look like:

```python
'File some_file.py()'
    'class someclass()'
        'def __init__(self)'
        'def do_something(self)'
            'for i in range(len(self.a))'
                'if[i,2] LOGIC: [==]'
        'def do_something_else(self,num)'
            'while[self.a,100] LOGIC: [<]'
```
