import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    
    try:
        # Handle the case where directory is None (list working_directory itself)
        if directory is None:
            target_path = working_directory
        else:
            # Create full path by joining working_directory with the relative directory
            target_path = os.path.join(working_directory, directory)
        
        # Normalize paths to handle ".." and other relative components
        working_directory_abs = os.path.abspath(working_directory)
        target_path_abs = os.path.abspath(target_path)
        
        # Check if target_path is within working_directory boundaries
        if not target_path_abs.startswith(working_directory_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Check if the target path exists
        if not os.path.exists(target_path):
            return f'Error: "{directory}" does not exist'
        
        # Check if the target path is a directory
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'
        
        # Get directory contents
        try:
            entries = os.listdir(target_path)
        except PermissionError:
            return f'Error: Permission denied accessing "{directory}"'
        except OSError as e:
            return f'Error: Cannot access "{directory}": {str(e)}'
        
        # Build the result string
        result_lines = []
        for entry in sorted(entries):  # Sort for consistent output
            entry_path = os.path.join(target_path, entry)
            try:
                # Get file size and directory status
                stat_info = os.stat(entry_path)
                file_size = stat_info.st_size
                is_dir = os.path.isdir(entry_path)
                
                result_lines.append(f" - {entry}: file_size={file_size} bytes, is_dir={is_dir}")
            except OSError as e:
                result_lines.append(f" - {entry}: Error getting info: {str(e)}")
        
        return "\n".join(result_lines)
    
    except Exception as e:
        return f"Error: Unexpected error: {str(e)}"
    
    