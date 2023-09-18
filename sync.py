import os
import shutil
import argparse
import time

def FolderSync(src_folder, rep_folder, log_file):
    try:
        if not os.path.exists(rep_folder):
            os.makedirs(rep_folder)

        with open(log_file, 'a') as log:
            log.write(f"Synchronization started at {time.ctime()}\n")

        for root, _, files in os.walk(src_folder):
            relative_path = os.path.relpath(root, src_folder)
            rep_path = os.path.join(rep_folder, relative_path)

            if not os.path.exists(rep_path):
                os.makedirs(rep_path)

            for file in files:
                src_file = os.path.join(root, file)
                rep_file = os.path.join(rep_path, file)

                if not os.path.exists(rep_file) or (os.path.getmtime(src_file) > os.path.getmtime(rep_file)):
                    shutil.copy2(src_file, rep_file)
                    with open(log_file, 'a') as log:
                        log.write(f"Copied: {src_file} -> {rep_file}\n")
                    print(f"Copied: {src_file} -> {rep_file}")

        for root, _, files in os.walk(rep_folder):
            relative_path = os.path.relpath(root, rep_folder)
            src_path = os.path.join(src_folder, relative_path)

            for file in files:
                rep_file = os.path.join(root, file)
                src_file = os.path.join(src_path, file)

                if not os.path.exists(src_file):
                    os.remove(rep_file)
                    with open(log_file, 'a') as log:
                        log.write(f"Removed: {rep_file}\n")
                    print(f"Removed: {rep_file}")

        with open(log_file, 'a') as log:
            log.write(f"Synchronization completed at {time.ctime()}\n")
        print(f"Synchronization completed at {time.ctime()}")

    except Exception as e:
        with open(log_file, 'a') as log:
            log.write(f"Error: {str(e)}\n")
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Folder Synchronization Program')
    parser.add_argument('src_folder')
    parser.add_argument('rep_folder')
    parser.add_argument('log_file')
    parser.add_argument('--interval', type=int, default=60)

    args = parser.parse_args()

    while True:
        FolderSync(args.src_folder, args.rep_folder, args.log_file)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
