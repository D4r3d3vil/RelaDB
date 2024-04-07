# RelaDB

🔥 RelaDB is a lightweight set of classes for a relational database system designed for simplicity and speed. It integrates with SQLite and provides an easy-to-use API for managing database schemas, tables, and records in Python.

## Installation

Installation form pip is recommended: 
```bash
pip install relaDB
```

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

# Usage Example

## Getting Started

Let's start by creating a simple database and adding some tables to it.

```python
from relaDB import Database

# Initialize the database
db = Database()

# Create a table for storing user data
users_table = db.create("users", {"name": str, "age": int})

# Add some users to the table
users_table.add_row(name="Alice", age=30)
users_table.add_row(name="Bob", age=25)
users_table.add_row(name="Jimmy", age=16)
```

## Retrieving Data

Now, let's retrieve data from the `users` table.

```python
# Find a user by name
alice = users_table.find(lambda row: row.get("name") == "Alice")[0]
print(alice.get())  # Output: {'name': 'Alice', 'age': 30}

# Find users older than 18
adults = users_table.find(lambda row: row.get("age") > 18)
for user in adults:
    print(user.get())  # Output: {'name': 'Alice', 'age': 30}, {'name': 'Bob', 'age': 25}
```

## Updating Data

We can also update or add in existing records in the table.

```python
# Update Alice's age
alice.add_field("age", 31)
print(alice.get())  # Output: {'name': 'Alice', 'age': 31}
```

## Deleting Data

Deleting records from the table is straightforward as well.

```python
# Delete users younger than 18
users_table.delete_row(lambda row: row.get("age") < 18)
```

## Advanced Usage

Rela DB supports more advanced operations such as deleting tables, saving and loading databases from files, and more. For now, the only extension supported is sqlite.

```python
# Save the database to a file
db.db_file = "users.sqlite3"
db.save()
```

Once you have saved it, you can load the database:

```python
# Load the database from a file
db = Database('users.sqlite3') # only do this if it's in another file or you haven't called Database()
db.load()
for user in db.get('users').find():
    print(user.get()) # This is left empty to get the entire row if you would like to get a specific value of the row such as name or age, pass it in as a parameter.
```


Happy programming!
