import urllib.request
import re

urls = [
    ("Red Bull option 1", "https://images.unsplash.com/photo-1578849278619-e73505e9610f?w=600&auto=format&fit=crop&q=80"),
    ("Red Bull option 2", "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=600&auto=format&fit=crop&q=80"),
    ("Red Bull option 3", "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=600&auto=format&fit=crop&q=80"),
    ("Monster option", "https://images.unsplash.com/photo-1622543925917-763c34d1a86e?w=600&auto=format&fit=crop&q=80"),
    ("Coca-Cola option", "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&auto=format&fit=crop&q=80")
]

for name, u in urls:
    req = urllib.request.Request(u.replace("?w=600&auto=format&fit=crop&q=80", ""), headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"{name}: HTTP {resp.status}")
    except Exception as e:
        print(f"{name}: error {e}")
