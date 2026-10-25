# Address to MGRS CLI Converter

A command-line utility written in Python to convert human-readable street addresses to 1-meter precision Military Grid Reference System (MGRS) coordinates and vice versa. 

This tool uses direct HTTP requests to the high-accuracy Geocodio API v2 to prevent the linear address interpolation and block-jumping issues found in open-source geocoders.

## License

This project is licensed under the Apache License 2.0. See the file header in the script for the full license text.

---

## Installation

### 1. Clone or Download the Script
Save the Python file as `addr2mgrs.py` in your working directory.

### 2. Set Up a Virtual Environment (Recommended)
Navigate to your project folder and create a clean environment using your package manager:

```bash
python3 -m venv myEnv
source myEnv/bin/activate
```

### 3. Install Dependencies
Install the required packages using `pip` or `uv`:

```bash
pip install requests mgrs python-dotenv
```

---

## Configuration

The script reads its runtime configurations securely from a local environment file. 

1. Create a file named **`.env`** in the exact same directory as the script.
2. Generate a free API key at [geocod.io](https://www.geocod.io/) (includes 2,500 free lookups daily).
3. Add your variables to the file:

```text
GEOCODIO_API_KEY=your_actual_api_key_here
GEOCODIO_BASE_URL=https://api.geocod.io/v2
```

*Note: Make sure your `.env` file is added to your `.gitignore` to prevent committing your secret API keys to public version control.*

---

## Example Usage

The tool uses standard CLI arguments via `argparse`. You must specify either `--to-mgrs` or `--to-address`.

### 1. Convert Address to MGRS (Forward Lookup)
Provide a human-readable street address string wrapped in quotes to generate a 1-meter precision coordinate string:

```bash
python addr2mgrs.py --to-mgrs "1600 Amphitheatre Parkway, Mountain View, CA"
```

**Output:**
```text
MGRS (1-Meter): 10SEG0238981231
Full Address:   1600 Amphitheatre Pkwy, Mountain View, CA 94043
```

### 2. Convert MGRS to Address (Reverse Lookup)
Provide an MGRS string to resolve the exact coordinate block back into a postal street address:

```bash
python addr2mgrs.py --to-address "10SEG0238981231"
```

**Output:**
```text
Full Address:   1600 Amphitheatre Pkwy, Mountain View, CA 94043
```

---

## Troubleshooting

### Error: `list indices must be integers or slices, not str`
Ensure you are using the final updated version of the code. This occurs if the script tries to access the raw Geocodio response array directly without specifying the index payload target (`results[0]`).

### Error: `GEOCODIO_API_KEY is not set`
Verify that your `.env` file is spelled correctly with a leading dot and resides in the exact directory from which you are executing the python command. 
