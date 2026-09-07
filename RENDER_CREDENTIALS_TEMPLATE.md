# Render Environment Variables Template

Use this file as a scratchpad to break down your Render **Internal Database URL** before you copy and paste the values into the Render "Environment Variables" section.

---

### Step 1: Copy your Render URL here
*Example URL:* `postgres://inventory_db_user:Th1sIsARand0mP4ssw0rd@dpg-abc123xyz-a:5432/inventory_db`

**Your URL:** `(paste your URL here)`

---

### Step 2: Break it down into these variables

These are the exact values you need to click **"Add Environment Variable"** for on the Render website:

* **`SECRET_KEY`** = `django-insecure-random-string-for-render-only!`
* **`DEBUG`** = `False`
* **`DB_ENGINE`** = `django.db.backends.postgresql`
* **`DB_PORT`** = `5432`

Now, look at your URL from Step 1 and fill in the rest:

* **`DB_NAME`** = *(the database name at the very end of your URL)*
* **`DB_USER`** = *(the username right after `postgres://` in your URL)*
* **`DB_PASSWORD`** = *(the password between the `:` and `@` in your URL)*
* **`DB_HOST`** = *(the host between the `@` and `:5432` in your URL, usually starts with `dpg-`)*

---

### Step 3: Copy and Paste
Now that you have all the values written out above, go to your Render Web Service page and copy-paste them one by one into the **Environment Variables** section!
