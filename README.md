# FastBlog
Demo blog API built with FastAPI


## Implementation Notes
- The API works with a fake database, which is just a Python class with no persistency. This `FakeDb`
emulates very bare-bones database:
    - Rows inserted using a model class
    - Basic functions such as `add`, `get`, `get_all`,  `delete`, and `update`


## Environment
Environment is managed with **pipenv**. Hence, to install all the required packages specified in the
`Pipfile`, run
```bash
pipenv install
```


## Testing
Tests written using **pytest**. Just run `pytest` from the project directory to execute all the tests.
