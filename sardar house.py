import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ডিরেক্টরি পাথ সেট করা
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# static ফোল্ডার না থাকলে তৈরি করা
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ডাটাবেজ একদম খালি রাখা হয়েছে (আপনার ইনস্ট্রাকশন অনুযায়ী)
products = {}

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sardar House | Exclusive Shop</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #050505; color: #D4AF37; font-family: 'Segoe UI', sans-serif; }
        .nav-header { padding: 40px; border-bottom: 2px solid #D4AF37; background: #000; text-align: center; }
        .product-card { background: #111; border: 1px solid #222; border-radius: 15px; padding: 20px; text-align: center; transition: 0.3s; }
        .product-card:hover { border-color: #D4AF37; }
        .prod-img { width: 100%; height: 280px; object-fit: contain; background: #fff; border-radius: 12px; }
        .admin-section { background: #111; border: 2px dashed #444; padding: 30px; border-radius: 20px; margin-top: 60px; }
        .delete-btn { color: #ff4444; text-decoration: none; font-size: 14px; margin-top: 10px; display: inline-block; }
        .empty-msg { padding: 50px; color: #777; border: 1px dashed #333; border-radius: 15px; }
    </style>
</head>
<body>
    <div class="nav-header">
        <h1 class="display-4 fw-bold">SARDAR HOUSE</h1>
        <p class="text-secondary text-uppercase" style="letter-spacing: 3px;">Premium Collections</p>
    </div>
    
    <div class="container py-5">
        {{ content|safe }}
        
        <div class="admin-section shadow-lg">
            <h3 class="text-center mb-4">নতুন পণ্য যোগ করুন (ম্যানেজমেন্ট)</h3>
            <form action="/add" method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="col-md-4">
                    <input type="text" name="name" class="form-control bg-dark text-white border-secondary" placeholder="পণ্যের নাম (যেমন: কাটারি পাঞ্জাবি)" required>
                </div>
                <div class="col-md-3">
                    <input type="text" name="price" class="form-control bg-dark text-white border-secondary" placeholder="দাম (টাকায়)" required>
                </div>
                <div class="col-md-3">
                    <input type="file" name="file" class="form-control bg-dark text-white border-secondary" required>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-warning w-100 fw-bold">যোগ করুন</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    if not products:
        content = '<div class="empty-msg text-center"><h3>বর্তমানে কোনো পণ্য স্টকে নেই।</h3><p>নিচের ফরম ব্যবহার করে আপনার প্রথম পণ্যটি যোগ করুন।</p></div>'
    else:
        content = '<div class="row g-4">'
        for pid, p in products.items():
            img_url = url_for('static', filename=p['img'])
            content += f'''
            <div class="col-md-4 col-6">
                <div class="product-card shadow">
                    <img src="{img_url}" class="prod-img">
                    <h4 class="mt-3 fw-bold">{p['name']}</h4>
                    <h5 class="text-white mb-2">৳ {p['price']}</h5>
                    <a href="/delete/{pid}" class="delete-btn" onclick="return confirm('পণ্যটি কি মুছে ফেলবেন?')">মুছে ফেলুন</a>
                </div>
            </div>'''
        content += '</div>'
    return render_template_string(HTML_LAYOUT, content=content)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    file = request.files.get('file')
    if name and price and file:
        filename = f"{name.replace(' ', '_')}.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_id = str(len(products) + 1)
        while new_id in products:
            new_id = str(int(new_id) + 1)
        products[new_id] = {'name': name, 'price': price, 'img': filename}
    return redirect('/')

@app.route('/delete/<pid>')
def delete_product(pid):
    if pid in products:
        del products[pid]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
