import json
import sqlite3
from typing import Dict, List, Callable, Union, Any, Type, Optional

def serialize(value: Any) -> Any:
        """
        Serializes a value into a JSON string if it's a dictionary or list, otherwise returns the value unchanged.

        Args:
            value (Any): The value to serialize.

        Returns:
            Any: The serialized value or the original value.
        """
        if isinstance(value, (dict, list)):
            return json.dumps(value)
        return value

def deserialize(value: Any) -> Any:
    """
    Deserializes a JSON string back into a Python dictionary or list if applicable, otherwise returns the value unchanged.

    Args:
        value (Any): The value to deserialize.

    Returns:
        Any: The deserialized Python object or the original value.
    """
    try: return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value

class Field:
    def __init__(self, name: str, data_type: Type) -> None:
        """
        Initializes a new Field instance.

        Args:
            name (str): The name of the field.
            data_type (Type): The Python type of the field.
        """
        self.name: str = name
        self.data_type: Type = data_type

class Row:
    def __init__(self, **kwargs: Union[Dict[str, Any], Any]) -> None:
        """
        Initializes a new Row instance with dynamic fields.

        Args:
            **kwargs: Arbitrary keyword arguments representing field names and values.
        """
        self.fields: Dict[str, Any] = {}
        for field_name, field_value in kwargs.items():
            self.fields[field_name] = serialize(field_value)
    
    def get(self, field: str = '') -> Union[Dict[str, Any], Any]:
        """
        Retrieves the value of a specified field, or all fields if no specific field is requested.

        Args:
            field (str, optional): The name of the field to retrieve. If empty, all fields are returned. Defaults to ''.

        Returns:
            Union[Dict[str, Any], Any]: The value of the specified field, or a dictionary of all fields and their values.
        """
        if field == '':
            return {i: deserialize(self.fields[i]) for i in self.fields}
        return deserialize(self.fields[field])

    def add_field(self, field_name: str, field_value: Any) -> None:
        """
        Adds or updates a field to the row.

        Args:
            field_name (str): The name of the field to add or update.
            field_value (Any): The value of the field.
        """
        self.fields[field_name] = serialize(field_value)

class Table:
    def __init__(self, name: str) -> None:
        """
        Initializes a new Table instance.

        Args:
            name (str): The name of the table.
        """
        self.name: str = name
        self._fields: List[Field] = []
        self._rows: List[Row] = []

    def add_fields(self, fields_dict: Dict[str, Type]) -> None:
        """
        Adds multiple fields to the table schema.

        Args:
            fields_dict (Dict[str, Type]): A dictionary mapping field names to their data types.
        """
        for field_name, data_type in fields_dict.items():
            self.add_field(field_name, data_type)

    def add_field(self, field_name: str, data_type: Type) -> None:
        """
        Adds a single field to the table schema.

        Args:
            field_name (str): The name of the field to add.
            data_type (Type): The data type of the field.
        """
        self._fields.append(Field(field_name, data_type))
    
    def delete_fields(self, *field_names: str) -> None:
        """
        Deletes fields from the table schema.

        Args:
            *field_names (str): Variable number of field names to delete.
        """
        self._fields = [field for field in self._fields if field.name not in field_names]
        for row in self._rows:
            for field_name in field_names:
                if field_name in row.fields:
                    del row.fields[field_name]

    def add_row(self, **kwargs: Dict[str, Any]) -> None:
        """
        Adds a new row to the table with the specified field values.

        Args:
            **kwargs: Arbitrary keyword arguments representing field names and their values.

        Raises:
            ValueError: If the number of fields in the row does not match the table schema, 
                        if a field does not exist in the table schema, 
                        or if a field value does not match its expected data type.
        """
        if len(kwargs) != len(self._fields):
            raise ValueError("Number of fields in row does not match the number of fields in table schema.")

        for field_name, field_value in kwargs.items():
            expected_data_type = next((field.data_type for field in self._fields if field.name == field_name), None)
            if expected_data_type is None:
                raise ValueError(f"Field '{field_name}' does not exist in table schema.")
            elif not isinstance(field_value, expected_data_type):
                raise ValueError(f"Field '{field_name}' type does not match the expected type ({expected_data_type}).")

        self._rows.append(Row(**kwargs))
    
    def delete_row(self, condition: Callable[[Row], bool]) -> None:
        """
        Deletes rows from the table that match the given condition.

        Args:
            condition (Callable[[Row], bool]): A function that evaluates to True for rows to be deleted.
        """
        self._rows = [row for row in self._rows if not condition(row)]

    def find(self, condition: Callable[[Row], bool] = lambda func: True, amount: int = 0) -> List[Row]:
        """
        Finds rows in the table that match a given condition.

        Args:
            condition (Callable[[Row], bool]): A function that evaluates to True for rows to be included in the result.
            amount (int, optional): The maximum number of rows to return. If 0, all matching rows are returned. Defaults to 0.

        Returns:
            List[Row]: A list of rows that match the condition, limited by the 'amount' parameter if it is not 0.
        """
        matching_rows = [row for row in self._rows if condition(row)]
        if amount > 0:
            return matching_rows[:amount]
        return matching_rows

