from faker import Faker
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

fake = Faker()

def generate_data(file_name, num_addresses, target_percentage):
    try:
        los_angeles_count = int(num_addresses * target_percentage / 100)
        other_cities_count = num_addresses - los_angeles_count

        with open(file_name, "w") as file:
            # Generate addresses for Los Angeles
            for _ in range(los_angeles_count):
                name = fake.name()
                address = fake.address().replace('\n', '')
                city = "Los Angeles"
                state = fake.state_abbr()
                zipcode = fake.zipcode()
                full_address = f"{name}, {address}, {city}, {state} {zipcode}"
                file.write(full_address + '\n')

            # Generate addresses for other cities
            for _ in range(other_cities_count):
                name = fake.name()
                address = fake.address().replace('\n', '')
                city = fake.city()
                state = fake.state_abbr()
                zipcode = fake.zipcode()
                full_address = f"{name}, {address}, {city}, {state} {zipcode}"
                file.write(full_address + '\n')
    except Exception as e:
        print(f"Error writing to file: {e}")

def process_data(file_name, filter_condition):
    try:
        with open(file_name, "r") as file:
            for line in file:
                line = line.strip()
                if filter_condition(line):
                    address_parts = line.split(',')
                    address_length = len(address_parts[1].strip())
                    first_name = address_parts[0].split()[0].strip()
                    city = address_parts[2].strip()
                    yield address_length, first_name, city
    except FileNotFoundError:
        print(f"File {file_name} not found")


# Define a condition function using lambda
filter_condition = lambda line: "Los Angeles" or "New York" or "Chicago" or "Phoenix" in line

# Generate data to a file
file_name = "generated_data.txt"
num_addresses = 1000000
target_percentage = 30
generate_data(file_name, num_addresses, target_percentage)



print("LA addresses:")
for address_length, first_name, city in process_data(file_name, filter_condition):
    if city == "Los Angeles" or "New York" or "Chicago" or "Phoenix":
        print(f"{address_length}, {first_name}, {city}")


# Initialize counters and calculate statistics
address_lengths = []
first_names = []
cities = Counter()
for address_length, first_name, city in process_data(file_name, filter_condition):
    address_lengths.append(address_length)
    first_names.append(first_name)
    cities.update([city])


min_length = min(len(address_lengths), len(first_names))
address_lengths = address_lengths[:min_length]
first_names = first_names[:min_length]

# Count the occurrences of each name
name_counts = Counter(first_names)

# Get the 10 most common names
most_common_names = name_counts.most_common(10)

# Extract names and their frequencies
names = [name[0] for name in most_common_names]
frequencies = [name[1] for name in most_common_names]


# Create DataFrame
data = pd.DataFrame({
    'Address Length': address_lengths,
    'First Name': first_names,

})

if address_lengths:
    average_address_length = sum(address_lengths) / len(address_lengths)
    print("Average address length:", average_address_length)

    most_common_first_name = Counter(first_names).most_common(5)
    print("Most common first names:", most_common_first_name)

    unique_cities_count = len(cities)
    print("Unique cities count:", unique_cities_count)


    data = pd.DataFrame({'Address Length': address_lengths, 'First Name': first_names})



    plt.figure(figsize=(8, 6))
    sns.histplot(data=data, x='Address Length', bins=10, kde=True, color="blue")
    plt.axvline(average_address_length, color="red", linestyle="--", label="Average address length")
    plt.title("Histogram over addresse længde")
    plt.xlabel("Addresse længde")
    plt.ylabel("Densitet")
    plt.show(block=False)

    plt.figure(figsize=(10, 6))
    plt.bar(names, frequencies, color='skyblue')
    plt.title('Top 10 almindelige navne')
    plt.xlabel('Navne')
    plt.ylabel('Hyppighed')
    plt.xticks(rotation=45)
    plt.show()


else:
    print("No filtered addresses found")