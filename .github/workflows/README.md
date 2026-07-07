# GitHub Actions Workflows

This directory contains the automation workflows for maintaining and deploying the Homebrew Cask for **Award Tracker**.

Depending on your preference for automation and security (token sharing), you can configure this tap in one of three ways:

---

## Deployment Options

### Option 1: Manual Cask Management (No Automation, Safest)
*   **Best for:** Users who want zero security risks, no background scripts, and no GitHub tokens.
*   **How it works:** You manage the tap repository manually. Whenever a new upstream release is published, you manually download the release asset, calculate its SHA-256, and update `Casks/awardtracker.rb`.
*   **Setup required:** None. You don't need any workflows enabled or any tokens.

---

### Option 2: Semi-Automatic Update (Safe, Trigger/Schedule)
*   **Best for:** Users who want automation but do not want to create or share a Personal Access Token (PAT) between repositories.
*   **How it works:** Uses the `deploy-cask.yml` workflow along with `update_cask.py` in this tap repository. You can either run the update manually from the GitHub Actions tab or wait for the automatic daily cron schedule (checks upstream at 00:00 UTC).
*   **Setup required:**
    1. Keep `deploy-cask.yml` and `.github/scripts/update_cask.py` in this tap repository.
    2. Ensure the workflow has write permissions (`permissions: contents: write` is already set in the YAML).

---

### Option 3: Fully Automatic Update (Maximum Automation)
*   **Best for:** Maintainers who want the cask tap to update instantly whenever a release is published in the main repository.
*   **How it works:** A release in the upstream source repository (`shyoo/awardtracker`) triggers a dispatch event to this tap repository to kick off the upgrade.
    
    ```mermaid
    sequenceDiagram
        participant Upstream as shyoo/awardtracker (App Repo)
        participant Action1 as Main Repo (Dispatch Workflow)
        participant Action2 as Tap Repo (Deploy Workflow)
        participant CaskFile as Casks/awardtracker.rb

        Upstream->>Upstream: Publish Release (vX.Y.Z)
        Note over Upstream, Action1: Triggers dispatch-release.yml
        Action1->>Action2: Trigger repository_dispatch (new-release)
        Note over Action2: Triggers deploy-cask.yml
        Action2->>Action2: Run update_cask.py
        Action2->>CaskFile: Update version, download DMG, recalculate SHA256
        Action2->>CaskFile: Create backup & manage version limit (respecting .pinned)
        Action2->>Action2: Commit & push changes
    ```
*   **Setup required:** Follow the **Step-by-Step Setup** below to configure the webhook token.

---

## Step-by-Step Setup for Fully Automatic (Option 3)

### Step 1: Create a Personal Access Token (PAT)
1. Go to your GitHub profile settings -> **Developer settings** -> **Personal access tokens** -> **Fine-grained tokens** (recommended).
2. Click **Generate new token**.
3. Name it something descriptive like `Award Tracker Tap Dispatcher`.
4. Under **Repository access**, select **Only select repositories** and choose your tap repository (`kevmando/homebrew-awardtracker`).
5. Under **Permissions**, click **Repository permissions**:
   - Set **Contents** to **Read and write** (this grants the token permission to trigger repository dispatch events on that repository).
6. Click **Generate token** and copy it securely.

*Note: If you choose to use a **Classic PAT** instead, you must select the general `repo` scope.*

### Step 2: Add the Secret to the Source Repository
1. Go to your **upstream/source repository** page on GitHub (`shyoo/awardtracker`).
2. Go to **Settings** -> **Secrets and variables** (in the sidebar) -> **Actions**.
3. Click **New repository secret**.
4. Set the **Name** to: `TAP_GITHUB_TOKEN`.
5. Paste your copied token into the **Value** field.
6. Click **Add secret**.

### Step 3: Add the Dispatch Workflow to the Source Repository
1. Copy the contents of the reference file [.github/workflows/dispatch-release.yml](dispatch-release.yml) from this tap repository.
2. In your **upstream/source repository** (`shyoo/awardtracker`), create a new file at `.github/workflows/dispatch-release.yml`.
3. Paste the contents, commit, and push it.

> [!IMPORTANT]
> **The `dispatch-release.yml` file is placed in this tap repository for reference/backup, but it must be configured in the upstream source repository (`shyoo/awardtracker`) to function.**

---

## Workflow Details

### 1. Cask Deploy/Upgrade (`deploy-cask.yml`)
*   **Trigger:** Repository Dispatch (`new-release`), manual trigger (`workflow_dispatch`), or daily cron (`schedule`).
*   **Job Details:** Clones the repository, sets up Python, runs the update script, and commits/pushes the updated cask file along with any backup files.

### 2. Cask Update Script (`.github/scripts/update_cask.py`)
This helper script automates the update process:
1.  **Format Validation:** Uses regex to validate input versions to prevent directory traversal or malicious injection.
2.  **Backups:** Creates a copy of the current version as `Casks/awardtracker@<old_version>.rb`.
3.  **Version Pinning:** Reads `Casks/.pinned` to load protected versions that will never be deleted.
4.  **Cleanup (Retention):** Deletes older backups, maintaining a maximum of **5 unpinned versions** (this limit can be adjusted at [update_cask.py:L142-L143](../scripts/update_cask.py#L142-L143)).
5.  **Download & SHA256:** Downloads the macOS DMG setup from the upstream release to compute its SHA-256 hash.
6.  **Cask Upgrades:** Writes the new version number and calculated SHA-256 checksum to `Casks/awardtracker.rb`.

### 3. Cask Release Dispatcher (`dispatch-release.yml`)
*   **Trigger:** Release published in the source repository.
*   **Job Details:** Uses the `TAP_GITHUB_TOKEN` to call GitHub's repository dispatch API, sending the published tag name to the tap repository. Inputs are safely passed via environment variables to prevent command injection.
