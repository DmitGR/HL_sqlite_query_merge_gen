import sqlite3

def execute_update_script(db_path, sql_query_path, log_path):
    # Database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    total_queries = 0
    successful_queries = 0

    # Open the log file
    with open(log_path, 'w') as log_file:
        log_file.write("Query execution logs:\n")

        # Read the SQL query file
        with open(sql_query_path, 'r') as script_file:
            for line in script_file:
                line = line.strip()
                if not line:  # Skip the blank lines
                    continue

                total_queries += 1
                try:
                    # Running the query
                    cursor.execute(line)
                    conn.commit()
                    successful_queries += 1
                    log_file.write(f"SUCCESS: {line}\n")
                except Exception as e:
                    # Logging the error
                    conn.rollback()
                    log_file.write(f"ERROR: {line}\nReason: {e}\n")
                    print(f"Error during query execution: {line}\nReason: {e}")

    # Closing the connection
    conn.close()

    # Statistics output
    print(f"Total requests: {total_queries}")
    print(f"Successfully completed: {successful_queries}")
    print(f"Failed: {total_queries - successful_queries}")

    # Logging the summary statistics
    with open(log_path, 'a') as log_file:
        log_file.write("\nExecution statistics:\n")
        log_file.write(f"Total requests: {total_queries}\n")
        log_file.write(f"Successfully completed: {successful_queries}\n")
        log_file.write(f"Failed: {total_queries - successful_queries}\n")


# Example of use
execute_update_script("Updated/PhoenixShipData.sqlite", "differences_and_updates.sql", "execution_log.txt")
