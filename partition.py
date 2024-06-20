# Function to partition the DeviceDatabase.jsonl file
def partition_jsonl(file_path, partition_size=500):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Create the first partition with the first 500 lines
    with open("DeviceDatabase_first_500.jsonl", "w") as f:
        f.writelines(lines[:partition_size])

    # Create the second partition with the remaining lines
    with open("DeviceDatabase_remaining.jsonl", "w") as f:
        f.writelines(lines[partition_size:])


# Path to the original JSONL file
file_path = "./DeviceDatabase.jsonl"

# Partition the file
partition_jsonl(file_path)
