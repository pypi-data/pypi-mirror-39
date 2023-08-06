py_pushover_simple
==================

This is a very simple python pushover wrapper for sending quick messages from command line scripts.

## Installation Instructions

1. Download from PyPi:
    
        python3 -m pip install py_pushover_simple

2. Add it to your script:

        from py_pushover_simple import pushover
    
        def send_message(message):
            p = pushover.Pushover()
            p.user = 'user_key'
            p.token = 'app_token'
    
            p.sendMessage(message)
    

For a working demo, see
[ippush.py](https://git.sr.ht/~mjorgensen/ip_push/tree/master/ippush.py)
from the [ip_push](https://git.sr.ht/~mjorgensen/ip_push/) project.

## Debugging

`py_pushover_simple` has some simple debugging features:

For a full list of arguments:

    $ python -m py_suchover_simple.pushover -h
    usage: pushover.py [-h] [-u <string>] [-t <string>]
    
    optional arguments:
      -h, --help   show this help message and exit
      -u <string>  pushover user token
      -t <string>  pushover app token

## Documentation

Documentation lives at https://man.sr.ht/~mjorgensen/py_pushover_simple

## Contributors

* Matthew Jorgensen

## License

This project is licensed inder the terms of the MIT license.
