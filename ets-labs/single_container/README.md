# Application example (single container)

This example shows how you can create an application using a single declarative container. Using a single declarative container is a good choice for small or moderate size application. For building a large application refer to Application example (multiple containers).

We build an example micro application following the dependency injection principle. It consists of several services with a domain logic. The services have dependencies on database & AWS S3.

![UML Class Diagram](docs/uml.png)

## Getting started

Make sure that the venv is activated, pip is updated, packages are installed and cd into ets-labs/single_container within the venv.

## Running main
`python -m single_container user@example.com secret photo.jpg`

This should return:

```
[DEBUG] [single_container.services.UserService]: User user@example.com has been found in database
[2022-12-21 15:59:22,162] [DEBUG] [single_container.services.AuthService]: User user@example.com has been successfully authenticated
[2022-12-21 15:59:22,162] [DEBUG] [single_container.services.PhotoService]: Photo photo.jpg has been successfully uploaded by user user@example.com
```


## Running tests
`pytest single_container/tests.py --cov=single_container`

This should return:
```
single_container/tests.py .                                                                 [100%]

---------- coverage: platform darwin, python 3.8.6-final-0 -----------
Name                             Stmts   Miss  Cover
----------------------------------------------------
single_container/__init__.py         0      0   100%
single_container/__main__.py        14     14     0%
single_container/containers.py      13      0   100%
single_container/services.py        29     14    52%
single_container/tests.py           14      0   100%
----------------------------------------------------
TOTAL                               70     28    60%

```
