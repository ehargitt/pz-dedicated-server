#!/usr/bin/env python3
"""Update Project Zomboid server mod list from a Steam Workshop collection."""

import argparse
import glob
import json
import re
import sys
import urllib.request
import urllib.parse

STEAM_API = "https://api.steampowered.com"
COLLECTION_DETAILS_URL = f"{STEAM_API}/ISteamRemoteStorage/GetCollectionDetails/v1/"
FILE_DETAILS_URL = f"{STEAM_API}/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

DEFAULT_VOLUME_PATH = (
    "/home/ehargitt/.local/share/docker/volumes"
    "/pz-dedicated-server_pzserver-config/_data/Server"
)

MOD_ID_PATTERN = re.compile(r"Mod ?ID\s*:\s*(.+)", re.IGNORECASE)


def extract_collection_id(url):
    """Extract the numeric collection ID from a Steam Workshop URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    ids = params.get("id")
    if not ids:
        sys.exit(f"Error: Could not extract collection ID from URL: {url}")
    return ids[0]


def steam_post(url, data):
    """POST form-encoded data to a Steam API endpoint and return JSON."""
    encoded = urllib.parse.urlencode(data, doseq=True).encode()
    req = urllib.request.Request(url, data=encoded)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_collection_items(collection_id):
    """Return list of workshop item IDs in a collection."""
    data = {
        "collectioncount": "1",
        "publishedfileids[0]": collection_id,
    }
    result = steam_post(COLLECTION_DETAILS_URL, data)
    details = result.get("response", {}).get("collectiondetails", [])
    if not details or details[0].get("result") != 1:
        sys.exit(
            f"Error: Could not fetch collection {collection_id}. "
            "Is the URL correct and the collection public?"
        )
    children = details[0].get("children", [])
    return [item["publishedfileid"] for item in children]


def get_item_details(item_ids):
    """Return details for a list of workshop item IDs (batched in one call)."""
    data = {"itemcount": str(len(item_ids))}
    for i, fid in enumerate(item_ids):
        data[f"publishedfileids[{i}]"] = fid
    result = steam_post(FILE_DETAILS_URL, data)
    return result.get("response", {}).get("publishedfiledetails", [])


def parse_mod_ids(description):
    """Extract Mod IDs from a workshop item's description text.

    Returns a list of mod ID strings (split on ; if multiple are listed).
    """
    mod_ids = []
    for match in MOD_ID_PATTERN.finditer(description):
        raw = match.group(1).strip()
        # Strip any BBCode / HTML tags that Steam descriptions often contain
        raw = re.sub(r"\[/?[^\]]*\]", "", raw)
        raw = re.sub(r"<[^>]*>", "", raw)
        raw = raw.strip().rstrip(";")
        for part in re.split(r"[;\s]+", raw):
            part = part.strip()
            if part:
                mod_ids.append(part)
    return mod_ids


def find_ini_file():
    """Auto-detect the server .ini file in the Docker volume."""
    pattern = f"{DEFAULT_VOLUME_PATH}/*.ini"
    matches = glob.glob(pattern)
    if not matches:
        sys.exit(
            f"Error: No .ini files found in {DEFAULT_VOLUME_PATH}\n"
            "Use --ini to specify the path manually."
        )
    if len(matches) > 1:
        names = "\n  ".join(matches)
        sys.exit(
            f"Error: Multiple .ini files found:\n  {names}\n"
            "Use --ini to specify which one to update."
        )
    return matches[0]


def update_ini(ini_path, mod_ids, workshop_ids):
    """Update the Mods= and WorkshopItems= lines in the .ini file."""
    with open(ini_path, "r") as f:
        lines = f.readlines()

    mods_value = ";".join(mod_ids)
    workshop_value = ";".join(workshop_ids)
    found_mods = False
    found_workshop = False

    for i, line in enumerate(lines):
        if line.startswith("Mods="):
            lines[i] = f"Mods={mods_value}\n"
            found_mods = True
        elif line.startswith("WorkshopItems="):
            lines[i] = f"WorkshopItems={workshop_value}\n"
            found_workshop = True

    if not found_mods:
        lines.append(f"Mods={mods_value}\n")
    if not found_workshop:
        lines.append(f"WorkshopItems={workshop_value}\n")

    with open(ini_path, "w") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Update PZ server mods from a Steam Workshop collection."
    )
    parser.add_argument(
        "url",
        help="Steam Workshop collection URL",
    )
    parser.add_argument(
        "--ini",
        help="Path to the server .ini file (auto-detected if omitted)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without modifying the .ini file",
    )
    args = parser.parse_args()

    # 1. Extract collection ID
    collection_id = extract_collection_id(args.url)
    print(f"Collection ID: {collection_id}")

    # 2. Fetch collection contents
    print("Fetching collection items...")
    item_ids = get_collection_items(collection_id)
    print(f"Found {len(item_ids)} workshop items.")

    # 3. Fetch item details
    print("Fetching item details...")
    items = get_item_details(item_ids)

    # 4. Parse mod IDs from descriptions
    all_mod_ids = []
    seen_mod_ids = set()
    all_workshop_ids = []
    warnings = []

    for item in items:
        wid = item.get("publishedfileid", "???")
        title = item.get("title", "(unknown)")
        description = item.get("description", "")
        mod_ids = parse_mod_ids(description)

        if not mod_ids:
            warnings.append(f"  WARNING: No Mod ID found for '{title}' (workshop {wid})")
        else:
            for mid in mod_ids:
                if mid not in seen_mod_ids:
                    seen_mod_ids.add(mid)
                    all_mod_ids.append(mid)

        all_workshop_ids.append(wid)

    # 5. Print summary
    print(f"\n{'=' * 60}")
    print(f"Workshop items: {len(all_workshop_ids)}")
    print(f"Mod IDs found:  {len(all_mod_ids)}")
    if warnings:
        print(f"\n{len(warnings)} item(s) with missing Mod IDs:")
        for w in warnings:
            print(w)

    print(f"\nWorkshopItems={';'.join(all_workshop_ids)}")
    print(f"Mods={';'.join(all_mod_ids)}")
    print(f"{'=' * 60}")

    if args.dry_run:
        print("\n--dry-run: No files were modified.")
        return

    # 6. Update the ini file
    ini_path = args.ini or find_ini_file()
    print(f"\nUpdating: {ini_path}")
    update_ini(ini_path, all_mod_ids, all_workshop_ids)
    print("Done. Restart the server for changes to take effect:")
    print("  docker compose restart pzserver")


if __name__ == "__main__":
    main()
