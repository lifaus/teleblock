# Teleblock

This script automates blocking users on a target Telegram account based on a list of users saved in a `blocked_users.json` file. It also provides functionality to verify blocked users on the target account.

## Features

1. **Block Users from a File**:
   - Reads a list of users from `blocked_users.json` and blocks them on the target Telegram account.

2. **Verify Blocked Users**:
   - Fetches and verifies the list of blocked users on the target Telegram account.

3. **Handles Rate Limits**:
   - Implements automatic waiting when hitting Telegram's rate limit.

4. **Error Handling**:
   - Logs and saves skipped users in a `skipped_users.json` file for manual review.

## Requirements

### Python Packages
- `telethon`
- `asyncio`

Install the required package:
```bash
pip install telethon
```

### Other Requirements
- **Telegram API credentials**: You need your `api_id` and `api_hash` from [Telegram's API Development Tools](https://my.telegram.org/).
- **Phone Number**: The phone number associated with the Telegram account where users will be blocked.

## Setup

1. Clone or download this repository.
2. Create and configure `blocked_users.json`. Each entry in the file must be a JSON object with `id` or `username` (or both). Example:

    ```json
    [
        {"id": 123456789, "username": "exampleuser1"},
        {"id": 987654321, "username": "exampleuser2"}
    ]
    ```
3. Update the following variables in the script:
   - `api_id_target`: Your Telegram API ID.
   - `api_hash_target`: Your Telegram API hash.
   - `phone_number_target`: Your Telegram phone number.

## Usage

### Running the Script

Run the script using the following command:

```bash
python main.py
```

The script will:
1. Load users from `blocked_users.json`.
2. Block each user on the target Telegram account.
3. Save skipped users (if any) to `skipped_users.json`.
4. Verify and log the total number of blocked users.

### Output Files
- **`skipped_users.json`**: Contains users that could not be blocked due to errors.

## Notes

- **Rate Limit Handling**:
  The script pauses automatically when encountering rate limits (`FloodWaitError`).

- **File Dependencies**:
  Ensure that `blocked_users.json` exists in the same directory before running the script. If the file is missing, the script will terminate with an error.

- **Skipped Users**:
  Users who cannot be blocked due to errors are saved in `skipped_users.json` for further review.

## Troubleshooting

- **File Not Found Error**:
  Ensure `blocked_users.json` exists in the script directory.

- **Authentication Issues**:
  Double-check the `api_id`, `api_hash`, and `phone_number` values. Ensure they match the target Telegram account.

- **FloodWaitError**:
  If you encounter frequent rate limit errors, consider reducing the script's execution speed by increasing the `asyncio.sleep(2)` interval.

## License
This script is free to use and modify. No warranty is provided.
