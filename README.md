[Permalink](http://arcane-cove-8701.herokuapp.com "Permalink to ")

# 

 
### A web service, written in Python with Flask, which performs basic SoundEx encoding.

#### *Oren Leiman* 

Follow [this link][1] for the encoding front end.  
Alternatively, curling the following URL:
  
>http://arcane-cove-8701.herokuapp.com/encode/[insert name here]

will return a JSON packet containing the original name and its SoundEx  
### Example

> $ curl -i http://arcane-cove-8701.herokuapp.com/Konstantin  
> >HTTP/1.1 200 OK  
> >Content-Type: text/html; charset=utf-8  
> >Date: Mon, 31 Dec 2012 02:23:35 GMT  
> >Server: Werkzeug/0.8.3 Python/2.7.2  
> >Content-Length: 40  
> >Connection: keep-alive  
> >  
> >{"raw": "KONSTANTIN", "soundex": "K523"}  
>

 [1]: http://arcane-cove-8701.herokuapp.com/encode 