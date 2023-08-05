python3 -m venv venv && \
    . venv/bin/activate && \
    pip install pip setuptools wheel twine -U && \
    pip install keyring ipython -U && \
    pip install -e .
