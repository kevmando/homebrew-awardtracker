cask "awardtracker" do
  version "1.3.5"
  sha256 "43227293e35666f9adf8d29f0eeb2bb86bcdd3c5a9ef30eeceb0dc591f6cda55"

  url "https://github.com/shyoo/awardtracker/releases/download/v#{version}/awardtracker-macos-setup-v#{version}.dmg"
  name "Award Tracker"
  desc "Local, privacy-focused travel rewards and mileage synchronization dashboard"
  homepage "https://github.com/shyoo/awardtracker"

  depends_on :macos

  app "AwardTracker.app"

  zap trash: [
    "~/Library/Application Support/AwardTracker",
    "~/Library/Preferences/com.awardtracker.app.plist",
    "~/Library/Saved Application State/com.awardtracker.app.savedState",
  ]
end
