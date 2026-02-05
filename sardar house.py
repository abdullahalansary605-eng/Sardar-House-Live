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
                margin-top: 100px;
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
            .card-premium {{
                background: rgba(20,20,20,0.8);
                border: 1px solid rgba(255,255,255,0.05);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
            }}
            .whatsapp-btn {{
                background: #25D366; color: white !important;
                padding: 10px 20px; border-radius: 10px;
                text-decoration: none; font-weight: bold; display: block; text-align: center;
                transition: 0.3s;
            }}
            .whatsapp-btn:hover {{ transform: scale(1.05); background: #1eb954; }}
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
        <h1 class="display-2 fw-bold" style="color:#D4AF37;">WELCOME TO SARDAR HOUSE</h1>
        <p class="lead text-secondary text-uppercase" style="letter-spacing:3px;">আপনার আভিজাত্যের প্রতীক - প্রিমিয়াম পাঞ্জাবি কালেকশন</p>
        <a href="/shop" class="btn btn-outline-warning btn-lg mt-4 px-5 py-3 fw-bold">শপ ভিজিট করুন</a>
    </div>
    """
    return render_template_string(get_layout(content, 'home'))

@app.route('/shop')
def shop():
    content = ""
    if not products:
        content += '<div class="card-premium text-center"><h3>বর্তমানে কোনো পণ্য নেই। নিচে থেকে যোগ করুন।</h3></div>'
    else:
        content += '<div class="row g-4">'
        for pid, p in products.items():
            img_url = url_for('static', filename=p['img'])
            wa_link = f"https://wa.me/8801877278210?text=আসসালামু আলাইকুম, আমি এই পাঞ্জাবিটি কিনতে চাই: {p['name']}"
            content += f'''
            <div class="col-md-4">
                <div class="card-premium h-100 shadow-lg">
                    <img src="{img_url}" class="w-100 rounded-3 mb-3" style="height:300px; object-fit:cover;">
                    <h4 class="fw-bold">{p['name']}</h4>
                    <h5 class="text-white my-3">৳ {p['price']}</h5>
                    <a href="{wa_link}" target="_blank" class="whatsapp-btn">WhatsApp অর্ডার</a>
                </div>
            </div>'''
        content += '</div>'
    
    content += """
    <div class="card-premium mt-5 shadow-lg">
        <h3 class="mb-4 text-center">নতুন পণ্য যোগ করুন (ম্যানেজমেন্ট)</h3>
        <form action="/add" method="POST" enctype="multipart/form-data" class="row g-3">
            <div class="col-md-4"><input type="text" name="name" class="form-control bg-dark text-white border-secondary" placeholder="পণ্যের নাম" required></div>
            <div class="col-md-3"><input type="text" name="price" class="form-control bg-dark text-white border-secondary" placeholder="দাম (যেমন: ১২০০)" required></div>
            <div class="col-md-3"><input type="file" name="file" class="form-control bg-dark text-white border-secondary" required></div>
            <div class="col-md-2"><button type="submit" class="btn btn-warning w-100 fw-bold">আপলোড</button></div>
        </form>
    </div>
    """
    return render_template_string(get_layout(content, 'shop'))

@app.route('/about')
def about():
    content = """
    <div class="card-premium shadow-lg">
        <h2 style="color:#D4AF37;">আমাদের সম্পর্কে</h2>
        <hr border-secondary>
        <p class="lead text-secondary">Sardar House একটি প্রিমিয়াম পাঞ্জাবি ব্র্যান্ড। আমরা গুণগত মান এবং আধুনিক ডিজাইনের সমন্বয়ে সেরা পোশাক নিশ্চিত করি। আমাদের প্রতিটি পাঞ্জাবি অত্যন্ত যত্ন সহকারে তৈরি করা হয় যেন তা আপনার ব্যক্তিত্বকে আরও আকর্ষণীয় করে তোলে।</p>
    </div>
    """
    return render_template_string(get_layout(content, 'about'))

@app.route('/contact')
def contact():
    content = """
    <div class="card-premium shadow-lg">
        <h2 style="color:#D4AF37;">যোগাযোগ</h2>
        <hr border-secondary>
        <p class="h5 mb-3">📍 ঠিকানা: ঢাকা, বাংলাদেশ</p>
        <p class="h5 mb-3">📞 ফোন: 01877278210</p>
        <p class="h5">💬 হোয়াটসঅ্যাপ: সরাসরি মেসেজ দিতে শপ পেজ ভিজিট করুন।</p>
    </div>
    """
    return render_template_string(get_layout(content, 'contact'))

@app.route('/policy')
def policy():
    content = """
    <div class="card-premium shadow-lg">
        <h2 style="color:#D4AF37;">রিটার্ন ও রিফান্ড পলিসি</h2>
        <hr border-secondary>
        <div class="text-secondary h5">
            <p>১. পাঞ্জাবির সাইজ না মিললে ৩ দিনের মধ্যে পরিবর্তনযোগ্য।</p>
            <p>২. কোনো ছেঁড়া বা ত্রুটি থাকলে সাথে সাথে রিটার্ন নেওয়া হবে।</p>
            <p>৩. রিফান্ডের ক্ষেত্রে ডেলিভারি চার্জ প্রযোজ্য হতে পারে।</p>
        </div>
    </div>
    """
    return render_template_string(get_layout(content, 'policy'))

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    file = request.files.get('file')
    if name and price and file:
        filename = f"{name.replace(' ', '_')}.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        products[str(len(products)+1)] = {'name': name, 'price': price, 'img': filename}
    return redirect(url_for('shop'))

if __name__ == '__main__':
    app.run(debug=True)
