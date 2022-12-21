import logging.config
import sqlite3

import boto3
from dependency_injector import containers, providers

from . import services

'''
IOC Container

DeclarativeContainer is a class-based style of the providers definition.

You create the declarative container subclass, put the providers as attributes and create the container instance.

This is opposed to DynamicContainer, where providers can be defined at runtime.
'''
class Container(containers.DeclarativeContainer):

    '''
    Get configuration KV pairs from config.ini and store as Configuration Provider
    
    E.g. if config.ini has the following content:
    
    [aws]
    access_key_id = KEY
    
    and it is initialised as such:
    
    class Container(containers.DeclarativeContainer):
        config = providers.Configuration(ini_files=["config.ini"])
        
    then it can later be accessed by:
    
    Container().config.aws.access_key_id()
    '''
    config = providers.Configuration(ini_files=["config.ini"])


    '''
    A Resource Provider provides a component with initialization and shutdown.
    
    This is useful for logging, since you usually want to configure logging params e.g. Level.
     
    This is achieved by:
    1. Passing the fileConfig pointer from the logging package to the Resource Provider
        - This sets the fileConfig method as a function which must be when initialising
    2. Passing kwargs of fileConfig to Resource Provider
        - This allows the kwargs to be injected to fileConfig when initialising

    During runtime, this happens:
    1. Container().init_resources() invoked
    2. providers.Resource invokes logging.config.fileConfig and passes fname as kwarg
    3. logging can then be used as per normal
    
    Note:
    Container().shutdown_resources() is not necessary for logging, but may be relevant for a method pointer which returns a resource, e.g.
    
    def init_thread_pool(max_workers: int):
        thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        yield thread_pool
        thread_pool.shutdown(wait=True)
    
    class Container(containers.DeclarativeContainer):
        config = providers.Configuration()
        
        thread_pool = providers.Resource(
            init_thread_pool,
            max_workers=config.max_workers,
        )
    
    if __name__ == '__main__':
        container = Container(config={"max_workers": 4})

        container.init_resources() 

        thread_pool = container.thread_pool()
        thread_pool.map(print, range(10)) # do some work

        container.shutdown_resources() # shutdown thread pool


    '''
    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    
    '''
    Singleton provider provides single object. It memorizes the first created object and returns it on the rest of the calls. Singleton provider scope is tied to the container. Two different containers will provider two different singleton objects.
    
    Useful for creating a single client to act as an access point for external services.    
    '''

    database_client = providers.Singleton(
        sqlite3.connect,
        config.database.dsn,
    )

    s3_client = providers.Singleton(
        boto3.client,
        service_name="s3",
        aws_access_key_id=config.aws.access_key_id,
        aws_secret_access_key=config.aws.secret_access_key,
    )
    

    '''
    Factory provider creates new objects. 
    The first argument of the Factory provider is a class, a factory function or a method that creates an object.
    The rest of the Factory positional and keyword arguments are the dependencies. Factory injects the dependencies every time when creates a new object. The dependencies are injected following these rules:
    
        * If the dependency is a provider, this provider is called and the result of the call is injected.
        * If you need to inject the provider itself, you should use the .provider attribute.
        * All other dependencies are injected “as is”.
        * Positional context arguments are appended after Factory positional dependencies.
        * Keyword context arguments have the priority over the Factory keyword dependencies with the same name.
    
    E.g.
    
    class Photo:
        ...


    class User:
        def __init__(self, uid: int, main_photo: Photo) -> None:
            self.uid = uid
            self.main_photo = main_photo


    class Container(containers.DeclarativeContainer):

        photo_factory = providers.Factory(Photo)

        user_factory = providers.Factory(
            User,
            main_photo=photo_factory,
        )


    if __name__ == "__main__":
        container = Container()

        user1 = container.user_factory(1)
        # Same as: # user1 = User(1, main_photo=Photo())

        user2 = container.user_factory(2)
        # Same as: # user2 = User(2, main_photo=Photo())

        another_photo = Photo()
        user3 = container.user_factory(
            uid=3,
            main_photo=another_photo,
        )
        # Same as: # user3 = User(uid=3, main_photo=another_photo)
    
    '''

    user_service = providers.Factory(
        services.UserService,
        db=database_client,
    )

    auth_service = providers.Factory(
        services.AuthService,
        db=database_client,
        token_ttl=config.auth.token_ttl.as_int(),
    )

    photo_service = providers.Factory(
        services.PhotoService,
        db=database_client,
        s3=s3_client,
    )