# API consumer and processor

This codebase presents some guidelines on how to integrate 
an external API on a reliable manner.

## Some notes:
#### Tests:
Generally speaking, integration to external APIs requires two levels of verification:
Verifying that the API returns expected results when accessed according to its documentation. I used Marshmallow as a schema validator to validate returned values concerning API verification.
Verifying app functionality after API verification. I used a mixture of mocking and stubbing to verify the business logic that happens inside the app, mainly nested_by_films method of People endpoint.

Integration testing against a sandbox server that replicates the actual API server is missing. In this case, instead of mocking external call responses, which is mainly done by using stub_request method of request_mock fixture, we can call the external sandbox server to check against the HTTP response code,  HTTP headers in the response, and the payload.

#### Caching:
I used cachetools to cache the converted response data on list and retrieve methods of APIEndpoints, 
but a more extensible and cleaner approach exists too: Adding caching functionality inside **APIRequester.request** method.

  

The idea is simply defining a global cache policy using template design pattern for **APIRequester** class, which can be overwritten by the caller. inside **APIRequester.request** method, before the invocation of **self._client.retry_request,** it'll check the request against the cache policy and if a response was found in the cache policy it'll return it instead of calling the actual API. This is a work in progress on '**feat/caching-middleware**' branch.

## Getting Up and Running Locally

you can use docker to run the app on a container or install and run it locally.


### 1- install using docker
#### Prerequisites
- Docker; if you don’t have it yet, follow the installation instructions;
- Docker Compose; refer to the official documentation for the installation guide.

#### How to install:
1- Build the Stack:
Open a terminal at the project root and run the following for local development:
```bash
$ docker-compose build 
```
2- Run the docker-compose:
```bash
$ docker-compose up
```
### 2- install locally without docker
Installing the app on your local machine, you can run tests and 
test coverage commands directly. 

#### How to install:
2-1: Install poetry:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
2-2: Installing dependencies:
```bash
make install
```
2-3: Run server:
```bash
make server
```
#### how to run tests:
- Run test without overage report:
```bash
make test
```
- Run test with overage report:
```bash
make coverage
```



