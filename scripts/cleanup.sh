#!/bin/bash
# MusicAITools Project Cleanup Script
# Used to remove temporary files, cache files, and other files that should not be committed to version control

echo "================ MusicAITools Cleanup Script ================"
echo "Cleaning unnecessary files..."

# Clean Python cache files
echo "Cleaning Python cache files..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyd" -delete

# Clean system files
echo "Cleaning system metadata files..."
find . -name ".DS_Store" -delete
find . -name "._.DS_Store" -delete
find . -name "Thumbs.db" -delete

# Clean editor temporary files
echo "Cleaning editor temporary files..."
find . -name "*~" -delete
find . -name "*.swp" -delete
find . -name "*.swo" -delete
find . -name ".*.sw*" -delete

# Clean backup files
echo "Cleaning backup files..."
find . -name "*.bak" -delete

# Check for test generated temporary files
TEST_OUTPUTS=$(find . -not -path "*/tests/test_data/*" -not -path "*/docs/images/*" -name "test_*.png" -o -name "test_*.mp3" -o -name "test_*.wav")
if [ -n "$TEST_OUTPUTS" ]; then
  echo "Found test output files (excluding test data directory and documentation images):"
  echo "$TEST_OUTPUTS"
  read -p "Do you want to delete these files? (y/n): " choice
  if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
    echo "$TEST_OUTPUTS" | xargs rm -f
    echo "Test output files deleted"
  else
    echo "Test output files preserved"
  fi
fi

# Confirm cleanup completion
echo "================ Cleanup Complete ================"
echo "Your project is now clean and ready for commit!"
echo "Remember to add the following patterns to your .gitignore file to prevent these files from being re-added:"
echo "
# Python cache
__pycache__/
*.py[cod]
*$py.class

# System files
.DS_Store
._.DS_Store
Thumbs.db

# Editor files
*~
*.swp
*.swo
.*.sw*

# Backup files
*.bak

# Test outputs
test_*.png
test_*.mp3
test_*.wav

# Large media files (except test data)
/output/
" 