# SPMB Bali Scraping

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A Python web scraping tool to extract student selection results from the SPMB Bali website (`bali.spmb.id`). It uses Selenium with Microsoft Edge to navigate the site, collect school-level summary data, and scrape individual student details (name, origin school, NISN, and test scores), then exports everything as CSV files.

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (package manager)
- Microsoft Edge browser

## Dependencies

| Package             | Version   |
| ------------------- | --------- |
| `selenium`          | >= 4.45.0 |
| `webdriver-manager` | >= 4.1.2  |

> `webdriver-manager` will automatically download and manage the correct Microsoft Edge WebDriver — no manual installation needed.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/tudemaha/spmbbali-scraping.git
   cd spmbbali-scraping
   ```

2. **Install dependencies using `uv`**

   ```bash
   uv sync
   ```

## Configuration

Before running the script, open `main.py` and update the following variables at the top of the file:

```python
# URL of the selection result page from smabali.spmb.id or smkbali.spmb.id
url = "https://smabali.spmb.id/010101/hasil"

# List of school names to scrape student details from
selected_school = ["SMA NEGERI 1 DENPASAR"]

# Selection type — used as the output folder name (e.g., "Domisili", "Prestasi")
selection_type = "Domisili"
```

### Variable Details

| Variable          | Description                                        | Example                                              |
| ----------------- | -------------------------------------------------- | ---------------------------------------------------- |
| `url`             | The URL of the SPMB selection result page          | `"https://smabali.spmb.id/010101/hasil"`             |
| `selected_school` | List of school names to scrape student details for | `["SMA NEGERI 1 DENPASAR", "SMA NEGERI 2 DENPASAR"]` |
| `selection_type`  | Marker used as the output folder name              | `"Domisili"`, `"Prestasi"`                           |

> **Note:** School names must match exactly as shown on the SPMB Bali website (case-sensitive).

## Usage

Run the script with `uv`:

```bash
uv run main.py
```

## Output

The script generates CSV files inside a folder named after `selection_type`:

```
<selection_type>/
├── Seleksi <selection_type>.csv   # Summary of all schools (name, NPSN, highest & lowest score)
├── SMA NEGERI 1 DENPASAR.csv      # Student details for each selected school
└── ...
```

### School Summary CSV (`Seleksi <selection_type>.csv`)

| Column        | Description                       |
| ------------- | --------------------------------- |
| `school_name` | Name of the school                |
| `npsn`        | National school identifier (NPSN) |
| `highest`     | Highest student score accepted    |
| `lowest`      | Lowest student score accepted     |

### Student Details CSV (`<School Name>.csv`)

| Column       | Description                          |
| ------------ | ------------------------------------ |
| `name`       | Student's full name                  |
| `origin_smp` | Student's origin junior high school  |
| `nisn`       | Student's NISN (national student ID) |
| `math`       | TKA Mathematics score                |
| `indonesian` | TKA Bahasa Indonesia score           |

## Example

To scrape domisili selection results for two schools:

```python
url = "https://smabali.spmb.id/010101/hasil"
selected_school = ["SMA NEGERI 1 DENPASAR", "SMA NEGERI 3 DENPASAR"]
selection_type = "Domisili"
```

After running:

```
Domisili/
├── Seleksi Domisili.csv
├── SMA NEGERI 1 DENPASAR.csv
└── SMA NEGERI 3 DENPASAR.csv
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Feel free to contribute for more advanced scraping. Just need to fork, add features, and create a pull request.

## Issues

Go to [Issues](https://github.com/tudemaha/spmbbali-scraping/issues) page then create an issue.
