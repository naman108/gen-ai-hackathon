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
         
            if len(notifications) >= 2:
                top_2_patients = notifications[:2]
                click.echo(f"Top 2 elements: {top_2_patients}")

                # Let the user choose which patient to display and remove
                user_choice = click.prompt("Choose 1 or 2", type=int)

                if user_choice in [1, 2]:
                    chosen_patient = top_2_patients[user_choice - 1]
                    click.echo(f"Chosen element: {chosen_patient}")

                    # Remove the chosen patient from the list
                    notifications.remove(chosen_patient)
                    click.echo(f"Removed chosen patient from the list.")

                    # Send back the unchosen patient to the source
                    unchosen_patient = top_2_patients[1] if user_choice == 1 else top_2_patients[0]
                    socket.send_string(unchosen_patient)
                    click.echo(f"Sent back unchosen patient: {unchosen_patient}")

        time.sleep(5)  # Wait for 5 seconds before checking again


if __name__ == '__main__':
    check_notifications()
