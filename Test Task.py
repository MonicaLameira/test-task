import os
import shutil
import time
import logging

def synchronize_folders(source_folder, replica_folder, interval, log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s')

    while True:
        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_path = os.path.join(replica_folder, relative_path)

            # Create directories in replica if they don't exist
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)

            # Copy files to replica, overwriting existing ones
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_path, file)

                if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info("Copied {source_file} to {replica_file}")

        # Remove files from replica that are not in source
        for root, dirs, files in os.walk(replica_folder):
            relative_path = os.path.relpath(root, replica_folder)
            source_path = os.path.join(source_folder, relative_path)

            for file in files:
                source_file = os.path.join(source_path, file)
                if not os.path.exists(source_file):
                    os.remove(os.path.join(root, file))
                    logging.info("Removed {os.path.join(root, file)}")

        time.sleep(interval)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Synchronize folders')
    parser.add_argument('source_folder', help='Source folder path')
    parser.add_argument('replica_folder', help='Replica folder path')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', help='Log file path')
    args = parser.parse_args()

    synchronize_folders(args.source_folder, args.replica_folder, args.interval, args.log_file)