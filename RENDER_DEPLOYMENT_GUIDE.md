# 🚀 Render Deployment Guide

Your project is already beautifully structured and almost 100% ready for Render deployment! You already have the `build.sh` script, `requirements.txt` with `gunicorn`, and `whitenoise` configured.

Here is the step-by-step guide to get your Inventory Management System live on Render.

## Step 1: Push your code to GitHub
Render pulls your code directly from GitHub, so your first step is to make sure your latest code is pushed to a repository on your GitHub account.

## Step 2: Create a PostgreSQL Database on Render
Before creating the web service, you need a live database for it to connect to.
1. Go to your [Render Dashboard](https://dashboard.render.com/).
2. Click **New** -> **PostgreSQL**.
3. Name it (e.g., `inventory-db`) and click **Create Database**.
4. Once created, scroll down to the **Connections** section and look for the **Internal Database URL** (you will need this in Step 4).

## Step 3: Create the Web Service
1. Go back to the Render Dashboard and click **New** -> **Web Service**.
2. Connect your GitHub repository containing this project.
3. Fill out the deployment details:
   - **Name:** `inventory-management-system`
   - **Environment:** `Python`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`

## Step 4: Add Environment Variables
Before clicking "Create", scroll down to **Environment Variables** and add all the variables from your local `.env` file, but use the live database credentials.

Click **Add Environment Variable** and add these:
* `SECRET_KEY` = `(make up a long random string)`
* `DEBUG` = `False`
* `DB_ENGINE` = `django.db.backends.postgresql`

Now, look at the **Internal Database URL** from Step 2. It looks something like this: `postgres://USER:PASSWORD@HOST:5432/DB_NAME`. Break it down and add the rest of the variables:
* `DB_NAME` = *(the database name from the URL)*
* `DB_USER` = *(the username from the URL)*
* `DB_PASSWORD` = *(the password from the URL)*
* `DB_HOST` = *(the host from the URL, usually starts with `dpg-`)*
* `DB_PORT` = `5432`

## Step 5: Deploy!
Click **Create Web Service**. 

Render will now run your `build.sh` script (installing packages, collecting static files, and migrating the live database) and then start Gunicorn. 

Once it says **Live**, click the URL at the top left to see your live project!
