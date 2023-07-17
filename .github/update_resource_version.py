import sys
import json

if len(sys.argv) < 3:
    print("Usage: python update_resource_version.py <properties_file> <version>")
    exit(1)

properties_file = sys.argv[1]
version = sys.argv[2]

with open(properties_file, "r") as f:
    data = json.load(f)

data["version"] = version

with open(properties_file, "w") as f:
    json.dump(data, f, indent=4)
