
import hashlib
import json
import copy


# Generate a SHA-256 fingerprint for a medication record
def generate_hash(record):

    # Convert the dictionary into consistent JSON
    record_json = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":")
    )

    # Convert JSON into bytes
    record_bytes = record_json.encode("utf-8")

    # Generate SHA-256 hash
    fingerprint = hashlib.sha256(record_bytes).hexdigest()

    return fingerprint


# 1. Create a sample medication record
original_record = {
    "patient_ref": "PAT-DEMO-001",
    "medication": "Metformin",
    "status": "Taken",
    "scheduled_time": "20:00",
    "version": 1
}


# 2. Generate the original fingerprint
original_hash = generate_hash(original_record)
# Generate the fingerprint again
repeated_hash = generate_hash(original_record)

print("\n===== REPEATABILITY TEST =====")
print("Original Hash:", original_hash)
print("Repeated Hash:", repeated_hash)

if original_hash == repeated_hash:
    print("SUCCESS: Same record produces the same fingerprint.")
else:
    print("ERROR: Fingerprints do not match.")

print("\n===== ORIGINAL MEDICATION RECORD =====")
print(json.dumps(original_record, indent=4))

print("\nOriginal SHA-256 Fingerprint:")
print(original_hash)


# 3. Create a modified copy
modified_record = copy.deepcopy(original_record)

modified_record["status"] = "Missed"


# 4. Generate the modified fingerprint
modified_hash = generate_hash(modified_record)

print("\n===== MODIFIED MEDICATION RECORD =====")
print(json.dumps(modified_record, indent=4))

print("\nModified SHA-256 Fingerprint:")
print(modified_hash)


# 5. Compare both fingerprints
print("\n===== INTEGRITY VERIFICATION =====")

if original_hash == modified_hash:
    print("VERIFIED: No changes detected.")
else:
    print("MISMATCH DETECTED: Record has been modified!")

# Experiment: Change only the scheduled time

time_test_record = copy.deepcopy(original_record)

time_test_record["scheduled_time"] = "21:00"

time_test_hash = generate_hash(time_test_record)

print("\n===== SINGLE FIELD CHANGE TEST =====")
print("Original Hash:", original_hash)
print("Changed Time Hash:", time_test_hash)

if original_hash != time_test_hash:
    print("SUCCESS: Changing the time also changes the fingerprint.")