

<p align="center">
  <a href="https://github.com/MohamadNematizadeh/website_PlantsAI">
<img src="https://github.com/MohamadNematizadeh/Shenas/blob/main/logo/logo_no_name.png?raw=true" alt="Logo"  height="100">
  </a>
  <h2 align="center"> 
Shenas </h2>

  <p align="center" ><img src = "https://skillicons.dev/icons?i=fastapi,py,docker,redis,vue,ts,nodejs"></p>

  <p align="center">
   The electronic identity authentication system (eKYC) uses modern technologies to authenticate users quickly, securely and online.👨‍🦰
   

## How to Install :
```
pip install -r requirements.
```

# How to Run  :

1. Run redis 
  ```
  docker pull redis
  docker run --name some-redis -d -p 6379:6379 redis
  ```

2. Run celery tasks
```
celery -A  celery_tasks worker --loglevel=ERROR -E
```

3. run mongo 
```
docker pull mongo
docker  run --name some-mongo -d -p 27017:27017 mongo
```

4. Run main APi
```
uvicorn app:app 
```
