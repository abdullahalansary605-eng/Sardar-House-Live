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

# ডাটাবেজ
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
        body { 
            /* প্রফেশনাল ডার্ক টেক্সচার ব্যাকগ্রাউন্ড */
            background-color: #0a0a0a;
            background-image: 
                radial-gradient(circle at 2px 2px, #1a1a1a 1px, transparent 0);
            background-size: 32px 32px;
            background-attachment: fixed;
            color: #D4AF37; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        }
        
        .nav-header { 
            padding: 60px 20px; 
            background: linear-gradient(to bottom, #000000, rgba(10,10,10,0.8));
            border-bottom: 1px solid rgba(212, 175, 55, 0.3); 
            text-align: center; 
        }

        .nav-header h1 {
            font-weight: 800;
            letter-spacing: 8px;
            text-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        }

        .product-card { 
            background: rgba(20, 20, 20, 0.8); 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.05); 
            border-radius: 20px; 
            padding: 20px; 
            text-align: center; 
            transition: all 0.4s ease;
        }

        .product-card:hover { 
            border-color: #D4AF37; 
            transform: translateY(-10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .prod-img { 
            width: 100%; 
            height: 300px; 
            object-fit: cover; 
            border-radius: 15px; 
            border: 1px solid #222;
        }

        .admin-section { 
            background: rgba(17, 17, 17, 0.9); 
            border: 1px solid rgba(212, 175, 55, 0.2); 
            padding: 40px; 
            border-radius: 25px; 
            margin-top: 80px; 
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        }

        .form-control {
            background: #151515 !important;
            border: 1px solid #333 !important;
            color: white !important;
            padding: 12px;
        }

        .form-control:focus {
            border-color: #D4AF37 !important;
            box-shadow: none !important;
        }

        .delete-btn { color: #ff4444; text-decoration: none; font-size: 14px; margin-top: 15px; display: inline-block; opacity: 0.7; }
        .delete-btn:hover { opacity: 1; color: #ff0000; }
        
        .empty-msg { 
            padding: 80px; 
            background: rgba(255,255,255,0.02); 
            border: 1px dashed #333; 
            border-radius: 20px; 
        }
    </style>
</head>
<body>
    <div class="nav-header">
        <h1 class="display-3">SARDAR HOUSE</h1>
        <p class="text-secondary text-uppercase" style="letter-spacing: 5px;">Define Your Royalty</p>
    </div>
    
    <div class="container py-5">
        {{ content|safe }}
        
        <div class="admin-section">
            <h3 class="text-center mb-4" style="color: #D4AF37;">ম্যানেজমেন্ট প্যানেল</h3>
            <form action="/add" method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="col-md-4">
                    <input type="text" name="name" class="form-control" placeholder="পাঞ্জাবির নাম" required>
                </div>
                <div class="col-md-3">
                    <input type="text" name="price" class="form-control" placeholder="দাম (যেমন: ১৮০০৳)" required>
                </div>
                <div class="col-md-3">
                    <input type="file" name="file" class="form-control" required>
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-warning w-100 fw-bold py-2">আপলোড করুন</button>
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
        content = '<div class="empty-msg text-center"><h3>বর্তমানে কোনো পণ্য স্টকে নেই।</h3><p class="text-muted">দয়া করে নিচের প্যানেল থেকে নতুন পণ্য যোগ করুন।</p></div>'
    else:
        content = '<div class="row g-4">'
        for pid, p in products.items():
            img_url = url_for('static', filename=p['img'])
            content += f'''
            <div class="col-md-4 col-6">
                <div class="product-card shadow">
                    <img src="{img_url}" class="prod-img">
                    <h4 class="mt-3 fw-bold">{p['name']}</h4>
                    <h5 class="text-white mb-2">{p['price']}</h5>
                    <a href="/delete/{pid}" class="delete-btn" onclick="return confirm('মুছে ফেলবেন?')">মুছে ফেলুন</a>
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
