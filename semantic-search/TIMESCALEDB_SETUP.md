# TimescaleDB Cloud Setup Guide

If you can't (or don't want to) use Docker, use TimescaleDB's managed cloud database instead.

## Prerequisites

- A free [TimescaleDB](https://www.timescale.com/) account

## Steps

### 1. Create a Free Trial Account

1. Go to [timescale.com](https://www.timescale.com/)
2. Click "Get Started Free"
3. Sign up with email/Google/GitHub

### 2. Create a New Service

1. Click "Create a Service"
2. Name it something like `semantic-search-lab`
3. **Important:** Select **"AI/ML" region** (this includes pgvector)
4. Choose any region close to you
5. Click "Create Service"

**Wait 2-3 minutes for provisioning to complete.**

### 3. Get Your Connection String

1. In your TimescaleDB dashboard, click on your service
2. Click "Connection" tab
3. Under "Connection String", copy the string (looks like: `postgresql://user:password@xyz.timescale.cloud:5432/tsdb`)

### 4. Paste Into utils.py

Open `utils.py` and update the `CONNECTION` variable at the top:

```python
CONNECTION = "postgresql://user:password@xyz.timescale.cloud:5432/tsdb"
```

Replace with your actual connection string from TimescaleDB.

### 5. Test It Works

```bash
python db_check.py
```

You should see: `✨ All checks passed! Your environment is ready.`

## Stopping/Starting

Your TimescaleDB instance runs in the cloud and is always on. You can:

- **Pause it** (saves money) in the dashboard
- **Resume it** when you need it again
- **Delete it** when done

## Troubleshooting

### "Connection refused" or "password authentication failed"
- Double-check you copied the entire connection string correctly
- Check the TimescaleDB dashboard to make sure the service is running
- Try resetting your password in the dashboard

### "Module pgvector not found"
- You didn't select "AI/ML" region when creating the service
- Create a new service and make sure to select the AI/ML region

### Connection string contains special characters
- If your password has `@` or `:` or other special characters, the connection string might look weird
- Copy-paste the entire string from the TimescaleDB dashboard—it handles escaping

## Questions?

The TimescaleDB support is usually helpful. You can also check their docs at [docs.timescale.com](https://docs.timescale.com/)
