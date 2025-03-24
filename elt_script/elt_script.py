import subprocess
import time
import os


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


if not wait_for_postgres(host="source_postgres"):
    exit(1)

if not wait_for_postgres(host="destination_postgres"):
    exit(1)

print("Starting ELT script...")

# Configuration for the source PostgreSQL database
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_postgres'
}

# Using pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w' 
]

# Setting the PGPASSWORD environment variable to avoid password prompt
subprocess_env = dict(PGPASSWORD=source_config['password'])

<<<<<<< HEAD:elt_script/elt_script.py
try:
    # Execute the dump command
    subprocess.run(dump_command, env=subprocess_env, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during pg_dump: {e}")
    exit(1)
=======
# Executing the dump command
subprocess.run(dump_command, env=subprocess_env, check=True)
>>>>>>> 856ca52978c5b323eec7dea0a89fda0e288a06c8:elt/elt_script.py

# Using psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

# Setting the PGPASSWORD environment variable for the destination database
subprocess_env = dict(PGPASSWORD=destination_config['password'])

<<<<<<< HEAD:elt_script/elt_script.py
try:
    # Execute the load command
    subprocess.run(load_command, env=subprocess_env, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error during psql load: {e}")
    exit(1)

# Clean up the dump file
os.remove('data_dump.sql')

=======
# Executing the load command
subprocess.run(load_command, env=subprocess_env, check=True)

>>>>>>> 856ca52978c5b323eec7dea0a89fda0e288a06c8:elt/elt_script.py
print("Ending ELT script...")
