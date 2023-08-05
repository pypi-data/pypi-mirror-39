# dst-server-deploy
A Python package for generating server files for use with [Don't Starve Together Docker Images](https://github.com/fairplay-zone/docker-dontstarvetogether).

The image requires docker engine and docker compose to be installed on the host system. 

This script is indended to be run in the directory in which you want to store the server data to generate most generic servers. 
If you need to tune the server after generation, look [here](https://github.com/fairplay-zone/docker-dontstarvetogether/blob/develop/docs/configuration.md) for reference.

## How to use
### Package Installation
```console
pip install dst-server-deploy
```

### Build Server Files
```console
dst-server-deploy
```
Command line arguments may be used in place of answering all configuration questions. To see arguments, use
```console
dst-server-deploy -h
```

### Deploy Server (requires docker engine and docker-compose)
```console
docker-compose up -d
```

## Known Issues / Notes
* BE AWARE: This will overwrite any docker-compose.yml file you have in a directory.
* This assumes assume you are only running one cluster on your machine. If you are running clusters, you will need to adjust the ports accordingly.
* This is just intended to help generate a moderate amount of server framework to aid users who are new to docker or this image. It is not meant to address all use cases.

# Reference files.
For an example of the files which may be read into the script, look [here](/reference_files/).

## Contribution
Do you want to contribute to the project? Check out the [contribution guide](/CONTRIBUTING.md).
