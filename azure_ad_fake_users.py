import faker
import random
import string
import csv
from pathlib import Path

# https://pynative.com/python-generate-random-string/
def password_generator(password_length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(password_length))

# function to create a single dictionary object with user fields populated with data from faker library
# required to provide FQDN domain name
def user_generator(domain):
    user = faker.Faker()
    fqdn = domain
    first_name = user.first_name()
    last_name = user.last_name()
    name = (first_name + ' ' + last_name)
    username = first_name[0] + last_name[:] + '@' + fqdn
    initial_password = password_generator(10)
    block_sign_in = 'No'
    job_title = user.job()
    department = ''
    usage_location = 'United States'
    street_address = user.street_address()
    state = user.state_abbr()
    country = "United States"
    office = ''
    city = user.city()
    zipcode = user.zipcode_in_state(state)
    office_phone = user.phone_number()

    user_profile = {
        'Name [displayName] Required': name,
        'User name [userPrincipalName] Required': username.lower(),
        'Initial password [passwordProfile] Required': initial_password,
        'Block sign in (Yes/No) [accountEnabled] Required': block_sign_in,
        'First name [givenName]': first_name,
        'Last name [surname]': last_name,
        'Job title [jobTitle]': job_title,
        'Department [department]': department,
        'Usage location [usageLocation]': usage_location,
        'Street address [streetAddress]': street_address,
        'State or province [state]': state,
        'Country or region [country]': country,
        'Office [physicalDeliveryOfficeName]': office,
        'City [city]': city,
        'ZIP or postal code [postalCode]': zipcode,
        'Office phone [telephoneNumber]': office_phone
    }

    return user_profile

def user_csv_generator(domain, number_of_users):
    user_list = []

    for i in range(0, number_of_users):
        user_list.append(user_generator(domain))

    header = []
    for key in user_list[0].keys():
        header.append(key)

    file_path = Path.cwd() / "azure_ad_test_users.csv"
    with file_path.open(mode='w', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=header)
        csv_writer.writeheader()
        for row in user_list:
            csv_writer.writerow(row)
        print(f"File created at {file_path}")


# example
user_csv_generator('example.net', 50)

# TODO: add csv.writerow() code for Azure template check in first column/row 'version:v1.0'