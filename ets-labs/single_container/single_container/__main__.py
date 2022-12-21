import sys

from dependency_injector.wiring import Provide, inject

from .services import UserService, AuthService, PhotoService
from .containers import Container

'''
Define the main function, which accepts variable number of args from CLI

E.g.
python -m example user@example.com secretPassword photo.jpg

When the main function is run,
1. The UserService checks if the user has an account,
2. Then AuthService authenticates the user with the given user and password,
3. Then finally the PhotoService uploads the photo

Dependency Injection is achieved through wiring.

Wiring is achieved via three steps:
1. Wrapping the function which requires dependency injection with @inject
2. Inserting dependency place markers to the function, e.g. def method(bar: bar = Provide[Container.bar])
3. Specifying which modules/packages requires the Container with .wire(modules=[__name__])


'''
@inject # indicates that dep inj is required in main()
def main(
        email: str,
        password: str,
        photo: str,
        user_service: UserService = Provide[Container.user_service],
        auth_service: AuthService = Provide[Container.auth_service],
        photo_service: PhotoService = Provide[Container.photo_service],
) -> None:
    user = user_service.get_user(email)
    auth_service.authenticate(user, password)
    photo_service.upload_photo(user, photo)

if __name__ == "__main__":
    container = Container()
    container.init_resources()
    # provide container to this file so that it can be accessed by @inject 
    container.wire(modules=[__name__]) 

    main(*sys.argv[1:])
    
  

        
