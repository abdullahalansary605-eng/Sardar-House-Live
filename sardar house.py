import urllib.request, csv, io, os
from flask import Flask, render_template_string, session, url_for, request, redirect

app = Flask(__name__)
app.secret_key = "sardar_house_exclusive_key"

# আপনার গুগল শিট ডাটাবেজ লিঙ্ক
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQUw7rSYMFBFTyun0JDkeUgwQb51YiGS_anOVzYZQR9hrUxS4UdFUf5hCbQrl4UJhvn9ExsrZglMSWT/pub?output=csv"

# আপনার দেওয়া নতুন পাসওয়ার্ড
ADMIN_PASSWORD = "1212716274"

def get_db_products():
    try:
        response = urllib.request.urlopen(SHEET_CSV_URL)
        dat = response.read().decode('utf-8')
        f = io.StringIO(dat)
        reader = csv.DictReader(f)
        return {row['Id']: {'name': row['Name'], 'price': row['Price'], 'img': row['Image Url']} for row in reader}
    except Exception as e:
        print(f"Database Error: {e}")
        return {}

def get_layout(content_html, active_page):
    menu_items = [('home', 'হোম'), ('shop', 'শপ'), ('about', 'আমাদের সম্পর্কে'), ('contact', 'যোগাযোগ'), ('policy', 'রিটার্ন পলিসি')]
    nav_links = "".join([f'<a href="{url_for(r)}" class="nav-link {"active-link" if active_page==r else ""}">{l}</a>' for r, l in menu_items])
    
    auth_action = '<a href="/logout" class="btn btn-sm btn-outline-danger ms-lg-2">Logout</a>' if 'is_admin' in session else '<a href="/login" class="btn btn-sm btn-outline-warning ms-lg-2">Admin</a>'

    template = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sardar House | Premium Shop</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #0a0a0a; color: #D4AF37; font-family: 'Segoe UI', sans-serif; padding-top: 100px; }}
            .navbar {{ background: rgba(0,0,0,0.98); border-bottom: 1px solid rgba(212,175,55,0.3); }}
            .navbar-brand {{ color: #D4AF37 !important; font-weight: bold; letter-spacing: 2px; }}
            .nav-link {{ color: #888 !important; font-weight: 600; margin: 0 10px; transition: 0.3s; text-decoration: none; }}
            .active-link, .nav-link:hover {{ color: #D4AF37 !important; }}
            .card-premium {{ background: rgba(20,20,20,0.8); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 20px; height: 100%; }}
            .product-img {{ width: 100%; height: 280px; object-fit: cover; border-radius: 15px; }}
            .whatsapp-btn {{ background: #25D366; color: white !important; border-radius: 10px; text-align: center; padding: 12px; display: block; text-decoration: none; font-weight: bold; }}
            .form-control {{ background: #151515 !important; border: 1px solid #333 !important; color: white !important; }}
            @media (max-width: 768px) {{ body {{ padding-top: 80px; }} .navbar-collapse {{ background: #000; padding: 20px; border-radius: 10px; margin-top: 10px; }} }}
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg fixed-top">
            <div class="container">
                <a class="navbar-brand" href="/">SARDAR HOUSE</a>
                <button class="navbar-toggler border-warning" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon" style="filter: invert(1);"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <div class="navbar-nav ms-auto">{nav_links} {auth_action}</div>
                </div>
            </div>
        </nav>
        <div class="container">{content_html}</div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    return template

@app.route('/')
def home():
    content = '<div class="text-center py-5 mt-lg-5"><h1 class="display-3 fw-bold">SARDAR HOUSE</h1><p class="lead">প্রিমিয়াম কালেকশন - আভিজাত্যের অন্য নাম</p><a href="/shop" class="btn btn-warning btn-lg mt-3 px-5 fw-bold">শপ ভিজিট করুন</a></div>'
    return render_template_string(get_layout(content, 'home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('shop'))
        error = "ভুল পাসওয়ার্ড!"
    content = f'<div class="row justify-content-center"><div class="col-md-4 card-premium text-center"><h3>Admin Access</h3><form method="POST"><input type="password" name="password" class="form-control mb-3" placeholder="পাসওয়ার্ড" required><button type="submit" class="btn btn-warning w-100 fw-bold">Login</button></form><p class="text-danger mt-3">{error}</p></div></div>'
    return render_template_string(get_layout(content, 'login'))

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

@app.route('/shop')
def shop():
    products = get_db_products()
    content = '<div class="row g
