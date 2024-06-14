import os

def add_prefix_to_images(directory, prefix):
    # Check if the provided directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return

    # List all files in the directory
    files = os.listdir(directory)
    
    # Process each file in the directory
    for filename in files:
        # Check if the file is an image (common extensions can be expanded)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Construct the full file path
            old_path = os.path.join(directory, filename)
            # Create the new filename by adding the prefix
            new_filename = prefix + filename
            new_path = os.path.join(directory, new_filename)
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed {old_path} to {new_path}")

# Example usage:
directory = 'C:/Users/hp/Desktop/rename'  # replace with your directory
prefix = 'web1_'  # replace with your desired prefix
add_prefix_to_images(directory, prefix)