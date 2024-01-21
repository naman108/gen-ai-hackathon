import click
import zmq
import time

@click.command()
def check_notifications():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5555")  # Bind to the address where you'll receive messages

    while True:
        click.echo("waiting for notifications...")
        data = socket.recv_string()  # Receive a message
        if data:
            click.echo(f"Notification: {data}")
            break

        time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == '__main__':
    check_notifications()
