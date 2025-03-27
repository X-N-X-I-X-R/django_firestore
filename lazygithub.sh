#!/bin/bash

# Start time measurement
start=$(date +%s)

echo "=== LazyGitHub - Starting Process ==="

save_to_local_repo(){
      echo "=== Pushing Changes to GitHub ==="
      
      echo "1. Adding files..."
      git add .
      
      echo "2. Creating commit..."
      git commit -m "lazygithub{$(date +%Y%m%d_%H%M%S)}"
      
      echo "3. Pushing changes to remote..."
      git push
      
      echo "=== Finished Pushing Changes ==="
      
      # Show final status
      echo "=== Current Repository Status ==="
      git status
      
      # Show recent commit history
      echo "=== Recent Commit History ==="
      git log -3 --oneline
}

# Run the function
save_to_local_repo

# End time measurement
end=$(date +%s)

# Calculate runtime
duration=$((end - start))

echo "=== Summary ==="
echo "Runtime: $duration seconds"
echo "=== LazyGitHub - Process Complete ===" 




