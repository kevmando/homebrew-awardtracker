cask "awardtracker" do
  version "1.3.4"
  sha256 "757a038d37b4cc44b6332aae10de02141f371161aa8a8de81e1c42eae66ef980"

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
