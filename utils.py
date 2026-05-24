import os
import shutil

def ensure_directories(directories: list[str]) -> None:
    """
    Ensures that the specified directories exist.
    Creates them if they do not exist.
    """
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

def validate_pdf(filename: str, file_size: int = 1) -> bool:
    """
    Validates if a file is a PDF based on its extension and check that it's not empty.
    """
    if not filename.lower().endswith('.pdf'):
        return False
    if file_size <= 0:
        return False
    return True

def save_uploaded_file(uploaded_file, upload_dir: str) -> str:
    """
    Saves a file uploaded via Streamlit to a local uploads directory.
    Returns the absolute path of the saved file.
    """
    ensure_directories([upload_dir])
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        # Write bytes from Streamlit UploadedFile object
        f.write(uploaded_file.getbuffer())
    return os.path.abspath(file_path)

def clear_directory(directory: str) -> None:
    """
    Removes all files and subdirectories from the given directory.
    """
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
