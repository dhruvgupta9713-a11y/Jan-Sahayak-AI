import os
import sys

# Set the protobuf environment variable before importing any other modules
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

try:
    from streamlit.web import cli as stcli
except ImportError:
    # Fallback for older streamlit versions
    from streamlit import cli as stcli

if __name__ == '__main__':
    # Force the arguments to run app.py
    sys.argv = ["streamlit", "run", "app.py"]
    sys.exit(stcli.main())
