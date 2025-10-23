# Pythonic Web!
Pythonic Web is a concept of a server-rendered, pure Python web server.

The idea of creating a web server in Python, that is server-rendered came
from a frustration with PHP. I really don't like that syntax.

Python is a lovely language, and I want to create websites using it. 
So I'm making this dream to become true.

This is a side project and **DEFINITELY** is not _production ready_. 
Maybe one day this turns into a wonderful tool. I hope.

## The concept

The point of the project is to create pages using a good mix of HTML and 2 
special tags that will be replaced in rendering time: ```<python>``` and ```<py>```

I don't want to make a new, strange language syntax, it's just 2 new tags 
inside your html and Python working as you expected.

### The _\<python>_ tag

The \<python> tag is meant to be a block of Python code. Where you can access 
global variables, make declarations and make imports.
```html
<ul>
    <python>
        from random import randint
        for i in range(5):
            write(f"<li>{randint(1, 100)}</li>")
    </python>
</ul>
```

Using the function ```write(content)``` you can generate HTML that will 
replace the tag.

### The _\<py>_ tag

The \<py> tag is meant to simple access previously declared variables and 
functions
```html
<python>
... more code here
    
title = "Awesome Title!"  
    
... other code here
</python>
... tags here

    <h1><py>title</py></h1>

... tags there
```

The content of \<py> tag is directly evaluated to string and replaced in the HTML.

### Running the server

Now the project is LITERALLY just Python 3.13. After cloning the project 
and having Python 3.13 installed. You can:

```
$ sudo python3 start.py
```
\* ```sudo``` is required to use port 80.
