import asyncio
import json
from telethon import TelegramClient
from telethon.tl.functions.contacts import BlockRequest, GetBlockedRequest
from telethon.errors import FloodWaitError

api_id_target = 'API_TARGET'
api_hash_target = 'API_HASH'
phone_number_target = 'PHONE_NUMBER'

BLOCKED_USERS_FILE = "blocked_users.json"

target_client = TelegramClient('target_session', api_id_target, api_hash_target)


async def block_users_from_file(client):
    """Block all users from the blocked_users.json file"""
    try:
        with open(BLOCKED_USERS_FILE, "r") as file:
            blocked_users = json.load(file)
    except FileNotFoundError:
        print(f"File {BLOCKED_USERS_FILE} not found. Make sure to run the fetching script first.")
        return

    print(f"Loaded {len(blocked_users)} users from {BLOCKED_USERS_FILE}.")
    total_blocked = 0
    skipped_users = []

    print("Connecting to Telegram...")
    await client.start(phone_number_target)

    for idx, user in enumerate(blocked_users):
        try:
            print(f"[{idx + 1}/{len(blocked_users)}] Blocking user {user['username'] or user['id']}...")
            if user.get("username"):
                entity = await client.get_entity(user["username"])
            else:
                entity = await client.get_input_entity(user["id"])

            await client(BlockRequest(entity))
            print(f"Blocked user {user['username'] or user['id']}.")
            total_blocked += 1
            await asyncio.sleep(2)
        except FloodWaitError as e:
            print(f"Rate limit hit. Waiting for {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"Error blocking user {user['username'] or user['id']}: {e}")
            skipped_users.append(user)

    print(f"Total users blocked on target account: {total_blocked}")
    if skipped_users:
        print(f"Skipped users: {len(skipped_users)}")
        with open("skipped_users.json", "w") as skipped_file:
            json.dump(skipped_users, skipped_file, indent=4)
        print("Saved skipped users to skipped_users.json.")



async def verify_blocked_users(client):
    """Fetch the list of blocked users from the target account."""
    print("Fetching blocked users from target account for verification...")
    offset = 0
    limit = 100
    blocked_users = []

    while True:
        result = await client(GetBlockedRequest(offset=offset, limit=limit))
        if not result.users:
            break

        blocked_users.extend([user.id for user in result.users])
        offset += len(result.users)

    print(f"Verified {len(blocked_users)} users are blocked on the target account.")
    return set(blocked_users)


async def main():
    async with target_client:
        await block_users_from_file(target_client)
        blocked_users = await verify_blocked_users(target_client)
        print(f"Blocked users on target account: {len(blocked_users)}")


if __name__ == "__main__":
    asyncio.run(main())
