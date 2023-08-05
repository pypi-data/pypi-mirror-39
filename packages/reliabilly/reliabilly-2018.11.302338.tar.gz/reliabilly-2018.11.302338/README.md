![Reliabilly](reliabilly.png)  ![](hillbilly.png)
---


A micro-service scaffolding framework that provides high speed development velocity without sacrificing quality.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have installed Python 3.7 and run the setup.sh shell script.

```
./setup.sh
```

## Running the tests

All tests and tasks are automated using python invoke. 

### Run linting and unit tests

Run the following invoke command which is defaulted to linting and unit tests.

```
inv
```

### Integrations Tests

Integration tests are included but docs to come soon...

```
inv int
```

## Deployment

The services are intended to be containerized using docker with a cluster technology such as kubernetes.

## Built With

* [Nameko](https://github.com/nameko/nameko) - The web framework used
* [Docker](https://www.docker.com/) - Docker
* [Kubernetes](https://kubernetes.io/) - Kubernetes container orchestration

## Contributing

Coming soon...
Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

Coming soon... 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

