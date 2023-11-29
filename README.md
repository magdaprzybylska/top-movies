# Movie Ranking Web App
This is a Python web application built using Flask that allows you to maintain a list of movies and rank them based on user ratings. Users can search for movies, add them to their list, and edit or delete movies as needed. The app also retrieves movie data from The Movie Database (TMDb) to display movie details.

## Prerequisites
Before you get started, make sure you have the following:

- Python installed on your system.
- A TMDb API key, which you can obtain by signing up at TMDb.
- A PostgreSQL database (or other compatible database) and the corresponding database URI.

## Installation
1. Clone or download the project from the GitHub repository.
2. Navigate to the project directory in your terminal.
3. Create a virtual environment (optional but recommended).
4. Install the required dependencies.

`pip install -r requirements.txt`

5. Create a .env file in the project root directory with the following content:

`SECRET_KEY=your_secret_key`
`SQLALCHEMY_DATABASE_URI=your_database_uri`
`ACCESS_TOKEN_AUTH=your_tmdb_api_key`

Replace your_secret_key, your_database_uri, and your_tmdb_api_key with your own values.


## Using pre-commit for Code Quality Checks

This project uses [pre-commit](https://pre-commit.com/), a framework for managing and maintaining multi-language pre-commit hooks. Pre-commit helps ensure that your codebase is consistently formatted and free of common issues before each commit.

### Installation

To get started with pre-commit, follow these steps:

1. **Install pre-commit:**

   `pip install pre-commit`

2. **Set up pre-commit in your repository:**

    `pre-commit install`

3. **Install flake8:**

    `pip install flake8`

4. **Install black:**

    `pip install black`

This command installs pre-commit hooks defined in the .pre-commit-config.yaml file into your Git hooks al well as flake8 linter and black formatting tool. Now, these hooks will run automatically before each commit.


### Pre-commit Hooks

[pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)


This repository provides a variety of pre-commit hooks for common code quality checks. In your project, the following hooks are configured:

- `check-yaml`: Checks that YAML files are valid.
- `end-of-file-fixer`:
Ensures files end with a newline.
- `trailing-whitespace` : Removes trailing whitespaces from the end of lines.
- `requirements-txt-fixer` : Sorts and updates the `requirements.txt` file.

## Features

1. Home Page: View a list of movies ranked by user ratings.
2. Add Movie: Search for a movie using the TMDb API and add it to your list.
3. Edit Movie: Edit the rating and review of a movie.
4. Delete Movie: Delete a movie from your list.

## Usage
1. To start server, run your local server the program and click in link provided in console.
2. To add a movie, click "Add Movie," enter the movie title, and click "Search." Select a movie from the search results, and it will be added to your list.
3. To edit a movie, click "Edit" next to a movie. You can update the rating and add a review.
4. To delete a movie, click "Delete" next to a movie.
5. The movie list is automatically ranked based on user ratings.

## Credits
This project uses the following libraries and technologies:

- Flask: A Python web framework.
- Flask-SQLAlchemy: For working with a relational database.
- Flask-WTF: For working with web forms.
- Flask-Bootstrap5: For Bootstrap integration.
- TMDb API: For retrieving movie data.
- PostgreSQL: As the database system.
- The Movie Database (TMDb): The source for movie details and images.

## License
This project is open-source and available under the MIT License.

Enjoy ranking your favorite movies!
