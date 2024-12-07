import sqlite3
import os


def remove_lines_with_substring(file_path, sub_strings):
    try:
        # Read the contents of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Filter the lines
        filtered_lines = [line for line in lines if not any(sub_string in line for sub_string in sub_strings)]

        # Write it back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(filtered_lines)

        print(f"Lines containing '{sub_strings}', have been removed from the file {file_path}.")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"There was an error: {e}")


def remove_duplicates_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Удаляем дубликаты, сохраняя порядок строк
        unique_lines = list(dict.fromkeys(lines))

        # Записываем уникальные строки обратно в файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(unique_lines)

        print(f"Duplicates have been removed from the file: {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error: {e}")




def generate_update_script(main_db, mod_db, output_file):
    # Connect to primary and secondary databases
    main_conn = sqlite3.connect(main_db)
    mod_conn = sqlite3.connect(mod_db)

    # Getting cursors
    main_cursor = main_conn.cursor()
    mod_cursor = mod_conn.cursor()

    # Open the file for recording
    with open(output_file, 'a') as output:
        # Get the list of tables from the main database
        main_cursor.execute("SELECT COALESCE(name,'NULL') FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in main_cursor.fetchall()]

        for table in tables:
            try:
                # Getting the table columns
                main_cursor.execute(f"PRAGMA table_info({table});")
                columns = [row[1] for row in main_cursor.fetchall()]

                # Filter columns with ID in the name
                id_columns = [col for col in columns if "ID" in col.upper()]

                if not id_columns:
                    continue  # Skip tables without ID columns

                # Form a query to select rows from an additional database
                mod_cursor.execute(f"SELECT * FROM {table}")
                mod_rows = mod_cursor.fetchall()

                # Get the names of all columns from the table
                mod_cursor.execute(f"PRAGMA table_info({table});")
                mod_columns = [row[1] for row in mod_cursor.fetchall()]

                # Checking rows from the mod database into the main database
                for row in mod_rows:
                    values = tuple(row[mod_columns.index(col)] for col in columns)  # id_columns

                    # Filtering columns and values simultaneously
                    filtered_columns_values = [
                        (col, value)
                        for col, value in zip(columns, values)
                        if col  # Exclude None or empty row from columns
                    ]

                    # Separate filtered columns and values
                    filtered_columns, filtered_values = zip(*filtered_columns_values) if filtered_columns_values else (
                        [], [])

                    # Generation of conditions
                    conditions = " AND ".join(
                        f"{col} IS ?" if value is None else f"{col} = ?"
                        for col, value in filtered_columns_values
                    )

                    query = f"SELECT * FROM {table} WHERE {conditions}"
                    main_cursor.execute(query, filtered_values)
                    if not main_cursor.fetchone():  # If the row is not in the main database
                        # Form an SQL query for inserting a string
                        insert_query = f"INSERT OR REPLACE INTO {table} ({', '.join(filtered_columns)}) VALUES ("
                        insert_values = tuple(filtered_values)

                        # Write the request to a file
                        for query_row in insert_values:
                            if query_row is None:
                                query_row = 'NULL'
                                insert_query += (f"{query_row}" + ', ')
                            elif isinstance(query_row, str):
                                if '\'' in query_row:
                                    query_row = query_row.replace("\'", "''")
                                insert_query += (f"\'{query_row}\'" + ", ")
                            else:
                                insert_query += str(query_row) + ', '

                        output.write(insert_query[:-2].replace(", ,", ",") + ");\n")

            except Exception as e:
                print(f"Error during table processing  {table}: {e}")

    # Closing the connections
    main_conn.close()
    mod_conn.close()
    # Specify the file path and substring to delete
    file_path = output_file  # "differences_and_updates.sql"

    remove_lines_with_substring(file_path, substrings)
    print(f"The script was successfully saved to  {output_file}")


# Example of use
# File cleanup
open('differences_and_updates.sql', 'w').close()
# Path to mods_db folder
folder_path = "mods_db"
substrings = ["Tutorial"]  # Change it if you know for sure that this data crashes the start of the game
# !Case sensitive!

#  Go through all the files in the mods_db folder
for root, _, files in os.walk(folder_path):
    for filename in files:
        if filename.endswith(".sqlite"):
            mod_file = os.path.join(root, filename)
            generate_update_script("PhoenixShipData.sqlite", mod_file, "differences_and_updates.sql")
            print(f"File processed: {mod_file}")

remove_duplicates_from_file('differences_and_updates.sql')
