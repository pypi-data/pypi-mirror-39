# walt is a "namespace package", shared by walt-client, walt-server, walt-node...
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
