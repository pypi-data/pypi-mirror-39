virtualenv venv && \
    . venv/bin/activate && \
    pip install pip setuptools wheel twine -U && \
    pip install pip keyring ipython -U && \
    pip install ipython && \
    pip install -e .
