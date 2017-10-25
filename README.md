# shijou.moe
Scripts and templates for shijou.moe

Requeriments:
- Python 3.6
- Flask
- Mutagen
- asyncio
- websockets

how to run:
- install uwsgi, nginx, python3
- new python3 venv, install requermients
- cp sample_config.ini config.ini, change as needed
- use shijoumoe config file for nginx
- cp app_uwsgi.ini into root folder
- launch main webapp: nohup uwsgi_python3 --ini app_uwsgi.ini &
- launch radio websocket script: nohup python3 watcher.py &