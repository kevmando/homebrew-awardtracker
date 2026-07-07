cask "awardtracker@1.3.0" do
  version "1.3.0"
  sha256 "87299179059912d8e66d0fbb123224bd1411d4c6afc2fdbdc2631233343eea3c"

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
