from server.commands import consumer, producer
from server.core.cli import create_app


def main():
    app = create_app()
    app.add_typer(consumer.app)
    app.add_typer(producer.app)
    app()
