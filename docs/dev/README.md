## 개발 환경

## Docker image
- `docker pull ibjsw/ucs:0.21`
- `docker run -it -d -p 8000:8000 --name ucs ibjsw/ucs:0.21 /bin/bash -c "/root/settings/serviceRunner.sh"`
  - 서버의 8000 포트는 개방되어 있어야 합니다.
- `docker exec -it /bin/bash ucs`
- `cd $WD`
- `./auto_init.sh`
- `./run_server.sh`
- http://[yourIP]:8000 로 접속
