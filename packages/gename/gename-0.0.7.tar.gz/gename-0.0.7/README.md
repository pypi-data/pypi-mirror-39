## Summary
This package is for anyone who wants to speculate the gender given a first
name. There is no magic involved, the speculate method simply does a local
database lookup.


## Usage
~~~
>>> from gename import Gender
>>> gender = Gender()
>>> gender.speculate('Bertrand')
'M'
>>> gender.speculate('Simone')
'F'
>>> gender.speculate('Unicorn')
'U'
~~~

U is for Unknown.

