#!/usr/bin/env fish

# Fix for "ENOSPC: System limit for number of file watchers reached" error
# This script increases the system's inotify watch limit

echo "🔧 Fixing file watcher limit issue..."
echo ""

# Check current limit
echo "Current file watcher limit:"
cat /proc/sys/fs/inotify/max_user_watches
echo ""

# Increase the limit temporarily (until reboot)
echo "Setting temporary limit (until reboot)..."
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl -p
echo ""

# Make the change permanent
echo "Making the change permanent..."
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
echo ""

echo "✅ File watcher limit increased!"
echo "New limit:"
cat /proc/sys/fs/inotify/max_user_watches
echo ""

echo "You can now run your dev server:"
echo "  bun nx run @evalio.click/evalio-ui:serve"
