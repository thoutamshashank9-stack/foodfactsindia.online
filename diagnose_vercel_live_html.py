import urllib.request

def test_urls():
    print("=== LIVE VERCEL DIAGNOSTICS ===")

    urls_to_test = [
        ("Vercel Proxy Amul Butter", "https://foodfactsindia-online.vercel.app/api/img/4901488010320"),
        ("Vercel Proxy Marie Gold", "https://foodfactsindia-online.vercel.app/api/img/8901063162426"),
        ("Vercel Proxy Good Day", "https://foodfactsindia-online.vercel.app/api/img/8901063092853"),
        ("Direct OFF CDN Amul Butter", "https://images.openfoodfacts.org/images/products/490/148/801/0320/front_en.3.400.jpg")
    ]

    for label, url in urls_to_test:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                print(f"[{label}] Status: {resp.status} | Content-Type: {resp.headers.get('Content-Type')} | Final URL: {resp.url}")
        except urllib.error.HTTPError as e:
            print(f"[{label}] HTTPError: {e.code} {e.reason}")
        except Exception as e:
            print(f"[{label}] Error: {e}")

if __name__ == '__main__':
    test_urls()
