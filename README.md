# Atlan Backend Internship Task

## REST API endpoints to manage a process

- Stop a process
- Resume a process

## Introduction

```shell

  It defines endpoints for managing a baseline upload behavior. In this the process can be halted, restarted.

```

## Approach

```shell

  After uploading a file and starting the process, the upload request if successful should return the process id
  of the task. If user want to stop the process should send the stop request using the process id. If user want to   
  resume the process after stopping it, will send request to resume api endpoint.

```
## Requirements

- Python 3.5+
- Flask

## To run

- Build the docker image using docker and then run it.

```shell

  docker build -t Assignment:latest
  docker run --name App -v$PWD/app:/app -p5000:5000 Assignment:latest


```
- Test the upload endpoint

```shell

  curl -F file=@C:\Users\nkthe\Downloads\UPES.png http://127.0.0.1:5000/api/upload
  curl  http://127.0.0.1:5000/api/resume?pid=HASH (SAMPLE REQUEST)

```


> TODO

- Implement a status endpoint to show running task of particular user.
- Test all scripts using unittest module.
- Map the process id of each upload task using a hash function.
