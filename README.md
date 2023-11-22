# FastAPI-Raft

Distributed systems play a crucial role in addressing the challenges of scalability, fault tolerance, and availability in modern computing environments. This project focuses on implementing the Raft consensus algorithm [(following the paper)][raft-paper] to achieve data consistency and system availability in a distributed environment suitable for applications requiring distributed data storage and retrieval. Raft is a consensus algorithm for managing a replicated log. Nodes maintain logs and operate in leader, candidate, or follower states, monitored throughout the network. The system utilises Docker for node replication. Hosting will be on the Google Cloud Platform for easy deployment and monitoring. Nginx can be taken into consideration once we get the leader’s information after the successful consensus.

## Weaknesses of our approach
- Single Leader: Raft relies on a single leader for updates, which can become a bottleneck for performance.
- Availability during Partitions: For now, our system isn’t capable of demonstrating the networking partitioning problem, though theoretically, it is capable of introducing data consistency when the network is healed.
- Latency: Leader election and log replication introduce some latency, impacting performance in write-intensive applications.

## Future Work
- Fetch the Leader’s IP address via container ID and update the Nginx configuration with the same.
- Demonstrate the network partitioning problem.
- Scale up replicas after clusters have already started.
- Maintain the leader’s status on the removal of one or more replicas.


## Code

1. Tech stack used: ASGI + Starlette + FastAPI + Pydantic.
2. Pytest for testing.
3. Black for linting.
4. Pipenv for virtual environment management and dependencies management.

## Dependencies

A detailed list of dependencies can be found in `Pipfile`.

* dnspython: Tools for use with Docker DNS
* FastAPI: Web framework
* Pydantic: JSON validation
* Pytest: Testing
* requests: HTTP library
* Starlette: ASGI framework
* uvicorn: ASGI web server

## Installation

To run this project please install `docker` and `docker-compose` and run
```sh
docker-compose up --build
```

Alternatively, you can complete the setup by:

Install dependencies and development dependencies:

``` sh
python -m pip install pipenv
pipenv install --dev
pipenv shell
```

You can then run the test suite against the service.

``` sh
pytest
```

## Running

The project is designed to be run with `Docker` and
`docker-compose`. The reason for this is that the discovery mechanism works with DNS. All nodes share a service domain name, e.g. `node`. By DNS lookup for `node` the service receives the IP addresses of all individual replicas of the
service.

Another small FastAPI webservice is contained in the directory `monitor/`. Its purpose is to collect status data from all replicas of the main `app` and display it on a webpage.

## Run and test the project
In order to run the project, simply type
```sh
docker-compose up --build
```

To check the details of running services, open a new tab and type
```sh
docker ps
```

To pause a container, type
```sh
docker pause <container_id>
```

### Configuration

Available Configuration Variables `app/config.py` (as Environment Variables) are listed below. These values can be changed as per user's requirement.

| Environment Variable              | Description | Default Value |
|:----------------------------------|:------------|--------------:|
| FASTAPI_TITLE                     | The name of the application. | `` |
| FASTAPI_DESCR                     | A description for display in OpenAPI/SwaggerDoc. | `<redacted for brevity>` |
| FASTAPI_SCHEM                     | The path where the OpenAPI schema is available. | `/openapi.json` |
| FASTAPI_DOCS                      | The path where SwaggerDoc is available. | `/docs` |
| API_PREFIX                        | Path prefixed before all API-routes | `/api` |
| ROOT_PATH                         | Path where uvicorn will serve the app. | ` ` |
| APP_NAME                          | Name of the application (will be used in error messages e.g.) | `consensus-cluster-service` |
| LOGGING                           | Logging level | `DEBUG` |
| ELECTION_TIMEOUT_LOWER_MILLIS     | Lower bound for election timeout in milliseconds | `3000` |
| ELECTION_TIMEOUT_UPPER_MILLIS     | Upper bound for election timeout in milliseconds | `5000` |
| HEARTBEAT_REPEAT_MILLIS           | How fast a Leader will send heartbeats to all nodes | `500` |


[raft-paper]: https://raft.github.io/