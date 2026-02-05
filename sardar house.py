from flask import Flask, render_template_string, request, redirect, url_for
import os

app = Flask(__name__)

# পণ্যের তালিকা (সাময়িকভাবে মেমরিতে থাকবে)
products = []

# প্রফেশনাল এইচটিএমএল ডিজাইন (আপনার নম্বর সহ)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sardar House - Premium Collection</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --gold: #dfbd69;
            --dark-bg: #0d0d0d;
            --glass: rgba(255, 255, 255, 0.05);
        }

        body {
            background: radial-gradient(circle at center, #1a1a1a 0%, #050505 100%);
            color: #ffffff;
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        .header {
            text-align: center;
            padding: 50px 0;
        }

        .header h1 {
            font-size: 3rem;
            color: var(--gold);
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 5px;
            text-shadow: 2px 2px 10px rgba(223, 189, 105, 0.3);
        }

        .header p {
            color: #888;
            letter-spacing: 2px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .admin-panel {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(223, 189, 105, 0.2);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 50px;
        }

        input, button {
            padding: 12px;
            margin: 5px;
            border-radius: 8px;
            border: 1px solid #333;
            background: #111;
            color: white;
            width: calc(100% - 30px);
        }

        button {
            background: var(--gold) !important;
            color: #000 !important;
            font-weight: bold;
            cursor: pointer;
            border: none;
            transition: 0.3s;
            width: auto;
            padding: 12px 30px;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(223, 189, 105, 0.4);
        }

        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
        }

        .product-card {
            background: var(--glass);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 20px;
            text-align: center;
            transition: 0.4s;
        }

        .product-card:hover {
            border-color: var(--gold);
            transform: scale(1.02);
        }

        .product-card img {
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 15px;
        }

        .price {
            color: var(--gold);
            font-size: 1.5rem;
            font-weight: bold;
            margin: 10px 0;
        }

        .whatsapp-btn {
            display: inline-block;
            background: #25D366;
            color: white;
            padding: 12px 20px;
            text-decoration: none;
            border-radius: 10px;
            font-weight: bold;
            margin-top: 10px;
            transition: 0.3s;
        }
        
        .whatsapp-btn:hover {
            background: #1eb954;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>Sardar House</h1>
    <p>PREMIUM MENSWEAR COLLECTIONS</p>
</div>

<div class="container">
    <div class="admin-panel">
        <h3 style="color: var(--gold);">নতুন পণ্য যোগ করুন (ম্যানেজমেন্ট)</h3>
        <form action="/add" method="post">
            <input type="text" name="name" placeholder="পাঞ্জাবির নাম (উদা: রাজকীয় সিল্ক)" required>
            <input type="text" name="price" placeholder="দাম (উদা: ১৮০০৳)" required>
            <input type="text" name="img_url" placeholder="ছবির লিঙ্ক (URL)" required>
            <button type="submit">যোগ করুন</button>
        </form>
    </div>

    <div class="product-grid">
        {% for product in products %}
        <div class="product-card">
            <img src="{{ product.img_url }}" alt="Punjabi">
            <h3>{{ product.name }}</h3>
            <div class="price">{{ product.price }}</div>
            <a href="https://wa.me/8801877278210?text=আসসালামু আলাইকুম, আমি এই পাঞ্জাবিটি কিনতে চাই: {{ product.name }} (দাম: {{ product.price }})" class="whatsapp-btn" target="_blank">WhatsApp অর্ডার</a>
        </div>
        {% endfor %}
    </div>

    {% if not products %}
    <p style="text-align: center; color: #666; margin-top: 50px;">বর্তমানে কোনো পণ্য স্টকে নেই। উপর থেকে যোগ করুন।</p>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, products=products)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    img_url = request.form.get('img_url')
    if name and price and img_url:
        products.append({'name': name, 'price': price, 'img_url': img_url})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
