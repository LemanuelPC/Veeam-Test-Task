import os
import time
import shutil
import hashlib
import argparse
from datetime import datetime

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def synchronize_folders(source, replica, log_file_path):
    source_files = {}
    for root, dirs, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, source)
            source_files[relative_path] = file_path

    files_changed = 0
    dirs_changed = 0
    all_same = True

    # Synchronize files from source to replica
    for relative_path, source_file_path in source_files.items():
        replica_file_path = os.path.join(replica, relative_path)
        source_md5 = calculate_md5(source_file_path)
        if not os.path.exists(replica_file_path):
            all_same = False
            replica_dir = os.path.dirname(replica_file_path)
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                log_action(log_file_path, f"Directory created: {replica_dir}")
                dirs_changed += 1
            shutil.copy2(source_file_path, replica_file_path)
            log_action(log_file_path, f"File copied: {source_file_path} -> {replica_file_path}")
            files_changed += 1
        else:
            replica_md5 = calculate_md5(replica_file_path)
            log_action(log_file_path, f"Comparing MD5:\nSource ({source_file_path}) = {source_md5}\nReplica ({replica_file_path}) = {replica_md5}")
            if source_md5 != replica_md5:
                all_same = False
                shutil.copy2(source_file_path, replica_file_path)
                log_action(log_file_path, f"File copied: {source_file_path} -> {replica_file_path}")
                files_changed += 1

    # Remove files and directories from replica that are not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        for file in files:
            replica_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(replica_file_path, replica)
            if relative_path not in source_files:
                all_same = False
                os.remove(replica_file_path)
                log_action(log_file_path, f"File removed: {replica_file_path}")
                files_changed += 1

        for dir in dirs:
            replica_dir_path = os.path.join(root, dir)
            if not os.listdir(replica_dir_path):
                all_same = False
                os.rmdir(replica_dir_path)
                log_action(log_file_path, f"Directory removed: {replica_dir_path}")
                dirs_changed += 1

    if all_same:
        log_action(log_file_path, "All files are identical. No changes needed.")
    else:
        log_action(log_file_path, f"Synchronization complete. Files changed: {files_changed}, Directories changed: {dirs_changed}.")

    # Add a paragraph to separate each synchronization cycle
    with open(log_file_path, "a") as log_file:
        log_file.write("\n")

def log_action(log_file_path, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message + "\n")

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder.")
    parser.add_argument("replica", help="Path to the replica folder.")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds.")
    parser.add_argument("log_file", help="Path to the log file.")
    args = parser.parse_args()

    source = args.source
    replica = args.replica
    interval = args.interval
    log_file_path = args.log_file

    while True:
        synchronize_folders(source, replica, log_file_path)
        time.sleep(interval)

if __name__ == "__main__":
    main()
