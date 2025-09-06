import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory,directory)

    if not full_path.startswith(working_directory):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

    if not os.path.isdir(full_path):
        print(f'Error: "{directory}" is not a directory')


    lines = []

    for name in os.listdir(full_path):
        path = os.path.join(full_path,name)
        size = os.path.getsize(path)
        is_dir = os.path.isdir(path)
        lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(lines)