class Database:
    def __init__(self, db_file: str = '') -> None:
        """
        Initializes a new Database instance.

        Args:
            db_file (str, optional): The file path of the SQLite database. If empty, the database operates in memory. Defaults to ''.
        """
        self._tables: Dict[str, Table] = {}
        self.db_file: str = db_file

    def create(self, table_name: str, fields: Dict[str, Type]) -> Table:
        """
        Creates a new table in the database with the given schema.

        Args:
            table_name (str): The name of the table to create.
            fields (Dict[str, Type]): A dictionary mapping field names to their data types.

        Returns:
            Table: The newly created table.

        Raises:
            ValueError: If the table already exists.
        """
        if table_name in self._tables:
            raise ValueError(f"Table '{table_name}' already exists.")
        table = Table(table_name)
        table.add_fields(fields)
        self._tables[table_name] = table
        return table

    def delete(self, table_name: str) -> None:
        """
        Deletes a table from the database.

        Args:
            table_name (str): The name of the table to delete.

        Raises:
            KeyError: If the specified table does not exist.
        """
        if table_name not in self._tables:
            raise KeyError(f"Table '{table_name}' does not exist.")
        del self._tables[table_name]

    def get(self, table_name: str) -> Table:
        """
        Retrieves a table from the database.

        Args:
            table_name (str): The name of the table to retrieve.

        Returns:
            Table: The requested table.

        Raises:
            KeyError: If the specified table does not exist.
        """
        if table_name not in self._tables:
            raise KeyError(f"Table '{table_name}' does not exist.")
        return self._tables[table_name]

    def save(self) -> None:
        """
        Saves the database schema and data to a file specified by db_file attribute.

        Raises:
            ValueError: If db_file attribute is not set.
        """
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        for table_name, table in self._tables.items():
            field_definitions = []
            for field in table._fields:
                if field.data_type == list or field.data_type == dict:
                    field_definitions.append(f"{field.name} JSON")
                else:
                    field_type = "REAL" if field.data_type is float else "INTEGER" if field.data_type is int else "TEXT"
                    field_definitions.append(f"{field.name} {field_type}")
            field_definitions = ", ".join(field_definitions)

            cursor.execute(f"DROP TABLE IF EXISTS {table_name}") 
            cursor.execute(f"CREATE TABLE {table_name} ({field_definitions})")

            for row in table._rows:
                columns = ", ".join(row.fields.keys())
                placeholders = ", ".join(["?" for _ in row.fields])
                values = [serialize(value) for value in row.fields.values()]
                cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)

        connection.commit()
        connection.close()

    def load(self) -> None:
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name in tables:
            table_name = table_name[0]
            if table_name == "sqlite_sequence":
                continue

            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            fields_dict = {}
            for col in columns:
                col_name, col_type = col[1], col[2]
                if col_type == "JSON":
                    field_type = Union[list, dict]
                else:
                    field_type = float if col_type == "REAL" else int if col_type == "INTEGER" else str
                fields_dict[col_name] = field_type

            table = self.create(table_name, fields_dict)
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            for row in rows:
                kwargs = {columns[i][1]: deserialize(row[i]) for i in range(len(columns))}
                table.add_row(**kwargs)
        connection.close()