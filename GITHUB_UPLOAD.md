# Step-by-Step Guide: Upload to GitHub

## Prerequisites

1. **GitHub Account**: Make sure you have a GitHub account at https://github.com
2. **Git Installed**: You already have git (it's working in your project)

## Step-by-Step Instructions

### Step 1: Commit Your Current Changes

First, let's commit all the new files and changes we made:

```bash
# Navigate to your project (if not already there)
cd /Users/clairenewsom/budget-analyzer

# Check what files have changed
git status

# Add all files to staging
git add .

# Commit with a descriptive message
git commit -m "Add comprehensive documentation, LICENSE, and project improvements"
```

### Step 2: Create a GitHub Repository

**Option A: Using GitHub Website (Recommended for beginners)**

1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `budget-analyzer` (or any name you prefer)
   - **Description**: "Personal Budget Analyzer API - Flask-based REST API for expense tracking and financial forecasting"
   - **Visibility**: Choose **Public** (required for assignment) or **Private**
   - **DO NOT** check "Initialize this repository with a README" (we already have one)
   - **DO NOT** add .gitignore or license (we already have them)
5. Click **"Create repository"**

**Option B: Using GitHub CLI (if you have it installed)**

```bash
gh repo create budget-analyzer --public --description "Personal Budget Analyzer API"
```

### Step 3: Connect Your Local Repository to GitHub

After creating the repository on GitHub, you'll see a page with setup instructions. Copy the repository URL (it will look like):
```
https://github.com/YOUR_USERNAME/budget-analyzer.git
```

Then run these commands (replace `YOUR_USERNAME` with your actual GitHub username):

```bash
# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/budget-analyzer.git

# Verify it was added
git remote -v
```

**If you already have a remote named "origin", you can either:**
- Remove it first: `git remote remove origin`
- Or use a different name: `git remote add github https://github.com/YOUR_USERNAME/budget-analyzer.git`

### Step 4: Push Your Code to GitHub

```bash
# Push to GitHub (first time)
git push -u origin main
```

If you get an authentication error, you may need to:
- Use a Personal Access Token instead of password
- Or set up SSH keys

### Step 5: Verify Upload

1. Go to your GitHub repository page: `https://github.com/YOUR_USERNAME/budget-analyzer`
2. You should see all your files:
   - README.md
   - src/app.py
   - Dockerfile
   - requirements.txt
   - LICENSE
   - etc.

### Step 6: Update README with GitHub Link

Edit your README.md and replace `[INSERT-REPO-URL]` with your actual GitHub URL:

```bash
# Open README.md and find the line:
# GitHub Repo: [INSERT-REPO-URL]
# Replace it with:
# GitHub Repo: https://github.com/YOUR_USERNAME/budget-analyzer
```

Then commit and push:
```bash
git add README.md
git commit -m "Update README with GitHub repository link"
git push
```

## Troubleshooting

### Authentication Issues

**If you get "Authentication failed" or "Permission denied":**

1. **Use Personal Access Token (PAT)**:
   - Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with `repo` permissions
   - Use the token as your password when pushing

2. **Or set up SSH keys**:
   ```bash
   # Generate SSH key (if you don't have one)
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to SSH agent
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   
   # Copy public key
   cat ~/.ssh/id_ed25519.pub
   # Then add it to GitHub → Settings → SSH and GPG keys
   
   # Change remote to use SSH
   git remote set-url origin git@github.com:YOUR_USERNAME/budget-analyzer.git
   ```

### "Branch 'main' has no upstream branch"

If you see this error, use:
```bash
git push -u origin main
```

The `-u` flag sets up tracking.

### "Repository already exists" Error

If the remote already exists:
```bash
# Check current remotes
git remote -v

# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/budget-analyzer.git
```

## Quick Reference Commands

```bash
# 1. Commit changes
git add .
git commit -m "Your commit message"

# 2. Add remote (first time only)
git remote add origin https://github.com/YOUR_USERNAME/budget-analyzer.git

# 3. Push to GitHub
git push -u origin main

# 4. Future updates (after initial push)
git add .
git commit -m "Update message"
git push
```

## Next Steps After Uploading

1. ✅ Verify all files are on GitHub
2. ✅ Update README.md with your GitHub URL
3. ✅ Make sure LICENSE file is visible
4. ✅ Check that .env is NOT uploaded (it should be in .gitignore)
5. ✅ Test that someone else can clone and run your project

