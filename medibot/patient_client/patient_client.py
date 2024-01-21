import click
import requests


def call_patient_api(msi_card_number, symptoms):
    url = "http://134.190.135.240:5000/patient"  # replace with your actual API URL
    data = {
        "msi_card_number": msi_card_number,
        "symptoms": symptoms
    }
    response = requests.post(url, json=data)
    return response.json()  # assuming the response is in JSON format


@click.command()
def cli():
    print("Greetings! \n")

    msi_card_number = click.prompt('Please enter your MSI card number', type=str)
    symptoms = click.prompt('Please describe your symptoms', type=str)

    print("\n")

    user_input = input("Are you satisfied with the data provided? Type 'yes' or 'no': \n")

    while True:

        if user_input == "yes":

            print("\n")
            click.echo(f'|MSI Card Number: {msi_card_number}\n|Symptoms: {symptoms}')
            response = call_patient_api(msi_card_number, symptoms)
            click.echo("your priority is " + str(response['priority']))
            break

        else:

            print("\n")
            msi_card_number = click.prompt('Please Reenter your MSI card number', type=str)
            symptoms = click.prompt('Please describe your symptoms again', type=str)
            click.echo(f'|MSI Card Number: {msi_card_number}\n|Symptoms: {symptoms}')
            response = call_patient_api(msi_card_number, symptoms)
            click.echo("your priority is " + str(response['priority']))
            break

            print("\n")


if __name__ == '__main__':
    cli()