cask "awardtracker" do
  version "1.3.7"
  sha256 "d91e21ce5d31dff962405fb4808bfbcdf19ce60c6ebf5030b4306479539e3acc"

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
