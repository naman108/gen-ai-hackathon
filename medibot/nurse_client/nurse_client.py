import json
import click
import zmq
import time

@click.command()
def check_notifications():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://134.190.135.240:5555")  # Bind to the address where you'll receive messages
    
    notifications = []  # List to store received messages

    while True:
        click.echo("waiting for notifications...")
        data = socket.recv_json()  # Receive a message
        if data:
            # click.echo(json.dumps(data, indent=4))
            # Print each item in the conflicting_queue with its index
            for i, item in enumerate(data['conflicting_queue'], 1):
                click.echo(f"{i}. {json.dumps(item, indent=4)}")
                
            index = click.prompt("where should the new patient be placed?", type=int) - 1

            socket.send_json({'index': index})

if __name__ == '__main__':
    check_notifications()
