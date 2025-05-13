# Ragazzo Vocabulary

A tool to export Anki flashcards to GitHub Pages for use in other applications.

## Prerequisites

1. [Anki](https://apps.ankiweb.net/) installed
2. [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed in Anki
3. Python 3.6 or higher

## Installation

Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/ragazzo-vocabulary.git
cd ragazzo-vocabulary
```

Install the tool:
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Setting up the Command Alias

To use the `ragazzo-vocabulary` command from anywhere in your terminal, add this alias to your `~/.zshrc` file. Replace `YOUR_REPO_PATH` with the absolute path to your repository:

```bash
# Alias for ragazzo-vocabulary
alias ragazzo-vocabulary="YOUR_REPO_PATH/venv/bin/ragazzo-vocabulary"
```

To find your repository path, run this command from your repository directory:
```bash
pwd
```

Then reload your shell configuration:
```bash
source ~/.zshrc
```

## Usage

1. Make sure Anki is running with the AnkiConnect add-on installed
2. Run the following command to update your vocabulary:
```bash
ragazzo-vocabulary
```

This will:
1. Fetch your Italian flashcards from Anki
2. Format them and save them to a JSON file in the `docs` directory
3. Create an HTML redirect page
4. Commit and push the changes to GitHub

## GitHub Pages Setup

1. Go to your repository settings on GitHub
2. Navigate to "Pages" under "Code and automation"
3. Under "Source", select "Deploy from a branch"
4. Select "main" branch and "/docs" folder, then save

Your vocabulary will be available at: `https://moritzmoeller.github.io/ragazzo-vocabulary/vocabulary.json`