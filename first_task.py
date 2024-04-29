import asyncio
import os
import shutil
import logging
import argparse

logging.basicConfig(level=logging.ERROR)

async def read_folder(source_folder, destination_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            await copy_file(source_file, destination_folder)
    logging.info("All files copied successfully.")

async def copy_file(source_file, destination_folder):
    file_extension = os.path.splitext(source_file)[1]
    destination_folder = os.path.join(destination_folder, file_extension)

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    try:
        shutil.copy(source_file, destination_folder)
        logging.info(f"Copied {source_file} to {destination_folder}")
    except Exception as e:
        logging.error(f"Error copying {source_file}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Async file sorting script")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("destination_folder", help="Destination folder path")
    args = parser.parse_args()

    source_folder = args.source_folder
    destination_folder = args.destination_folder

    await read_folder(source_folder, destination_folder)

if __name__ == "__main__":
    asyncio.run(main())
