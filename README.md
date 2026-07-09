# homebrew-awardtracker

Homebrew tap for **Award Tracker**, a local, privacy-focused travel rewards and mileage synchronization dashboard.

## Installation

To install **Award Tracker**, first tap this repository, trust it, and then install the cask:

```bash
brew tap kevmando/awardtracker
brew trust kevmando/awardtracker
brew install --cask awardtracker
```

> [!NOTE]
> Starting with Homebrew 6.0.0, third-party taps require explicit trust via `brew trust` before their formulae or casks can be evaluated and installed.

If you prefer to trust only this specific cask rather than the entire tap, you can run:

```bash
brew tap kevmando/awardtracker
brew trust --cask kevmando/awardtracker/awardtracker
brew install --cask awardtracker
```

Alternatively, you can install it directly (you will be prompted to trust the cask/tap during installation if it is not already trusted):

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
