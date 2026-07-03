import sys
import os
import re
import urllib.request
import hashlib
import glob

def parse_version(version_str):
    # Parse version string into a tuple of integers for comparison, e.g., "1.3.3" -> (1, 3, 3)
    # Handles potential suffixes like "-beta" by ignoring them or setting them to a low priority
    parts = re.split(r'[-+.]', version_str)
    num_parts = []
    for p in parts:
        try:
            num_parts.append(int(p))
        except ValueError:
            # For non-integer parts like 'beta', append a negative number so they sort earlier
            num_parts.append(-1)
    return tuple(num_parts)

def get_sha256(url):
    print(f"Downloading release asset from: {url}")
    sha256 = hashlib.sha256()
    try:
        # Use a custom user agent to avoid being blocked
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req) as response:
            while True:
                chunk = response.read(1024 * 64)
                if not chunk:
                    break
                sha256.update(chunk)
    except Exception as e:
        print(f"Error downloading the asset: {e}", file=sys.stderr)
        sys.exit(1)
    return sha256.hexdigest()

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_cask.py <new_version>", file=sys.stderr)
        sys.exit(1)

    new_version = sys.argv[1].strip()
    if new_version.startswith('v'):
        new_version = new_version[1:]

    cask_path = "Casks/awardtracker.rb"
    if not os.path.exists(cask_path):
        print(f"Error: Cask file not found at {cask_path}", file=sys.stderr)
        sys.exit(1)

    with open(cask_path, 'r') as f:
        content = f.read()

    # Find the current version
    version_match = re.search(r'^\s*version\s+"([^"]+)"', content, re.MULTILINE)
    if not version_match:
        print("Error: Could not find current version in cask file", file=sys.stderr)
        sys.exit(1)

    current_version = version_match.group(1)
    print(f"Current version in cask: {current_version}")
    print(f"Target version: {new_version}")

    if current_version == new_version:
        print("Version is already up to date. Exiting.")
        sys.exit(0)

    # 1. Back up old version
    backup_file = f"Casks/awardtracker@{current_version}.rb"
    print(f"Creating backup: {backup_file}")
    
    # Replace cask name in the backup file content
    backup_content = re.sub(
        r'cask\s+"awardtracker"\s+do',
        f'cask "awardtracker@{current_version}" do',
        content
    )
    
    with open(backup_file, 'w') as f:
        f.write(backup_content)

    # 2. Limit past versions to 5
    backup_pattern = "Casks/awardtracker@*.rb"
    backup_files = glob.glob(backup_pattern)
    
    # Parse version from path and pair them
    backups_with_versions = []
    for path in backup_files:
        # Extract version string e.g. "Casks/awardtracker@1.3.3.rb" -> "1.3.3"
        basename = os.path.basename(path)
        ver_match = re.search(r'awardtracker@([^.]+?(\.[^.]+?)*)\.rb', basename)
        if ver_match:
            ver_str = ver_match.group(1)
            backups_with_versions.append((parse_version(ver_str), path))

    # Sort backups ascending (oldest first)
    backups_with_versions.sort(key=lambda x: x[0])

    if len(backups_with_versions) > 5:
        num_to_delete = len(backups_with_versions) - 5
        print(f"Found {len(backups_with_versions)} backup files. Deleting the oldest {num_to_delete}:")
        for i in range(num_to_delete):
            old_backup_path = backups_with_versions[i][1]
            print(f"Removing old backup: {old_backup_path}")
            os.remove(old_backup_path)

    # 3. Calculate new checksum
    download_url = f"https://github.com/shyoo/awardtracker/releases/download/v{new_version}/awardtracker-macos-setup-v{new_version}.dmg"
    new_sha256 = get_sha256(download_url)
    print(f"New SHA256 checksum: {new_sha256}")

    # 4. Deploy new version to main cask file
    # Replace version
    updated_content = re.sub(
        r'^(\s*version\s+)"[^"]+"',
        rf'\1"{new_version}"',
        content,
        flags=re.MULTILINE
    )
    # Replace sha256
    updated_content = re.sub(
        r'^(\s*sha256\s+)"[^"]+"',
        rf'\1"{new_sha256}"',
        updated_content,
        flags=re.MULTILINE
    )

    with open(cask_path, 'w') as f:
        f.write(updated_content)

    print("Successfully updated main cask file.")

if __name__ == "__main__":
    main()
