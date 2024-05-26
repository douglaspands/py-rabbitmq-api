# PY RABBITMQ API
Exemplo de projeto com utilização do Python com RabbitMQ.

## Dependencias
- Python ~3.12
- Docker ~24.0.5

## Como usar
### Instalar dependencias
```sh
poetry install
```

### Arquivo `.env`
Criar arquivo `.env` na raiz do projeto com os seguintes parametros:
```
queue_host=localhost
queue_port=5672
queue_name=queue.default
queue_exchange=topic.default
queue_routing_key=routing_key.default
queue_username=guest
queue_password=guest
``` 

### Iniciar RabbitMQ
```sh
docker compose -f rabbitmq.yaml up -d
```

### Iniciar ConsumerWorker
```sh
python app.py consumer start --workers 3
```
> `--workers 3` é a quantidade de threads de leitura da fila.


### Gerador de massa:
```sh
python app.py producer sends "teste send" --count 100
```
