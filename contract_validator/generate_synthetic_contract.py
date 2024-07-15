from faker import Faker
import os

# Initialize Faker instance
faker = Faker()

# Create directories if they don't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Generate synthetic data
num_samples = 1000  # Adjust as needed
for i in range(num_samples):
    contract_text = f"""
    1. Services
    The Provider, {faker.company()}, agrees to perform the services described in Schedule A (the “Services”).

    2. Payment
    The Client, {faker.company()}, agrees to pay the Provider the amount of {faker.currency()} {faker.random_number(digits=5)} (the “Payment”).

    3. Term of Agreement
    This Agreement shall commence on {faker.date_this_year()} and shall continue in effect until {faker.date_between(start_date='+1y', end_date='+5y')} (the “Term”).

    4. Confidentiality
    The Provider agrees to hold in confidence and not to disclose to any third party any Confidential Information received from the Client, {faker.company()}.

    5. Termination
    This Agreement may be terminated by either party upon thirty (30) days written notice to the other party. The notice must be sent to {faker.address()}.

    6. Governing Law
    This Agreement shall be governed by and construed in accordance with the laws of the State of {faker.state()}. Any disputes arising from this agreement shall be resolved in the courts located in {faker.city()}, {faker.state()}.

    7. Signature
    IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
    Provider: {faker.name()}
    Client: {faker.name()}
    """

    label = faker.random_element(elements=['valid', 'invalid'])  # Simulating valid or invalid contracts

    # Save the contract text to a file
    filename = os.path.join(data_dir, f'contract_{i}.txt')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(contract_text.strip())

    with open(os.path.join(data_dir, 'labels.txt'), 'a') as file:
        file.write(label + '\n')

print(f"Generated {num_samples} synthetic contracts in '{data_dir}'.")
