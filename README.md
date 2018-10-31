# SibirWTF 2018 (jury)

## Requriments

* docker
* docker-compose
* git

## Short manual for run

1. Clone project 
```
$ git clone git@gitlab.com:sibirctf/docker_jury.git /opt/wtf18.git
```

2. First you need build docker with jury:

```
$ cd /opt/wtf18.git/docker_jury && ./build_docker.sh
```

3. Start docker compose: 

```
cd /opt/wtf18.git && docker-compose up
```

## Usefull comamnd for cleanup

```
$ cd /opt/wtf18.git && sudo docker-compose rm
```

## Prepare

### Build special docker file with jury

```
$ cd /opt/wtf18.git/docker_jury && ./build_docker.sh
```

### Add new dependices for checkers

All dependencies needs for checkers please write to docker_jury/Dockerfile

After this:

```
$ cd /opt/wtf18.git/docker_jury && ./clean_docker.sh
$ cd /opt/wtf18.git/docker_jury && ./build_docker.sh
```

## Checker and config

`jury.d` will be mapped to `/usr/share/fhq-jury-ad/jury.d` (inside docker)

### Checkers

Checkers in here `jury.d/conf.d`

### Config 

Checkers and Teams in here `jury.d/conf.d/conf.ini`


