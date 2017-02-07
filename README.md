# The Met's Open Access CSV to JSON

This repository contains a Python script `met.py` which will download The Met's open access data file from [https://github.com/metmuseum/openaccess], parse the CSV, and generate a directory tree of JSON files. For a variety of reasons, I find JSON much easier to work with, and I suspect you may too!

I'm not currently mirroring the actual JSON files here.

## How to Use

1. Create a Python 3 virtualenv
2. Install `requests` by using the included `requirements.txt` or just running `pip install requests`
3. Run the script from the commandline, eg. `./met.py`
4. Success!

Feel free to ping me on Twitter @rogerhoward or open an issue if you need help. This was a quick hack, with basically no error handling or optimizations. It works though, I swear!

@rogerhoward