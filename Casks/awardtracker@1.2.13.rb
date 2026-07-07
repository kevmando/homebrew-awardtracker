cask "awardtracker@1.2.13" do
  version "1.2.13"
  sha256 "c38e7a55eb8f21b38379c52638de9e43e6a3d73ea7e6774af6312bae785d7dea"

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
