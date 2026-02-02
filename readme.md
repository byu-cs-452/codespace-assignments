# CS-452 Codespace Assignments

This repository contains GitHub Codespace-ready assignments for BYU CS-452 Data Engineering. Each assignment provides a **fully configured development environment** that runs in the cloud—no local setup required.

## Getting Started

1. **Fork this repository** to your own GitHub account
2. **Open in Codespace**: Click the green "Code" button → "Codespaces" → "Create codespace on main"
3. Wait for the environment to build (first time takes ~2-3 minutes)
4. Navigate to the assignment folder you're working on

## Assignments

| Assignment | Description |
|------------|-------------|
| [semantic-search](./semantic-search/) | Build a podcast recommender system using pgvector and semantic search |

## GitHub Codespaces Free Tier

GitHub provides **free Codespace hours** each month:

| Account Type | Free Hours/Month | Free Storage |
|--------------|------------------|--------------|
| **Free (no Student Pack)** | 60 hours | 15 GB |
| **GitHub Pro / Student Developer Pack** | 180 hours | 20 GB |

### Tips to Maximize Free Hours:
- ⏸️ **Stop your Codespace** when not in use (it auto-stops after 30 min idle)
- 🗑️ **Delete old Codespaces** you no longer need
- ⚡ **Use the 2-core machine** (default) to stretch your hours further

### Get More Free Hours
If you haven't already, sign up for the **GitHub Student Developer Pack**:
1. Go to [education.github.com/pack](https://education.github.com/pack)
2. Verify your `.edu` email
3. Get **180 hours/month** (3x the free tier!) plus tons of other benefits

## How Codespaces Work

- Each Codespace is a **full VS Code environment** running in the cloud
- Your code is **saved in the Codespace**, commit & push to save to GitHub
- You can **stop/start** your Codespace to save compute hours
- The environment includes **Postgres with pgvector** pre-configured

## Troubleshooting

### Codespace won't start
- Check your [Codespace usage](https://github.com/settings/billing/summary) to ensure you have hours remaining
- Try creating a new Codespace

### Database issues
```bash
# Check if Postgres is running
docker ps

# Rebuild the container (fixes most issues)
# Press: Ctrl+Shift+P → "Rebuild Container"
```

### Need help?
Post on the class discussion board or attend office hours.

---

**Happy coding! 🚀**
