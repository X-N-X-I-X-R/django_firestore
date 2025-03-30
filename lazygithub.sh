#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Start time measurement
start=$(date +%s)

echo -e "${BOLD}${BLUE}=== LazyGitHub - Starting Process ===${NC}"

save_to_local_repo(){
      echo -e "${BOLD}${CYAN}=== Pushing Changes to GitHub ===${NC}"
      
      echo -e "${YELLOW}1. Adding files...${NC}"
      git add .
      
      echo -e "${YELLOW}2. Creating commit...${NC}"
      git commit -m "lazygithub{$(date +%Y%m%d_%H%M%S)}"
      
      echo -e "${YELLOW}3. Pushing changes to remote...${NC}"
      git push
      
      echo -e "${GREEN}=== Finished Pushing Changes ===${NC}"
      
      # Show final status
      echo -e "${BOLD}${CYAN}=== Current Repository Status ===${NC}"
      git status
      
      # Show recent commit history
      echo -e "${BOLD}${CYAN}=== Recent Commit History ===${NC}"
      git log -3 --oneline
}

merge_to_main(){
      echo -e "${BOLD}${MAGENTA}=== Merging to Main Branch ===${NC}"
      
      echo -e "${YELLOW}1. Switching to main branch...${NC}"
      git checkout main
      
      echo -e "${YELLOW}2. Pulling latest changes from main...${NC}"
      git pull origin main
      
      echo -e "${YELLOW}3. Merging current branch into main...${NC}"
      git merge -
      
      echo -e "${YELLOW}4. Pushing merged changes to main...${NC}"
      git push origin main
      
      echo -e "${YELLOW}5. Switching back to previous branch...${NC}"
      git checkout -
      
      echo -e "${GREEN}=== Finished Merging to Main ===${NC}"
}

# Run the functions
save_to_local_repo
merge_to_main

# End time measurement
end=$(date +%s)

# Calculate runtime
duration=$((end - start))

echo -e "${BOLD}${BLUE}=== Summary ===${NC}"
echo -e "${GREEN}Runtime: ${duration} seconds${NC}"
echo -e "${BOLD}${BLUE}=== LazyGitHub - Process Complete ===${NC}" 




