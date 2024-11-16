import os
import cryptpandas as crp
from scripts.slack_passcode import get_all_file_passcodes

def decrypt_data(file_path, passcode):

    try:
        # Use cryptpandas to read the encrypted file
        decrypted_data = crp.read_encrypted(file_path, password=passcode)
        print(f"Successfully decrypted: {file_path}")
        return decrypted_data
    except Exception as e:
        print(f"Error decrypting {file_path} with passcode {passcode}: {e}")
        return None


def decrypt_all_files(channel_id, raw_dir="./data/raw/", decrypted_dir="./data/decrypted/"):

    # Ensure the decrypted directory exists
    os.makedirs(decrypted_dir, exist_ok=True)

    # Get all file-passcode pairs from Slack
    file_passcodes = get_all_file_passcodes(channel_id)

    for filename, passcode in file_passcodes:
        raw_file_path = os.path.join(raw_dir, filename)
        decrypted_file_path = os.path.join(decrypted_dir, filename.replace(".crypt", ".csv"))

        if not os.path.exists(raw_file_path):
            print(f"File not found: {raw_file_path}, skipping.")
            continue

        print(f"Decrypting {filename}..")
        decrypted_data = decrypt_data(raw_file_path, passcode)
        if decrypted_data is not None:
            # Save the decrypted data
            decrypted_data.to_csv(decrypted_file_path, index=False)
            print(f"Decrypted file saved: {decrypted_file_path}")
        else:
            print(f"Failed to decrypt {filename} with passcode {passcode}.")