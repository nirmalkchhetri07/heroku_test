# 🚀 Git & Heroku CLI Cheat Sheet

A quick reference for common **Git** and **Heroku CLI** commands used when deploying applications.

---

# 📦 Git Commands

## Initialize Repository
```bash
git init
```

## Check Status
```bash
git status
```

## Add Files
```bash
git add .
```

Add a specific file

```bash
git add filename
```

## Commit Changes
```bash
git commit -m "commit message"
```

## Create / Rename Branch
```bash
git branch -M main
```

## View Branches
```bash
git branch
```

## Add Remote Repository
```bash
git remote add origin https://github.com/username/repository.git
```

## View Remote
```bash
git remote -v
```

## Push Code
```bash
git push -u origin main
```

## Pull Updates
```bash
git pull origin main
```

## Clone Repository
```bash
git clone https://github.com/username/repository.git
```

---

# 🌐 Heroku CLI Commands

## Login to Heroku
```bash
heroku login
```

## Create Heroku App
```bash
heroku create app-name
```

Example

```bash
heroku create myflaskapp
```

## Add Heroku Remote
```bash
git remote add heroku https://git.heroku.com/app-name.git
```

## Deploy App to Heroku
```bash
git push heroku main
```

## Open Deployed App
```bash
heroku open
```

## View Logs
```bash
heroku logs --tail
```

## Restart App
```bash
heroku restart
```

## Check App Info
```bash
heroku info
```

## List All Apps
```bash
heroku apps
```

## Delete App
```bash
heroku apps:destroy app-name
```

---

# 📂 Minimal Flask Heroku Project Structure

```
project/
│
├── app.py
├── requirements.txt
├── Procfile
├── .gitignore
└── README.md
```

---

# 🧾 Example Procfile

```
web: python app.py
```

---

# 📜 Example requirements.txt

```
flask
gunicorn
```

---

# ⚡ Quick Deployment Steps

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
heroku login
heroku create myapp
git push heroku main
heroku open
```

---

# 💡 Tips

- Always use **requirements.txt** (not requirement.txt)
- Never upload **venv/**
- Use `.gitignore` to ignore unnecessary files

Example `.gitignore`

```
venv/
__pycache__/
*.pyc
.env
```

---

# 🔗 Useful Links

- https://git-scm.com/docs
- https://devcenter.heroku.com/