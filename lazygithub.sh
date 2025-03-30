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

merge_to_main(){
      echo "=== Merging to Main Branch ==="
      
      echo "1. Switching to main branch..."
      git checkout main
      
      echo "2. Pulling latest changes from main..."
      git pull origin main
      
      echo "3. Merging current branch into main..."
      git merge -
      
      echo "4. Pushing merged changes to main..."
      git push origin main
      
      echo "5. Switching back to previous branch..."
      git checkout -
      
      echo "=== Finished Merging to Main ==="
}

# Run the functions
save_to_local_repo
merge_to_main

# End time measurement
end=$(date +%s)

# Calculate runtime
duration=$((end - start))

echo "=== Summary ==="
echo "Runtime: $duration seconds"
echo "=== LazyGitHub - Process Complete ===" 




