import os

# Configuration
base_dir = "deep_test"
depth = 50   # Number of nested folders
filename = "test.txt"
file_content = "You made it to the deepest folder!"

# Create the nested folders
current_path = base_dir
for i in range(1, depth + 1):
    current_path = os.path.join(current_path, f"folder_{i}")
    os.makedirs(current_path, exist_ok=True)

# Create the file at the end
file_path = os.path.join(current_path, filename)
with open(file_path, "w") as f:
    f.write(file_content)

print(f"Created file at: {file_path}")
