#!/bin/bash

# GitHub username
USERNAME="violetta__"

# Function to make API request
make_api_request() {
    local endpoint=$1
    curl -s "https://api.github.com/users/$USERNAME/$endpoint"
}

# Make API request to fetch user repositories
user_repos=$(make_api_request "repos")
echo "User Repositories:"
echo "$user_repos" | jq '.[].name'
