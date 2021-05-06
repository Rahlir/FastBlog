# FastBlog
Demo blog API built with FastAPI


## Implementation Notes
- The API works with a fake database, which is just a Python class with no persistency. This `FakeDb`
emulates very bare-bones database:
    - Rows inserted using a model class
    - Basic functions such as `add`, `get`, `get_all`,  `delete`, and `update`
- The program could have been much shorter if I didn't create an entire fake database module and
instead used only pydantic models and saved their json representation into a simple map. However,
I felt that in that case the project would be too small and not really representative of real world
application
- Normally, I wouldn't be manipulating the blog post data directly in the `main.py` function, but
instead there would be a separate _crud_ module. However, since the `FakeDb` in `database.py` behaves
pretty much like a _crud_ module, I decided against creating this unnecessary module



## Environment
Environment is managed with **pipenv**. Hence, to install all the required packages specified in the
`Pipfile`, run
```bash
pipenv install
```


## Testing
Tests written using **pytest**. Just run `pytest` from the project directory to execute all the tests.
