This file is to provide vital information about the libraries that come with WalScript

There are two types of libraries: *.walrus and *.wp (walpy). *.walrus libraries are written in WalScript, whereas *.wp is written in a mix between WalScript and Python.
Math.wp
=======
A set of usefule mathematical functions, constants, and things
Constants
---------
```
pi
e
phi
```
(ALL THINGS BELOW THIS POINT NOT YET IMPLEMENTED)
Functions
---------
```
abs(x) //Get the absolute value of x
round(x) //round x
ceil(x) //nearest integer greater than x
floor(x) //nearest integer less than x
sqrt(x) //Square root of x
root(x, y) //xth root of y
sin(x) //Sine of x
cos(x) //Cosine of x
tan(x) //Tangent of x
asin(x) //Sine^-1 of x
acos(x) //Cosine^-1 of x
atan(x) //Tangent^-1 of x
```

String.walrus
=============
A set of string manipulation and examination functions
Constants:
----------
```
low      //lower case alphabet
caps     //upper case alphabet
Letters  //low+caps
digits   //Numbers
Alphanum //Letters+digits
ascii    //ASCII
```
String Manipulation:
--------------------
```
upper(s)     //Full caps of s
lower(s)     //Lower case of s
sub(b, e, s) //get substring b-e of s
```
