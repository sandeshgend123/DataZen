# DataZen Analytics - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### For Windows Users:

#### Option 1: Automated Setup (Easiest)
1. Double-click `setup.bat`
2. Wait for the script to complete
3. When prompted, create your admin account:
   ```
   Username: admin
   Email: admin@datazen.com
   Password: (your password)
   ```
4. Double-click `run.bat` to start the server

#### Option 2: Manual Setup
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python datazen_website\manage.py migrate

# Create admin user
python datazen_website\manage.py createsuperuser

# Run server
python datazen_website\manage.py runserver
```

---

### For macOS/Linux Users:

#### Option 1: Automated Setup (Easiest)
1. Open terminal in project folder
2. Run: `bash setup.sh`
3. Create your admin account when prompted
4. Run: `bash run.sh` to start the server

#### Option 2: Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python datazen_website/manage.py migrate

# Create admin user
python datazen_website/manage.py createsuperuser

# Run server
python datazen_website/manage.py runserver
```

---

## 🌐 Access Your Website

Once the server is running:

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:8000/ | **Website Home** |
| http://127.0.0.1:8000/admin/ | **Admin Panel** |

---

## 📝 Add Your First Project to Portfolio

1. Open http://127.0.0.1:8000/admin/
2. Login with your admin credentials
3. Click **"Projects"** under the **Main** app
4. Click **"ADD PROJECT"**
5. Fill in the details:
   - **Title**: Your Project Name
   - **Description**: Project details
   - **Tools Used**: Technologies (e.g., Python, Django, SQL)
   - **Image**: Upload project screenshot
6. Click **"SAVE"**

Your project will appear on the homepage and portfolio page!

---

## 🎨 Customize Your Site

### Change Website Title & Colors:

**1. Update Site Name:**
- Go to Admin Panel → Sites
- Change the site name to "DataZen Analytics"

**2. Change Colors:**
- Open: `datazen_website\main\static\css\style.css`
- Find color codes:
  - `#002d5c` = Dark Blue (Primary)
  - `#00bcd4` = Cyan (Accent)
- Replace with your brand colors

**3. Update Company Info:**
- Open: `datazen_website\main\templates\main\contact.html`
- Update address, phone, email
- Open: `datazen_website\main\templates\main\about.html`
- Update company description

---

## 📊 What's Included

### ✅ 7 Ready-to-Use Pages
- **Home**: Featured projects showcase
- **About**: Company information
- **Services**: Service listings with pricing
- **Portfolio**: Complete project gallery
- **Contact**: Contact form + information
- **Blog**: Blog post management
- **Admin**: Full content management

### ✅ Database Models
- **Projects**: Portfolio items
- **Services**: Service offerings
- **Blog Posts**: Blog articles
- **Contact Messages**: Lead storage

### ✅ Built-In Features
- Responsive design (mobile-friendly)
- Contact form with database storage
- Admin panel for content management
- Blog system
- Image uploads
- Professional CSS styling
- Form validation

---

## 🔐 Production Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `datazen_website\settings.py`
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up environment variables (.env file)
- [ ] Configure email settings for contact form
- [ ] Set up HTTPS/SSL certificate
- [ ] Configure static file serving
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Configure backups

---

## 🚢 Deploy Your Website

### Option 1: Render.com (Free)
```bash
pip install gunicorn
# Create Procfile:
# web: gunicorn datazen_website.wsgi
```

### Option 2: PythonAnywhere (Free tier available)
- Upload project files
- Configure virtual environment
- Set WSGI configuration
- Add static files path

### Option 3: AWS Elastic Beanstalk
```bash
pip install awsebcli
eb init
eb create
eb deploy
```

---

## 🐛 Troubleshooting

### Issue: Port 8000 already in use
**Solution:**
```bash
python datazen_website\manage.py runserver 8080
```
Then visit http://127.0.0.1:8080/

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Static files not loading
**Solution:**
```bash
python datazen_website\manage.py collectstatic --noinput
```

### Issue: Database is locked
**Solution:**
```bash
# Delete old database and migrations
rm db.sqlite3
python datazen_website\manage.py migrate
```

---

## 📚 File Structure Reference

```
datazen_website/
│
├── 📄 manage.py              # Django control script
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md              # Full documentation
├── 📄 setup.bat / setup.sh   # Setup script
├── 📄 run.bat / run.sh       # Quick run script
│
├── 📁 datazen_website/       # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL routing
│   └── wsgi.py               # WSGI app
│
├── 📁 main/                  # Main app
│   ├── models.py             # Database models
│   ├── views.py              # Page logic
│   ├── admin.py              # Admin configuration
│   ├── urls.py               # App URLs
│   ├── 📁 templates/         # HTML files
│   │   └── main/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── about.html
│   │       ├── services.html
│   │       ├── portfolio.html
│   │       ├── contact.html
│   │       └── blog.html
│   └── 📁 static/            # CSS, JS, images
│       ├── css/style.css
│       ├── js/script.js
│       └── images/
│
└── 📁 media/                 # Uploaded files
    └── projects/
```

---

## 🎓 Next Steps

### Beginner
1. ✅ Get the website running
2. ✅ Add 3-5 sample projects
3. ✅ Update about and contact pages
4. ✅ Customize colors

### Intermediate
1. Add blog posts
2. Set up email notifications
3. Add more services
4. Create FAQ page

### Advanced
1. User authentication
2. Advanced analytics
3. Payment integration
4. API for mobile app

---

## 💡 Tips & Tricks

**To add a new page:**
1. Create view in `views.py`
2. Add URL in `main/urls.py`
3. Create template in `main/templates/main/`
4. Add link in `base.html`

**To add a database model:**
1. Define in `models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`
4. Register in `admin.py`

**To collect static files:**
```bash
python manage.py collectstatic
```

---

## 📞 Support Resources

- **Django Docs**: https://docs.djangoproject.com/
- **Stack Overflow**: Tag with `django`
- **Django Community**: https://www.djangoproject.com/community/

---

## 🎉 Congratulations!

Your DataZen Analytics website is ready! 🚀

**Remember:** This is a starting point. Feel free to customize, extend, and make it your own!

---

**Last Updated**: April 2026  
**Django Version**: 4.2.0  
**Status**: Production Ready ✅
