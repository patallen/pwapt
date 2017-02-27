# PWAPT

[![Build Status](https://travis-ci.org/patallen/pwapt.svg?branch=master)](https://travis-ci.org/patallen/pwapt)
[![Codecov](https://img.shields.io/codecov/c/github/patallen/pwapt.svg)](https://img.shields.io/codecov/c/github/patallen/pwapt.svg)

PWAPT is a light profiler for python web applications. A.K.A Python Web Application Profiling Toolkit

![profiler](https://secure.netflix.com/us/boxshots/tv_sdp_s/70180077.jpg)

#### Installation
`$ mkvirtualenv pwaptenv`

`$ pip install pip install git+git://github.com/patallen/pwapt`


#### Implementation
- PWAPT requires a simple config. For now, just a dict passed into pwapt.config.from_dict()
- The config should look as follows:

```python
pwapt_config = {
    'SAMPLING_INTERVAL': 0.0005,  # How often the stack will be sampled in minutes
    'HANDLER_DUMP_INTERVAL': 2 * 60,  # How often the handler will dump store in seconds
    'HANDLER_MIDDLEWARE_CLASSES': [
        ...
    ],
    'SAMPLER_MIDDLEWARE_CLASSES': [
        ...
    ]
}
```

- To set up, all you need to do is instanciate  a Pwapt object, pass a config, and call Pwapt's `run`.
- This snippet should be placed above the app invocation.

```python
profiler = Pwapt()
profiler.config.from_dict(pwapt_config)
profiler.run()
```
- This does currently require `gevent` and its monkey patching.
