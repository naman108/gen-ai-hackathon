import click
import requests

def call_patient_api(msi_card_number, symptoms):
    url = "http://127.0.0.1:5000/patient"  # replace with your actual API URL
    data = {
        "msi_card_number": msi_card_number,
        "symptoms": symptoms
    }
    response = requests.post(url, json=data)
    return response.json()  # assuming the response is in JSON format

@click.command()
def cli():
    msi_card_number = click.prompt('Please enter your MSI card number', type=str)
    symptoms = click.prompt('Please describe your symptoms', type=str)
    click.echo(f'MSI Card Number: {msi_card_number}, Symptoms: {symptoms}')
    response = call_patient_api(msi_card_number, symptoms)
    click.echo(response)

if __name__ == '__main__':
    cli()