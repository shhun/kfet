# Site de la K-Fêt

## Architecture

1) Un serveur flask, qui sert un template kfet.html et une page /login pour pouvoir toggle l'état de la kfet après authentification
2) Un serveur websocket qui broadcast l'état de la kfet

## Configurer

- Dans `server.py`, pour contacter la websocket:
  * `IP`: l'addresse IP du serveur websocket
  * `PORT`: le port du serveur websocker
  * `secret_hash`: le sha256 du mot de passe souhaité
- Dans `websocket_server.py`:
  * `PORT`: le port du serveur websocket

Exporter l'application Flask, lancer la websocket puis lancer le serveur.
```
export FLASK_APP=/path/to/dir/server.py
python3 server.py & && flask run &
```

