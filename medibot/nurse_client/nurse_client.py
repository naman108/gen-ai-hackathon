import click
import zmq
import time

@click.command()
def check_notifications():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:5555")  # Bind to the address where you'll receive messages
    
    notifications = []  # List to store received messages

    while True:
        click.echo("waiting for notifications...")
        data = socket.recv_string()  # Receive a message
        if data:
            click.echo(f"Notification: {data}")
            # break
           
         # Process top 2 patients 
         # checks if the list has at least 2 patients
         