import os
import py7zr
from datetime import datetime

def compress_directory_to_7z(directory_path, output_path=None):
    """
    Compresses all files in the given directory into a single 7z archive,
    excluding the most recently created file.
    
    Args:
    directory_path (str): Path to the directory containing files to compress.
    output_path (str, optional): Path where the 7z archive will be saved. 
                                 If not provided, uses the input directory.
    
    Returns:
    str: Path to the created 7z archive.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"The provided path '{directory_path}' is not a valid directory.")
    
    if output_path is None:
        output_path = directory_path
    elif not os.path.isdir(output_path):
        os.makedirs(output_path)
    
    # Get all files in the directory
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    
    if not files:
        print("No files found in the directory.")
        return None
    
    # Sort files by creation time (newest first)
    files.sort(key=lambda x: os.path.getctime(os.path.join(directory_path, x)), reverse=True)
    
    # Exclude the most recent file
    files_to_compress = files[1:]
    
    if not files_to_compress:
        print("No files to compress after excluding the most recent one.")
        return None
    
    # Create a timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"compressed_{timestamp}.7z"
    archive_path = os.path.join(output_path, archive_name)
    
    # Create the 7z archive
    with py7zr.SevenZipFile(archive_path, 'w') as archive:
        for file in files_to_compress:
            file_path = os.path.join(directory_path, file)
            archive.write(file_path, file)
    
    print(f"Compressed {len(files_to_compress)} files into {archive_name}")
    print(f"Excluded file: {files[0]}")
    
    return archive_path

# Example usage
if __name__ == "__main__":
    directory_to_compress = "/path/to/your/directory"
    compressed_archive = compress_directory_to_7z(directory_to_compress)
    if compressed_archive:
        print(f"Created 7z archive: {compressed_archive}")
    else:
        print("No archive was created.")