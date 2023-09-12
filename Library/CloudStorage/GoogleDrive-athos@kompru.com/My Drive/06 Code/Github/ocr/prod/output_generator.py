
import csv
import pickle
import os
from ean_validator import validate_ean, fabricate_ean  # <-- Importing fabricate_ean
import subprocess  # <-- Import subprocess to run external script

# Run ocr1 script
print("Running ocr1...")
subprocess.run(["python", "ocr1.py"])  # <-- Run the ocr1 script
print("ocr1 finished.")

# Load distinct_13_digits from a file (automatically read after ocr1 runs)
print("Loading distinct_13_digits.pkl...")
with open('distinct_13_digits.pkl', 'rb') as f:
    distinct_13_digits = pickle.load(f)
print("Loaded distinct_13_digits.pkl.")

# Ensure the "eans_validation" folder exists
folder_path = "eans_validation"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Load or initialize the counter for the CSV filename
counter_filename = os.path.join(folder_path, "counter.txt")
if os.path.exists(counter_filename):
    with open(counter_filename, "r") as f:
        counter = int(f.read().strip())
else:
    counter = 0

# Increment the counter
counter += 1

# Save the new counter value for future runs
with open(counter_filename, "w") as f:
    f.write(str(counter))

# Load distinct_13_digits from a file
with open('distinct_13_digits.pkl', 'rb') as f:
    distinct_13_digits = pickle.load(f)

# Validate each 13-digit sequence and save the results
ean_results = {}
true_count = 0
false_count = 0
fabricated_count = 0

for sequence in distinct_13_digits:
    is_valid = validate_ean(sequence)
    ean_results[sequence] = [is_valid, "Original"]

    if is_valid:
        true_count += 1
    else:
        false_count += 1

        # Create a fabricated sequence using the function from ean_validator
        fabricated_sequence = fabricate_ean(sequence)  # <-- Using imported function
        is_valid_fabricated = validate_ean(fabricated_sequence)
        ean_results[fabricated_sequence] = [is_valid_fabricated, "Fabricated"]

        if is_valid_fabricated:
            true_count += 1
        fabricated_count += 1


# Generate CSV file with results
csv_filename = f"eans_validation_{counter:03d}.csv"
csv_full_path = os.path.join(folder_path, csv_filename)
with open(csv_full_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["13-digit sequence", "Is Valid EAN", "Origin"])
    for sequence, (is_valid, origin) in ean_results.items():
        writer.writerow([sequence, is_valid, origin])

print(f"CSV file generated: {csv_full_path}")
print(f"Number of valid EANs: {true_count}")
print(f"Number of fabricated EANs: {fabricated_count}")


