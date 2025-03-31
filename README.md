# 🍲 Recipe App

A full-stack Django web application that lets users browse, create, and share recipes with ingredients, cooking instructions, ratings, and more. Includes search, comments, difficulty scoring, data visualizations, and image uploads via AWS S3.

---

## ⚙️ Tech Stack

- **Backend:** Django, SQLite/PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap
- **Media Storage:** Amazon S3 (via `django-storages`)
- **Deployment:** Heroku
- **Environment Management:** `python-dotenv`
- **Charting:** Matplotlib (served as base64 PNGs)
- **Authentication:** Django auth system (login, logout, register)

---

## 🧠 Key Features

- 📝 **Create, read, update, and delete recipes**
- 📸 **Image uploads** stored in **Amazon S3**
- ⭐ **Comments and ratings** (1–5 stars)
- 🔍 **Search functionality** by name or ingredient
- 📊 **Data visualizations** with chart types:
  - Cooking time bar chart
  - Difficulty pie chart
  - Ingredient count line chart
- 👥 **User accounts** with login/logout
- 🧠 **Automatic difficulty scoring** based on ingredients and cook time
- 🔗 Shareable recipe links
- 🛡️ Secure settings for production (Heroku + HTTPS)

---

## 🔒 Authentication

- Users can register, log in, and log out.
- Only authenticated users can create or comment on recipes.
- Only the user who created a recipe can edit it.

---

## 🖼️ Media & Images (Amazon S3)

Images are uploaded to an S3 bucket called:

```
aw2recipe-app-images
```

Your media URLs are served directly via:

```
https://aw2recipe-app-images.s3.amazonaws.com/recipes/<image-filename>
```

Configuration added to `settings.py`:

```python
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"
```

---

## 🚀 Deployment

- Hosted on Heroku at:  
  [https://recipe-app77.herokuapp.com](https://recipe-app77.herokuapp.com)

Heroku environment includes:

- `DEBUG=False` for production
- `DATABASE_URL` for PostgreSQL
- AWS credentials for S3 integration

---

## 💠 Local Setup

1. Clone the repo  
2. Create a virtual environment  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env`:
   ```dotenv
   DEBUG=True
   DJANGO_SECRET_KEY=your_secret_key
   AWS_ACCESS_KEY_ID=your_aws_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret
   AWS_STORAGE_BUCKET_NAME=your_bucket_name
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## 🔍 Search & Charts

- Search for recipes by keyword (name or ingredient)
- View interactive data visualizations on the **charts** page
- Chart types include:
  - 📊 Cooking Time (Bar)
  - 🥧 Difficulty Level (Pie)
  - 📈 Ingredients Used (Line)



