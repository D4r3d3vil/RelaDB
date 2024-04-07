from setuptools import setup, find_packages

setup(
    name='RelaDB',
    version='2.0.1',
    author='Mulham Alamry',
    author_email='mulhamreacts@gmail.com',
    description='A fast and lightweight relational db',
    long_description="""# RelaDB

🔥 RelaDB is a lightweight set of classes for a relational database system designed for simplicity and speed. It integrates with SQLite and provides an easy-to-use API for managing database schemas, tables, and records in Python.

## Classes and Methods

#### `Field`

Represents a field (column) in a database table.

##### `__init__(self, name: str, data_type: Type) -> None`

- `name`: The name of the field.
- `data_type`: The Python type of the field (e.g., `int`, `str`, `float`, `dict`, `list`).

#### `Row`

Represents a row in a database table, allowing for dynamic field assignment.

##### `__init__(self, **kwargs: Union[Dict[str, Any], Any]) -> None`

- `**kwargs`: Key-value pairs representing the field names and their values for the row.

##### `get(self, field: str = '') -> Union[Dict[str, Any], Any]`

- `field`: Optional. The name of a specific field to retrieve. If not specified, returns a dictionary of all fields and values.

##### `add_field(self, field_name: str, field_value: Any) -> None`

- `field_name`: The name of the field to add or update.
- `field_value`: The value of the field.

#### `Table`

Represents a table in the database, including its schema (fields) and rows (records).

##### `__init__(self, name: str) -> None`

- `name`: The name of the table.

##### `add_fields(self, fields_dict: Dict[str, Type]) -> None`

- `fields_dict`: A dictionary mapping field names to their data types.

##### `add_field(self, field_name: str, data_type: Type) -> None`

- `field_name`: The name of the field to add.
- `data_type`: The data type of the field.

##### `delete_fields(self, *field_names: str) -> None`

- `*field_names`: One or more field names to delete from the table schema.

##### `add_row(self, **kwargs: Dict[str, Any]) -> None`

- `**kwargs`: Key-value pairs representing the field names and their values for the new row.

##### `delete_row(self, condition: Callable[[Row], bool]) -> None`

- `condition`: A function that returns `True` for rows that should be deleted.

##### `find(self, condition: Callable[[Row], bool] = lambda func: True, amount: int = 0) -> List[Row]`

- `condition`: A function that returns `True` for rows to include in the result.
- `amount`: Optional. The maximum number of rows to return.

#### `Database`

Manages the connection to the SQLite database and provides methods for database operations.

##### `__init__(self, db_file: str = '') -> None`

- `db_file`: Optional. The file path of the SQLite database. Defaults to in-memory operation if not specified.

##### `create(self, table_name: str, fields: Dict[str, Type]) -> Table`

- `table_name`: The name of the table to create.
- `fields`: A dictionary mapping field names to their data types.

##### `delete(self, table_name: str) -> None`

- `table_name`: The name of the table to delete.

##### `get(self, table_name: str) -> Table`

- `table_name`: The name of the table to retrieve.

##### `save(self) -> None`

Saves the database schema and data to the SQLite file specified in the `db_file` attribute.

##### `load(self) -> None`

Loads the database schema and data from the SQLite file specified in the `db_file` attribute.

## Usage Example

```python
from relaDB import Database

# Initialize database
db = Database()

# Create a table
users = db.create("users", {"name": str, "age": int})

# Add a row to the table
users.add_row(name="Alice", age=30)

# Find a row in the table
user = users.find(lambda row: row.get("name") == "Alice")[0]
print(user.get())
```

Happy programming!""",
    long_description_content_type='text/markdown',
    url='https://github.com/D4r3d3vil/RelaDB',
    packages=find_packages(),
    python_requires='>=3.0',
)
