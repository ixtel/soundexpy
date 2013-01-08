[Permalink](http://arcane-cove-8701.herokuapp.com "Permalink to")

#SoundExPy 
 
### A web service, written in Python with Flask, which performs basic SoundEx encoding.
### Please note that this is an attempt to implement SoundEx as a Markov Algorithm.

#### *Oren Leiman* 

Follow [this link][1] for the encoding front end.  

Alternatively, there is a small RESTful API available:   

##HTTP Verbs

###GET /encode/[name]
>Used for retrieving the SoundEx encoding of 'name'.   

#### Example

> $ curl -i http://arcane-cove-8701.herokuapp.com/Konstantin  
> >HTTP/1.1 200 OK  
> >Content-Type: application/json
> >Date: Mon, 31 Dec 2012 02:23:35 GMT  
> >Server: Werkzeug/0.8.3 Python/2.7.2  
> >Content-Length: 40  
> >Connection: keep-alive  
> >  
> >{"raw": "KONSTANTIN", "soundex": "K523"}  
>

 [1]: http://arcane-cove-8701.herokuapp.com/encode 
