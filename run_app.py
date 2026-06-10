import os
import sys

# Set the protobuf environment variable before importing any other modules
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Detect if we are already running inside the Streamlit server process
is_inside_streamlit = False
if "streamlit" in sys.modules or any("streamlit" in arg for arg in sys.argv):
    is_inside_streamlit = True

if is_inside_streamlit:
    # Import the main app module to execute it
    import app
else:
    # We are running directly via 'python run_app.py'. Boot the Streamlit server.
    try:
        from streamlit.web import cli as stcli
    except ImportError:
        from streamlit import cli as stcli
        
    sys.argv = ["streamlit", "run", "run_app.py"]
    sys.exit(stcli.main())
