# homebrew-awardtracker

Homebrew tap for **Award Tracker**, a local, privacy-focused travel rewards and mileage synchronization dashboard.

## Installation

To install **Award Tracker**, first tap this repository, then install the cask:

```bash
brew tap kevmando/awardtracker
brew install --cask awardtracker
```

Alternatively, you can install it directly:

```bash
brew install --cask kevmando/awardtracker/awardtracker
```

## How to use

Once installed, find **Award Tracker** in your `/Applications` directory or launch it via Spotlight.

## Uninstalling and cleaning up

To uninstall the application and completely remove all associated data (SQLite database, sync browser profiles, logs, etc.):

```bash
brew uninstall --cask --zap awardtracker
```

This will automatically clean up:
- The `AwardTracker.app` application bundle
- Local database, browser automation profiles, and cache directory under `~/Library/Application Support/AwardTracker`
- System preference plist files and saved application state
