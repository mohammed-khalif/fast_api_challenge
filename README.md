# fast_api_challenge

## API Endpoints

- `GET /get_all_endpoint/`: Get all data.
- `GET /get_one_endpoint/{id}`: Get a single data entry by ID.
- `POST /post_endpoint/`: Create a new data entry.
- `PUT /put_endpoint/{id}`: Update a data entry by ID (full update).
- `PATCH /patch_endpoint/{id}`: Update a data entry by ID (partial update).
- `DELETE /delete_endpoint/{id}`: Delete a data entry by ID.

## Data Model

The API works with a data model called `MyData`. It has the following fields:

- `id` (integer): The unique identifier for the data entry.
- `name` (string): The name of the data entry.
- `description` (string): The description of the data entry.

## Database

The API uses a SQLite database named `my_database.db`. The database file will be created automatically when you run the application.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the functionality, feel free to open a pull request.

## License

This project is licensed under the MIT License.
