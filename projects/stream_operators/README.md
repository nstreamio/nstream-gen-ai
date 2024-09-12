# **Stream Operators**

This project demonstrates generating real-time stream operators from natural language queries using OpenAI and SwimOS.

## **Project Structure**

```
.
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   └── stream_operators
│       ├── __init__.py
│       ├── main.py
│       ├── operators.py
│       ├── snippet.py
│       ├── test.py
└── tests
    └── __init__.py
```

- `pyproject.toml`: Project configuration and dependencies managed by Poetry.
- `poetry.lock`: Locked versions of the dependencies for reproducibility.
- `src/stream_operators/`: Source code for the project.
- `tests/`: Test suite for the project.

## **Requirements**

- Python 3.8+
- [Poetry](https://python-poetry.org/) for dependency management and packaging.

## **Setup Instructions**

1. **Install Poetry** (if you don't have it installed yet):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   Alternatively, follow the official installation guide [here](https://python-poetry.org/docs/#installation).

2. **Install Project Dependencies**:

   Once Poetry is installed, run the following command from the root of the project (where `pyproject.toml` is located) to install the project dependencies:

   ```bash
   poetry install
   ```

   This will install all required dependencies listed in `pyproject.toml` and make sure the environment adheres to the versions locked in `poetry.lock`.

3. **Activate the Virtual Environment**:

   Poetry automatically creates a virtual environment. To activate it, run:

   ```bash
   poetry shell
   ```

   This ensures that your environment is isolated and includes all dependencies.

## **Running the Application**

The main application is located in `src/stream_operators/main.py`. To run it, execute:

```bash
poetry run python src/stream_operators/main.py
```

Alternatively, if you've activated the virtual environment via `poetry shell`, you can simply run:

```bash
python src/stream_operators/main.py
```

## **Running Tests**

To run the tests in the `tests/` directory, use:

```bash
poetry run pytest
```

This will automatically discover and execute the test suite.

## **Environment Variables**

To run the project, you need to set up your environment variables. This project uses a `.env` file to store sensitive information like API keys. The `.env` file is excluded from version control for security reasons.

1. **Create a `.env` File**:
   A template is provided as `dot-env-file`. To set up your environment, copy this file to the root of the project and rename it to `.env`:

   ```bash
   cp src/stream_operators/dot-env-file .env
   ```

2. **Update the `.env` File**:
   Open the `.env` file and replace `<your_api_key>` with your actual OpenAI API key:

   ```bash
   OPENAI_API_KEY=<your_actual_api_key>
   ```

3. **Ensure the `.env` File is Ignored by Git**:
   The `.env` file is already excluded by the `.gitignore` file to prevent sensitive information from being committed to the repository.

## **Project Overview**

This project allows users to generate real-time stream operators from natural language queries using OpenAI and SwimOS. The `main.py` script processes commands, interacts with the LLM to generate operators, and executes the corresponding stream operations.
