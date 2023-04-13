import requests
from bs4 import BeautifulSoup

# Get the options of the dropdown menu
def get_dropdown_options():
    # Send a GET request to the web application
    response = requests.get("http://localhost:8888")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the dropdown menu element
    dropdown = soup.find("select", {"name": "dropdown_menu"}) # TODO Replace Name

    # Get all the options of the dropdown menu
    options = [option.text for option in dropdown.find_all("option")]

    return options

# Select an option from the dropdown menu
def select_dropdown_option(selected_option):
    # Send a POST request to the web application with the selected option as a parameter
    response = requests.post("http://localhost:8888", data={"dropdown_menu": selected_option}) # TODO Replace Name

    # Check if the request was successful
    if response.status_code == 200:
        print(f"{selected_option} option selected successfully")
    else:
        print("Failed to select option")

# Press the start button on the web application
def press_start_button():
    # Send a POST request to the web application to start the application
    response = requests.post("http://localhost:8888", data={"start_button": "pressed"}) # TODO Replace Name

    # Check if the request was successful
    if response.status_code == 200:
        print("Application started successfully")
    else:
        print("Failed to start application")

# Main function
def main():
    # Get the options of the dropdown menu
    options = get_dropdown_options()
    print("Dropdown menu options:")
    for option in options:
        print(option)

    # Select an option from the dropdown menu
    selected_option = options[0] # Replace this with the option you want to select
    select_dropdown_option(selected_option)

    # Press the start button on the web application
    press_start_button()

if __name__ == "__main__":
    main()