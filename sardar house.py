import os
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sardar_house_exclusive_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

products = {}
ADMIN_PASSWORD = "admin123"

def get_layout(content_html, active_page):
    menu_items = [('home', 'হোম'), ('shop', 'শপ'), ('about', 'আমাদের সম্পর্কে'), ('contact', 'যোগাযোগ'), ('policy', 'রিটার্ন পলিসি')]
    nav_links = ""
    for route, label in menu_items:
        active_class = "active-link" if active_page == route else ""
        nav_links += f'<a href="{url_for(route)}" class="nav-link {active_class}">{label}</a>'

    auth_action = '<a href="/logout" class="btn btn-sm btn-outline-danger ms-2">Logout</a>' if 'is_admin' in session else '<a href="/login" class="btn btn-sm btn-outline-warning ms-2">Admin</a>'

    # .replace() ব্যবহার করা হয়েছে যেন ব্র্যাকেট নিয়ে সমস্যা না হয়
    template = """
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sardar House | Exclusive Shop</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #0a0a0a; background-image: radial-gradient(circle at 2px 2px, #1a1a1a 1px, transparent 0); background-size: 32px 32px; color: #D4AF37; font-family: 'Segoe UI', sans-serif; margin-top: 90px; }
            .navbar { background: rgba(0,0,0,0.95); border-bottom: 1px solid rgba(212,175,55,0.3); position: fixed; top: 0; width: 100%; z-index: 1000; padding: 15px 0; }
            .nav-link { color: #888 !important; margin: 0 12px; font-weight: 600; text-decoration: none; }
            .active-link, .nav-link:hover { color: #D4AF37 !important; }
            .card-premium { background: rgba(20,20,20,0.8); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 25px; backdrop-filter: blur(10px); }
            .whatsapp-btn { background: #25D366; color: white !important; border-radius: 10px; text-align: center; padding: 10px; display: block; text-decoration: none; font-weight: bold; }
            .form-control { background: #151515 !important; border: 1px solid #333 !important; color: white !important; }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="container d-flex justify-content-between align-items-center">
                <a href="/" style="text-decoration:none;"><h3 style="color:#D4AF37; margin:0; letter-spacing:2px;">SARDAR HOUSE</h3></a>
                <div class="nav-menu">NAV_LINKS AUTH_ACTION</div>
            </div>
        </nav>
        <div class="container py-4">MAIN_CONTENT</div>
    </body>
    </html>
    """
    return template.replace("NAV_LINKS", nav_links).replace("AUTH_ACTION", auth_action).replace("MAIN_CONTENT", content_html)

@app.route('/')
def home():
    content = '<div class="text-center py-5"><h1 class="display-3 fw-bold">SARDAR HOUSE</h1><p class="lead">প্রিমিয়াম কালেকশন - আভিজাত্যের অন্য নাম</p><a href="/shop" class="btn btn-warning btn-lg mt-3">শপ ভিজিট করুন</a></div>'
    return render_template_string(get_layout(content, 'home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('shop'))
        error = "ভুল পাসওয়ার্ড!"
    
    content = f'<div class="row justify-content-center py-5"><div class="col-md-4 card-premium text-center"><h3>Admin Access</h3><form method="POST"><input type="password" name="password" class="form-control mb-3" placeholder="পাসওয়ার্ড" required><button type="submit" class="btn btn-warning w-100">Login</button></form><p class="text-danger mt-3">{error}</p></div></div>'
    return render_template_string(get_layout(content, 'login'))

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

@app.route('/shop')
def shop():
    content = '<div class="row g-4">'
    if not products:
        content += '<div class="col-12 text-center p-5 card-premium"><h4>বর্তমানে কোনো পণ্য নেই।</h4></div>'
    else:
        for pid, p in products.items():
            img_url = url_for('static', filename=p['img'])
            wa_link = f"https://wa.me/8801877278210?text=আসসালামু আলাইকুম, আমি এই পণ্যটি নিতে চাই: {p['name']}"
            content += f'''<div class="col-md-4"><div class="card-premium h-100 shadow"><img src="{img_url}" class="w-100 rounded-3 mb-3" style="height:280px; object-fit:cover;"><h4>{p['name']}</h4><h5 class="text-white my-3">৳ {p['price']}</h5><a href="{wa_link}" target="_blank" class="whatsapp-btn">WhatsApp অর্ডার</a>{'<a href="/delete/'+pid+'" class="text-danger d-block mt-3 text-center small" onclick="return confirm(\'মুছে ফেলবেন?\')">পণ্যটি ডিলিট করুন</a>' if 'is_admin' in session else ''}</div></div>'''
    content += '</div>'
    
    if 'is_admin' in session:
        content += '<div class="card-premium mt-5 shadow-lg border-warning"><h3 class="mb-4 text-center">নতুন পণ্য যোগ করুন</h3><form action="/add" method="POST" enctype="multipart/form-data" class="row g-3"><div class="col-md-4"><input type="text" name="name" class="form-control" placeholder="নাম" required></div><div class="col-md-3"><input type="text" name="price" class="form-control" placeholder="দাম" required></div><div class="col-md-3"><input type="file" name="file" class="form-control" required></div><div class="col-md-2"><button type="submit" class="btn btn-warning w-100 fw-bold">আপলোড</button></div></form></div>'
    return render_template_string(get_layout(content, 'shop'))

@app.route('/add', methods=['POST'])
def add_product():
    if 'is_admin' in session:
        name, price, file = request.form.get('name'), request.form.get('price'), request.files.get('file')
        if name and price and file:
            filename = f"{name.replace(' ', '_')}.jpg"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            products[str(len(products)+1)] = {'name': name, 'price': price, 'img': filename}
    return redirect(url_for('shop'))

@app.route('/delete/<pid>')
def delete_product(pid):
    if 'is_admin' in session and pid in products:
        del products[pid]
    return redirect(url_for('shop'))

@app.route('/about')
def about(): return render_template_string(get_layout('<div class="card-premium py-5"><h2>আমাদের সম্পর্কে</h2><p>Sardar House একটি প্রিমিয়াম লাইফস্টাইল ব্র্যান্ড।</p></div>', 'about'))

@app.route('/contact')
def contact(): return render_template_string(get_layout('<div class="card-premium py-5"><h2>যোগাযোগ</h2><p>📍 ঢাকা, বাংলাদেশ<br>📞 01877278210</p></div>', 'contact'))

@app.route('/policy')
def policy(): return render_template_string(get_layout('<div class="card-premium py-5"><h2>রিটার্ন পলিসি</h2><p>১. ৩ দিনের মধ্যে এক্সচেঞ্জ সুবিধা।</p></div>', 'policy'))

if __name__ == '__main__':
    app.run(debug=True)
