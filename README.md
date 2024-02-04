# Aria
![pylint](https://github.com/mazzobeg/aria/blob/develop/badges/coverage.svg)
![pytest](https://github.com/mazzobeg/aria/actions/workflows/python-test.yml/badge.svg?branch=develop)

## Description

Aria is designed to provide a summary interface for your technical (or other types of) monitoring. It is built to be extensive for article retrieving mechanisms (see this [Section](#add-a-new-scraper-for-article-retrieving) part for integrating your scraper) and is AI-powered for article summarizing.

Aria is a Python application that uses Celery for task management and Flower for task monitoring. It's designed to handle asynchronous tasks efficiently and provide real-time monitoring of task progress.

## Installation

To install the necessary dependencies for Aria, you can use pip. First, clone the repository:

```zsh
git clone https://github.com/username/aria.git
cd aria
```

Then, install the dependencies:

```zsh
pip install -r requirements.txt
```

## Usage
### Running the project
To run Aria, use the following command:

```zsh
sh run.sh
```

This script will start the Celery worker and Flower server, and redirect their output to log files in the logs directory.

```zsh
flask run -A aria
```

### Add a new scraper for article retrieving
**INCOMING**

## Running Tests
To run the tests for Aria, use the following command:

```zsh
pytest
```

## Contributing
Contributions to Aria are welcome!

## License
Aria is licensed under the [insert license here]. See the LICENSE.md file for details.