import requests
import json
from collections import Counter
import time

GET_NEW = False
example_fname = "example_results.json"

QUESTIONS_BASE = "https://api.stackexchange.com/2.2/questions?site=stackoverflow"


def get_new(pages=1):
    items = []
    for page in range(1, pages + 1):
        print("Fetching page:", page)
        query_string = QUESTIONS_BASE + f"&tagged=python&pagesize=100&page={page}"
        results = requests.get(query_string)
        if results.status_code != 200:
            print("bad response:", results)
            print(results.content)
            exit()
        results = results.json()
        items.extend(results["items"])
        if not results["has_more"]:
            print("no more pages")
            break
        if results["quota_remaining"] <= 0:
            print("no quota remaining:", results["quota_remaining"])
            break
        if "backoff" in results.keys():
            backoff_time = results["backoff"]
            print("backoff time:", backoff_time)
        else:
            backoff_time = 1 / 25
        print("Quota remaining:", results["quota_remaining"])
        print("Has more:", results["has_more"])
        print()
        time.sleep(backoff_time)

    with open(example_fname, "w") as f:
        json_out = {"items": items}
        json.dump(json_out, f)


TAG_CATEGORIES = {
    "charting": ["matplotlib", "plot", "seaborn", "plotly", "data-visualization"],
    "cloud_services": [
        "amazon-web-services",
        "google-cloud-platform",
        "aws-lambda",
        "google-colaboratory",
        "azure",
    ],
    "data_formats": ["json", "csv", "excel", "xml"],
    "data_science": [
        "data-science",
        "pandas",
        "numpy",
        "dataframe",
        "scipy",
        "pandas-groupby",
        "time-series",
        "matrix",
        "numpy-ndarray",
        "statistics",
        "linear-regression",
        "data-analysis",
    ],
    "database": [
        "mysql",
        "apache-spark",
        "sql",
        "sqlalchemy",
        "postgresql",
        "pyspark",
        "psycopg2",
        "mongodb",
        "sqlite",
        "flask-sqlalchemy",
        "sql-server",
        "pymongo",
    ],
    "game_programming": ["pygame"],
    "general_programming": [
        "algorithm",
        "api",
        "docker",
        "email",
        "git",
        "recursion",
        "regex",
        "sockets",
    ],
    "gui": ["tkinter", "pyqt5", "pyqt", "kivy", "user-interface"],
    "ide": ["pycharm", "visual-studio-code"],
    "image_processing": [
        "opencv",
        "image-processing",
        "image",
        "python-imaging-library",
    ],
    "language_features": [
        "arrays",
        "class",
        "date",
        "datetime",
        "dictionary",
        "f-string",
        "file",
        "for-loop",
        "function",
        "if-statement",
        "import",
        "list",
        "logging",
        "loops",
        "math",
        "module",
        "multiprocessing",
        "multithreading",
        "optimization",
        "parsing",
        "performance",
        "string",
        "lambda",
    ],
    "language_specific_tools": [
        "pip",
        "jupyter-notebook",
        "jupyter",
        "anaconda",
        "conda",
        "virtualenv",
        "pyinstaller",
    ],
    "language_version": ["python-3.x", "python-2.7"],
    "machine_learning": [
        "tensorflow",
        "machine-learning",
        "keras",
        "scikit-learn",
        "deep-learning",
        "pytorch",
        "neural-network",
        "nlp",
        "tensorflow2.0",
        "conv-neural-network",
    ],
    "os": ["linux", "windows", "macos", "ubuntu"],
    "other_language": ["javascript", "html", "c++", "r", "c", "bash"],
    "testing": [
        "selenium",
        "selenium-webdriver",
        "pytest",
        "selenium-chromedriver",
        "unit-testing",
    ],
    "web_framework": [
        "django",
        "django-forms",
        "django-models",
        "django-rest-framework",
        "django-templates",
        "django-views",
        "flask",
    ],
    "web_programming": ["python-requests"],
    "web_scraping": ["web-scraping", "beautifulsoup", "scrapy"],
}


def classify_tag(tag_name):
    for category, tags in TAG_CATEGORIES.items():
        if tag_name in tags:
            return "\t" + category
    return tag_name


if GET_NEW:
    get_new(50)

with open(example_fname, "r") as f:
    results = json.load(f)

other_tags = []
for s in results["items"]:
    other_tags.extend(s["tags"])

cnt = Counter(other_tags)
categories = Counter([classify_tag(tag) for tag in other_tags])

# for tag, count in sorted(cnt.items(), key=lambda x: x[1]):
# print(f"{tag}: {count}")
for tag, count in sorted(categories.items(), key=lambda x: x[1]):
    print(f"{tag}: {count}")
