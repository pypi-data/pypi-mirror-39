Facextractor
============

Facebook Data Extractor, simple tool for read and analyze facebook dump (JSON format).


## Instalation

PyPI
```bash
pip install facextractor
```

or from source:

```bash
git clone https://github.com/geekmoss/facextractor.git
cd facextractor
pip install .
```

and for bash complete:

```bash
bash bash-complete.sh
```

## Using

### CLI

```bash
# Friends:
facextractor friends ./facebook-dump

# Chats:
# For summary of all chats
facextractor threads ./facebook-dump
# For summary of chat with John Doe
facextractor friends ./facebook-dump -f "John Doe"
# For summary of all chats where is John Doe is participant
facextractor friends ./facebook-dump -p -f "John Doe" 
```

### Python Packages

```python
from Facextractor import Friends, Threads

t = Threads("./facebook-dump")
t.describe()  # str: summary of all chats
t.analysis.photos  # int: count photos of all chats

t.threads[0].describe()  # str: summary of first thread in list

t.find_thread_by_name("John Doe")  # Thread: return thread for exact match
t.find_threads_by_participant("John Doe")  # List[Thread]: returns list of threads where is participant
```