# DataZen Analytics - Django Website

A modern, fully-featured Django website for DataZen Analytics with dynamic content management, admin panel, and contact forms.

## Features

✅ **Dynamic Pages**: Home, About, Services, Portfolio, Contact, Blog  
✅ **Admin Panel**: Manage projects, services, blog posts, and contact submissions  
✅ **Contact Form**: Store visitor inquiries in the database  
✅ **Responsive Design**: Mobile-friendly UI with modern CSS  
✅ **Blog System**: Create and manage blog posts  
✅ **Service Management**: Showcase your services with pricing  
✅ **Portfolio**: Display your projects with images and descriptions  

## Project Structure

```
datazen_website/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                         # Database (created after migration)
├── datazen_website/                   # Project settings
│   ├── __init__.py
│   ├── settings.py                    # Django configuration
│   ├── urls.py                        # Main URL routing
│   └── wsgi.py                        # WSGI application
├── main/                              # Main application
│   ├── models.py                      # Database models (Project, Contact, Service, BlogPost)
│   ├── views.py                       # View logic
│   ├── urls.py                        # App URL routing
│   ├── admin.py                       # Admin panel configuration
│   ├── apps.py                        # App configuration
│   ├── templates/main/                # HTML templates
│   │   ├── base.html                  # Base template
│   │   ├── home.html                  # Home page
│   │   ├── about.html                 # About page
│   │   ├── services.html              # Services page
│   │   ├── portfolio.html             # Portfolio page
│   │   ├── contact.html               # Contact form
│   │   ├── blog.html                  # Blog listing
│   │   └── blog_detail.html           # Blog detail page
│   └── static/                        # Static files
│       ├── css/style.css              # Main stylesheet
│       ├── js/script.js               # JavaScript
│       └── images/                    # Image assets
└── media/                             # User-uploaded files
    └── projects/                      # Project images
```

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- pip (Python package installer)

### 2. Create Virtual Environment

```bash
# Navigate to project directory
cd datazen_website

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

```bash
# Run migrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 6. Run Development Server

```bash
python manage.py runserver
```

The website will be available at: `http://127.0.0.1:8000/`

## Access the Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. Add Projects, Services, Blog Posts, etc.

## Database Models

### Project
- `title` - Project name
- `description` - Project details
- `tools_used` - Technologies used
- `image` - Project screenshot
- `created_at` - Creation date
- `updated_at` - Last updated date

### Contact
- `name` - Visitor name
- `email` - Contact email
- `message` - Inquiry message
- `created_at` - Submission date

### Service
- `title` - Service name
- `description` - Service details
- `icon` - Icon emoji

### BlogPost
- `title` - Post title
- `content` - Post content
- `author` - Author name
- `is_published` - Publication status
- `created_at` - Creation date
- `updated_at` - Last updated date

## Pages & Routes

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Homepage with featured projects |
| About | `/about/` | About company page |
| Services | `/services/` | Services listing with pricing |
| Portfolio | `/portfolio/` | All projects showcase |
| Contact | `/contact/` | Contact form & information |
| Blog | `/blog/` | Blog posts listing |
| Blog Detail | `/blog/<id>/` | Individual blog post |

## Customization

### Update Settings
Edit `datazen_website/settings.py`:
- Change `SECRET_KEY` for production
- Update `ALLOWED_HOSTS` for deployment
- Configure static/media file settings

### Add More Pages
1. Create a view in `main/views.py`
2. Add URL pattern in `main/urls.py`
3. Create template in `main/templates/main/`
4. Add navigation link in `base.html`

### Customize Styling
Edit `main/static/css/style.css` to match your brand colors and design.

## Deployment Options

### Render.com
```bash
pip install gunicorn
```

### PythonAnywhere
1. Upload your project
2. Add WSGI configuration
3. Set up static files

### AWS
1. Use AWS Elastic Beanstalk
2. Configure environment variables
3. Set up RDS for database

## Important Security Notes

⚠️ **Before Deployment:**
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False`
- Configure `ALLOWED_HOSTS` with your domain
- Use environment variables for sensitive data
- Set up proper static file serving

## Troubleshooting

**Port 8000 already in use:**
```bash
python manage.py runserver 8080
```

**Static files not loading:**
```bash
python manage.py collectstatic
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

## Additional Features (Advanced)

- User authentication & registration
- Email notifications
- Search functionality
- Comments on blog posts
- Social media integration
- SEO optimization
- Performance caching

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, create an issue in the repository or contact support.

---

**DataZen Analytics - Transform Data into Smart Decisions** 🚀
