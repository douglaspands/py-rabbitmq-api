# PY RABBITMQ API
Exemplo de projeto com utilização do Python com RabbitMQ.  
Frameworks utilizados:
- Pika
- Pydantic
- Typer
- SQLAlchemy (Em desenvolvimento)

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

### Iniciar worker (Consumer)
```sh
python app.py consumer start --workers 3 --retry 2
```
> `--workers 3` é a quantidade de threads de leitura da fila;  
> `--retry 2` é a quantidade de tentativas antes de disparar o callback de falha;  

### Gerador de massa (Producer)
```sh
python app.py producer sends "teste send" --count 100
```

## RabbitMQ Management
[http://localhost:15672](http://localhost:15672)
```yaml
Username: guest
Password: guest
```
