import requests
from flask import Flask, render_template_string, session, url_for, request, redirect
import io

app = Flask(__name__)
app.secret_key = "sardar_house_airtable_final_v1"

# --- আপনার এয়ারটেবল কনফিগারেশন ---
# আপনার দেওয়া টোকেনটি এখানে স্ট্রিং হিসেবে বসানো হয়েছে
AIRTABLE_TOKEN = "pat84ZiUqxXwgYvSq.0d42c21d500190d30683294d301d98ae5733370aaa91917aaef840495df95fae"
BASE_ID = "appNA47UFkggOEi6G"
TABLE_NAME = "Table 1" 
# ----------------------------------

ADMIN_PASSWORD = "1212716274"

def get_airtable_products():
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            records = response.json().get('records', [])
            # ডাটাবেজ থেকে কলামের নাম অনুযায়ী ডাটা আনা
            return [r['fields'] for r in records]
        else:
            print(f"Airtable Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Connection Error: {e}")
        return []

def get_layout(content_html, active_page):
    nav_links = [('/', 'হোম', 'h'), ('/shop', 'শপ', 's')]
    nav_html = "".join([f'<a href="{u}" style="color:{"#D4AF37" if active_page==p else "#888"}; margin:0 15px; text-decoration:none; font-weight:bold;">{l}</a>' for u, l, p in nav_links])
    auth = '<a href="/logout" style="color:#ff4444; margin-left:15px; text-decoration:none; font-size: 0.9rem;">Logout</a>' if 'is_admin' in session else '<a href="/login" style="color:#D4AF37; margin-left:15px; text-decoration:none; font-size: 0.9rem;">Admin</a>'

    return f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sardar House | Premium Shop</title>
        <style>
            body {{ background-color: #0a0a0a; color: #D4AF37; font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding-top: 100px; text-align: center; }}
            .navbar {{ background: rgba(0,0,0,0.95); padding: 20px; position: fixed; top: 0; width: 100%; border-bottom: 1px solid #333; z-index: 1000; box-sizing: border-box; }}
            .card {{ background: #111; border: 1px solid #222; border-radius: 15px; padding: 15px; margin: 15px; display: inline-block; width: 280px; transition: 0.3s; vertical-align: top; text-align: left; }}
            .card:hover {{ border-color: #D4AF37; transform: translateY(-5px); }}
            .product-img {{ width: 100%; height: 250px; object-fit: cover; border-radius: 10px; background: #1a1a1a; }}
            .price {{ color: #fff; font-size: 1.3rem; margin: 10px 0; font-weight: bold; }}
            .wa-btn {{ background: #25D366; color: white; padding: 12px; display: block; text-decoration: none; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 10px; }}
            .wa-btn:hover {{ background: #1ebe57; }}
            h3 {{ margin: 10px 0; font-size: 1.1rem; min-height: 50px; color: #D4AF37; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <span style="font-size: 1.5rem; font-weight: bold; letter-spacing: 2px;">SARDAR HOUSE</span><br><br>
            {nav_html} {auth}
        </div>
        <div style="padding: 20px;">{content_html}</div>
    </body>
    </html>
    """

@app.route('/')
def home():
    content = """
    <div style="margin-top: 50px;">
        <h1 style="font-size: 3rem; margin-bottom: 10px;">SARDAR HOUSE</h1>
        <p style="font-size: 1.2rem; color: #888;">আভিজাত্য ও আধুনিকতার এক অনন্য সমন্বয়</p>
        <br>
        <a href="/shop" style="background: #D4AF37; color: #000; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem; display: inline-block;">কালেকশন দেখুন</a>
    </div>
    """
    return render_template_string(get_layout(content, 'h'))

@app.route('/shop')
def shop():
    products = get_airtable_products()
    if not products:
        return render_template_string(get_layout('<div style="padding: 50px;"><h2>বর্তমানে কোনো পণ্য নেই।</h2><p>অনুগ্রহ করে এয়ারটেবল ডাটাবেজে পণ্য যোগ করুন।</p></div>', 's'))
    
    html = '<div style="display: flex; flex-wrap: wrap; justify-content: center; max-width: 1200px; margin: 0 auto;">'
    for p in products:
        # এয়ারটেবল কলামের নাম: 'Name', 'Price', 'Image_URL'
        name = p.get('Name', 'Premium Product')
        price = p.get('Price', 'TBA')
        img = p.get('Image_URL', 'https://via.placeholder.com/250?text=Sardar+House')
        
        wa_link = f"https://wa.me/8801877278210?text=আসসালামু আলাইকুম, আমি এই পণ্যটি নিতে চাই: {name}"
        
        html += f"""
        <div class="card">
            <img src="{img}" class="product-img" onerror="this.src='https://via.placeholder.com/250?text=Image+Loading...'">
            <h3>{name}</h3>
            <div class="price">৳ {price}</div>
            <a href="{wa_link}" target="_blank" class="wa-btn">WhatsApp অর্ডার</a>
        </div>
        """
    html += '</div>'
    return render_template_string(get_layout(html, 's'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('pass') == ADMIN_PASSWORD:
            session['is_admin'] = True
            return redirect(url_for('shop'))
    return render_template_string(get_layout('<div style="margin-top: 50px;"><h3>Admin Login</h3><form method="POST"><input type="password" name="pass" placeholder="Password" style="padding: 12px; border-radius: 5px; border: 1px solid #333; background: #111; color: #fff; width: 250px;"><br><br><button type="submit" style="background: #D4AF37; padding: 10px 30px; border: none; border-radius: 5px; font-weight: bold; cursor: pointer;">Login</button></form></div>', ''))

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
