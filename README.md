# Cloud295 Server
1. Install Install Python3 and pip3
```
sudo apt-get update && \
  sudo apt-get install python3 && \
  python3 get-pip.py;
```

   - (Optional) Creaet virtual environments and activate it.
```
python3 -m venv venv
source venv/bin/activate
```

- Install Djando framework
```
python3 -m pip install Django
```

2. Start development server listening to all avaliable public IPs on port 8080

```
python manage.py runserver 0.0.0.0:8080
```


3. test cloudservice HTTP POST using commend line, replace ip address with your ip or localhoast
```
curl -d "label=test&echo=testing 2021" -X POST http://ip_address:8080/cloudservice/
```
