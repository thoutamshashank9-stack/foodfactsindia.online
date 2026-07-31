import urllib.request

def test_vercel_live():
    url = "https://foodfactsindia-online.vercel.app/api/img/4901488010320"
    print(f"Testing Live Vercel Image Proxy URL: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            print(f"Status: {resp.status}")
            print(f"Final URL: {resp.url}")
            print(f"Content-Type: {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"Error fetching live Vercel URL: {e}")

if __name__ == '__main__':
    test_vercel_live()
