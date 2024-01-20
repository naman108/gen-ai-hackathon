import click
import requests
import time

@click.command()
def check_notifications():
    while True:
        click.echo("waiting for notifications...")
        response = requests.get('/nurse/notifications')
        if response.status_code == 200:
            data = response.json()
            if data:
                click.echo(f"Notification: {data}")
                break

        time.sleep(5)  # Wait for 5 seconds before checking again

    

if __name__ == '__main__':
    check_notifications()
