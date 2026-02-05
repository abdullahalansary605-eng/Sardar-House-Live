import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ডিরেক্টরি কনফিগারেশন
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ডাটাবেজ (মেমরিতে)
products = {}

# কমন স্টাইল এবং লেআউট (সব পেজের জন্য)
def get_layout(content, active_page):
    menu_items = [
        ('home', 'হোম'),
        ('shop', 'শপ'),
        ('about', 'আমাদের সম্পর্কে'),
        ('contact', 'যোগাযোগ'),
        ('policy', 'রিটার্ন পলিসি')
    ]
    
    nav_links = ""
    for route, label in menu_items:
        active_class = "active-link" if active_page == route else ""
        nav_links += f'<a href="{url_for(route)}" class="nav-link {active_class}">{label}</a>'

    return f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sardar House | Premium Clothing</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ 
                background-color: #0a0a0a;
                background-image: radial-gradient(circle at 2px 2px, #1a1a1a 1px, transparent 0);
                background-size: 32px 32px;
                color: #D4AF37; 
                font-family: 'Segoe UI', sans-serif;
                margin-top: 80px;
            }}
            .navbar {{
                background: rgba(0,0,0,0.95);
                border-bottom: 1px solid rgba(212,175,55,0.3);
                padding: 15px 0;
                position: fixed;
                top: 0;
                width: 100%;
                z-index: 1000;
            }}
            .nav-link {{
                color: #888 !important;
                margin: 0 15px;
                font-weight: 600;
                text-decoration: none;
                transition: 0.3s;
            }}
            .nav-link:hover, .active-link {{
                color: #D4AF37 !important;
                text-shadow: 0 0 10px rgba(212,175,55,0.5);
            }}
            .container {{ max-width: 1100px; }}
            .card-premium {{
                background: rgba(20,20,20,0.8);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
            }}
            .whatsapp-btn {{
                background: #25D366; color: white !important;
                padding: 10px 20px; border-radius: 10px;
                text-decoration: none; font-weight: bold; display: block; text-align: center;
            }}
            .price {{ font-size: 1.5rem; color: #fff; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="container d-flex justify-content-between align-items-center">
                <a href="/" style="text-decoration:none;"><h3 style="color:#D4AF37; margin:0; letter-spacing:2px;">SARDAR HOUSE</h3></a>
                <div class="nav-menu">
                    {nav_links}
                </div>
            </div>
        </nav>
        <div class="container py-5">
            {content}
        </div>
    </body>
    </html>
    """

@app.route('/')
def home():
    content = """
    <div class="text-center py-5">
        <h1 class="display-2 fw-bold">WELCOME TO SARDAR HOUSE</h1>
        <p class="lead text-secondary">আপনার আভিজাত্যের প্রতীক - প্রিমিয়াম পাঞ্জাবি কালেকশন</p>
        <a href="/shop" class="btn btn-outline-warning btn-lg mt-4">শপ ভিজিট করুন</a>
    </div>
    """
    return render_template_string(get_layout(content, 'home'))

@app.route('/shop')
def shop():
    if not products:
        content = '<div class="card-premium text-center"><h3>বর্তমানে কোনো পণ্য নেই। নিচে থেকে যোগ করুন।</h3></div>'
    else:
        content = '<div class="row g-4">'
        for pid, p in products.items():
            img_url = url_for('static', filename=p['img'])
            wa_link = f"https://wa.me/8801877278210?text=আসসালামু আলাইকুম, আমি এই পাঞ্জাবিটি কিনতে চাই: {p['name']}"
            content += f'''
            <div class="col-md-4">
                <div class="card-premium h-100">
                    <img src="{img_url}" class="w-100 rounded-3 mb-3" style="height:300px; object-fit:cover;">
                    <h4>{p['name']}</h4>
                    <div class="price">{p['price']}</div>
                    <a href="{wa_link}" target="_blank" class="whatsapp-btn">WhatsApp অর্ডার</a>
                </div>
            </div>'''
        content += '</div>'
    
    # অ্যাডমিন প্যানেল শপ পেজের নিচেই রাখা হলো আপনার সুবিধার জন্য
    content += """
    <div class="card-premium mt-5">
        <h3 class="mb-4">নতুন পণ্য যোগ করুন (ম্যানেজমেন্ট)</h3>
        <form action="/add" method="POST" enctype="multipart/form-data" class="row g-3">
            <div class="col-md-4"><input type="text" name="name" class="form-control bg-dark text-white" placeholder="নাম" required></div>
            <div class="col-md-3"><input type="text" name="price" class="form-control bg-dark text-white" placeholder="দাম" required></div>
            <div class="col-md-3"><input type="file" name="file" class="form-control bg-dark text-white" required></div>
            <div class="col-md-2"><button type="submit" class="btn btn-warning w-100 fw-bold">আপলোড</button></div>
        </form>
    </div>
    """
    return render_template_string(get_layout(content, 'shop'))

@app.route('/about')
def about():
    content = """
    <div class="card-premium">
        <h2>আমাদের সম্পর্কে</h2>
        <p class="text-secondary">Sardar House একটি প্রিমিয়াম পাঞ্জাবি ব্র্যান্ড। আমরা গুণগত মান এবং আধুনিক ডিজাইনের সমন্বয়ে সেরা পোশাক নিশ্চিত করি।</p>
    </div>
    """
    return render_template_string(get_layout(content, 'about'))

@app.route('/contact')
def contact():
    content = """
    <div class="card-premium">
        <h2>যোগাযোগ</h2>
        <p>ঠিকানা: ঢাকা, বাংলাদেশ</p>
        <p>ফোন: 01877278210</p>
        <p>হোয়াটসঅ্যাপ: সরাসরি মেসেজ দিন</p>
    </div>
    """
    return render_template_string(get_layout
