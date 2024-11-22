# Folder Synchronization Tool

## Overview
This project is a Python-based folder synchronization tool that maintains a full, identical copy of a source folder at a replica folder. It performs one-way synchronization, ensuring that the replica folder matches the source folder, and it continues this process periodically based on a user-defined interval.

## Features
- One-way synchronization from source to replica folder.
- Periodic synchronization using a user-specified interval.
- MD5 checksum to compare files and ensure exact matches.
- Logging of all operations, including file creations, removals, and MD5 comparisons.
- Simple and clear log file output for each synchronization cycle.

## How It Works
The script performs folder synchronization by:
1. Calculating MD5 checksums for files in both source and replica directories to determine if they are identical.
2. Creating, updating, or removing files and directories in the replica to ensure it matches the source.
3. Logging each operation to a log file and providing console output for immediate feedback.
4. Repeating the synchronization based on a user-defined interval.

The main functions include:

- **`calculate_md5(file_path)`**: This function calculates the MD5 hash of a file to determine if the contents have changed.
- **`synchronize_folders(source, replica, log_file_path)`**: This is the core function responsible for synchronizing the source and replica folders.
  - It walks through the source folder, calculates file checksums, and compares them with files in the replica.
  - It copies, removes, or creates files and directories in the replica as needed.
  - It logs each of these operations for transparency.
- **`log_action(log_file_path, message)`**: Logs all actions to both the console and the log file.

## Command Line Arguments
The script uses command line arguments to specify key parameters:
- **`source`**: Path to the source folder.
- **`replica`**: Path to the replica folder.
- **`interval`**: Synchronization interval in seconds.
- **`log_file`**: Path to the log file where all actions are logged.

Example usage:
```sh
python folder_sync.py /path/to/source /path/to/replica 60 /path/to/logfile.log
```
This command will synchronize the folders every 60 seconds and log the actions to the specified log file.

## Libraries Used
- **`os`** and **`shutil`**: Used for file and directory operations, such as walking through directories, copying, and removing files.
- **`hashlib`**: Utilized to calculate MD5 checksums for files, ensuring accurate content comparison.
- **`argparse`**: Provides a way to handle command line arguments, making the script more flexible and easy to use.
- **`time`**: Used to implement the synchronization interval.
- **`datetime`**: Used to timestamp log entries for better traceability.

No external third-party libraries were used for folder synchronization to keep the solution simple and efficient.

## How to Run
1. Clone the repository:
   ```sh
   git clone <repository-link>
   ```
2. Navigate to the directory:
   ```sh
   cd folder_sync_tool
   ```
3. Run the script with the necessary arguments as mentioned above.

## Log File Example
The log file will contain entries like:
```
[2024-11-22 18:23:13] File copied: /path/to/source/file.txt -> /path/to/replica/file.txt
[2024-11-22 18:23:13] Comparing MD5:
Source (/path/to/source/file.txt) = 8d75259537684a27ebff1409ee980430
Replica (/path/to/replica/file.txt) = 8d75259537684a27ebff1409ee980430
[2024-11-22 18:23:13] All files are identical. No changes needed.
```
This makes it easy to track each action taken by the script during synchronization.

## Conclusion
This folder synchronization tool is a simple yet powerful way to ensure that two folders remain identical. It provides reliable file comparison, detailed logging, and flexible command line options to suit different use cases.

Feel free to reach out if you have any questions or need further clarification on how this tool works!
