# 🚀 GitHub Setup Guide

## Step-by-Step Instructions to Push to GitHub

### 1. Create a New Repository on GitHub

1. Go to [GitHub](https://github.com)
2. Click the **"+"** button (top right) → **"New repository"**
3. Fill in the details:
   - **Repository name**: `smart-expense-tracker`
   - **Description**: `ML-powered expense tracker with auto-categorization and anomaly detection`
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT** check "Initialize with README" (we already have one)
4. Click **"Create repository"**

### 2. Push Your Local Repository to GitHub

GitHub will show you commands. We've already initialized Git locally, so run:

```bash
cd C:\Users\anush\Desktop\kiro_expense_tracker\expense-tracker

# Add your GitHub repository as remote
git remote add origin https://github.com/anushka-n2204/smart-expense-tracker.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### 3. Enter Credentials

When prompted:
- **Username**: anushka-n2204
- **Password**: Your GitHub Personal Access Token (not your actual password)

#### How to Create a Personal Access Token:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Expense Tracker"
4. Select scopes: Check **repo** (full control)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

### 4. Verify Upload

After pushing, refresh your GitHub repository page. You should see all your files!

## Alternative: Using GitHub Desktop

### If you prefer a GUI:

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in with your GitHub account
3. Click "Add" → "Add existing repository"
4. Browse to: `C:\Users\anush\Desktop\kiro_expense_tracker\expense-tracker`
5. Click "Publish repository"
6. Uncheck "Keep this code private" if you want it public
7. Click "Publish repository"

## Making Changes Later

After making changes to your code:

```bash
# Stage all changes
git add .

# Commit with a message
git commit -m "Add: description of what you changed"

# Push to GitHub
git push
```

## Common Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# View remotes
git remote -v
```

## Repository Settings on GitHub

### Enable GitHub Pages (Optional)

If you want to host documentation:
1. Go to repository Settings
2. Click "Pages" in sidebar
3. Select source: main branch, /docs folder
4. Save

### Add Topics (Recommended)

Add relevant topics to make your repo discoverable:
- Click "⚙️" next to About section
- Add topics: `machine-learning`, `expense-tracker`, `streamlit`, `python`, `ml-project`, `data-science`, `finance-app`

### Create Releases

To create a release:
1. Go to "Releases" → "Create a new release"
2. Tag: v1.0
3. Title: "Version 1.0 - Initial Release"
4. Description: List features
5. Attach files if needed
6. Click "Publish release"

## Collaboration

### Accepting Contributions

If you want others to contribute:
1. Add CONTRIBUTING.md (✅ already included)
2. Go to Settings → Collaborators
3. Add collaborators

### Branch Protection

To protect your main branch:
1. Settings → Branches
2. Add rule for "main"
3. Enable "Require pull request reviews"

## Troubleshooting

### "Authentication failed"
- Use Personal Access Token, not password
- Check token has correct permissions

### "Repository not found"
- Verify repository name matches
- Check you have access rights

### "Permission denied"
- Use HTTPS URL, not SSH (unless you've set up SSH keys)

### "Changes not showing"
- Make sure you committed: `git commit -m "message"`
- Then push: `git push`

## Your Repository URL

Once created, your repository will be at:
**https://github.com/anushka-n2204/smart-expense-tracker**

Share this URL to showcase your project! 🎉
