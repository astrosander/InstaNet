import requests
import json
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()


# Load sensitive information from environment variables
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "X-CSRFToken": os.getenv("X_CSRF_TOKEN"),
    "X-IG-App-ID": os.getenv("X_IG_APP_ID"),
    "X-Requested-With": "XMLHttpRequest",
}

cookies = {
    "ig_did": os.getenv("IG_DID"),
    "datr": os.getenv("DATR"),
    "ds_user_id": os.getenv("DS_USER_ID"),
    "csrftoken": os.getenv("CSRF_TOKEN"),
    "sessionid": os.getenv("SESSION_ID"),
    "rur": os.getenv("RUR"),
}

def process_id(parse_id):
    """
    Fetch the list of users a given user ID is following.
    Skip processing if the data already exists in the folder.
    """
    # Define the output file path
    file_path = f"instagram_followers/{parse_id}.json"

    # Check if the file already exists; if so, skip processing
    if os.path.exists(file_path):
        print(f"Data for {parse_id} already exists. Skipping...")
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return [follower["id"] for follower in data]

    print(f"Fetching data for {parse_id}...")
    base_url = f"https://www.instagram.com/api/v1/friendships/{parse_id}/following/"
    all_followers = []
    max_id = None

    while True:
        # Prepare the URL with the current max_id (if present)
        url = f"{base_url}?count=200"
        if max_id:
            url += f"&max_id={max_id}"

        # Make the GET request
        response = requests.get(url, headers=headers, cookies=cookies)

        if response.status_code == 200:
            data = response.json()
            following_list = data.get("users", [])

            # Append the fetched users to the all_followers list
            all_followers.extend(
                {"id": user.get("id"), "username": user.get("username")} for user in following_list
            )

            # Check for more pages
            max_id = data.get("next_max_id")
            if not max_id:
                break  # Exit the loop if no more pages
        else:
            print(f"Failed to fetch followers for {parse_id}. Status code: {response.status_code}")
            break

    # Save all followers to a JSON file
    os.makedirs("instagram_followers", exist_ok=True)  # Ensure the folder exists
    with open(file_path, "w") as json_file:
        json.dump(all_followers, json_file, indent=4)

    # Extract follower IDs for further processing
    return [follower["id"] for follower in all_followers]


def main():
    """
    Main function to manage the fetching of Instagram data using multithreading.
    """
    # Replace this with a list of starting user IDs
    Points = ['15625857219']

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(process_id, Points)

        # Process the followers of each user in Points
        for user_followers in results:
            with ThreadPoolExecutor(max_workers=10) as follower_executor:
                follower_executor.map(process_id, user_followers)

if __name__ == "__main__":
    main()
