import os
import json

if len(os.argv) < 3:
    print("Usage: python update_resource_version.py <properties_file> <version>")
    exit(1)

properties_file = os.argv[1]
version = os.argv[2]

with open(properties_file, "r") as f:
    data = json.load(f)

data["version"] = version

with open(properties_file, "w") as f:
    json.dump(data, f, indent=4)
