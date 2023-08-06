# <img src="https://github.com/pip-services/pip-services/raw/master/design/Logo.png" alt="Pip.Services Logo" style="max-width:30%"> <br/> Basic portable abstractions for Python

This framework is a part of [Pip.Services](https://github.com/pip-services/pip-services) project.
It provides basic building blocks that can be used to implement non-trivial business logic in applications and services.

The key difference of this framework is a portable implementation across variety of different languages. 
Currently it supports Java, .NET, Python, Node.js, Golang. The code provides reasonably thin abstraction layer 
over most fundamental functions and delivers symmetric implementation that can be quickly ported between different platforms.

All functionality is decomposed into several packages:

- **Commands** - Commanding and Eventing patterns
- **Config** - configuration framework
- **Convert** - portable soft value converters
- **Data** - data value objects and random value generators
- **Errors** - portable application errors
- **Refer** - component referencing framework
- **Reflect** - portable reflection helpers
- **Run** - execution framework
- **Validate** - data validators

Quick Links:

* [Downloads](https://github.com/pip-services3-python/pip-services3-commons-python/blob/master/doc/Downloads.md)
* [API Reference](https://pip-services3-commons-python.readthedocs.io/en/latest/index.html)
* [Building and Testing](https://github.com/pip-services3-python/pip-services3-commons-python/blob/master/doc/Development.md)
* [Contributing](https://github.com/pip-services3-python/pip-services3-commons-python/blob/master/doc/Development.md/#contrib)

## Acknowledgements

The initial implementation is done by **Sergey Seroukhov**. Pip.Services team is looking for volunteers to 
take ownership over Python implementation in the project.
