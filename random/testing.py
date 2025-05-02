import requests

SIGNIN_APPLE_URL = "https://api.hevyapp.com/sign_in_with_apple_web"
APPLE_IDENTITY_TOKEN  = "eyJraWQiOiJyczBNM2tPVjlwIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLmhldnlhcHAud2ViIiwiZXhwIjoxNzQ2MjM1Mzg0LCJpYXQiOjE3NDYxNDg5ODQsInN1YiI6IjAwMTkwNi4zOGM2MDNmYmUxMzA0ZmVmYWFiN2EzNTlkZWQ4MGU4OC4wMTIyIiwiY19oYXNoIjoiOUo2S2pTOXJ5UEpGN1pIREdkOFA3USIsImVtYWlsIjoiOGdteDZqeWZxMkBwcml2YXRlcmVsYXkuYXBwbGVpZC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNfcHJpdmF0ZV9lbWFpbCI6dHJ1ZSwiYXV0aF90aW1lIjoxNzQ2MTQ4OTg0LCJub25jZV9zdXBwb3J0ZWQiOnRydWV9.NQhB-YzcGXK5nKvZ2xdGFLdfuToozrKPz6dGbNtAbN_uF8VpSHc16WASxFwqs1-5uDj0EyRULm7f9zsAm0TMS4DyszddgGC7l2sfC0ixIcqO5ryJKK94eFOp5LE52UsTA4eegl0z9nDyY5SepZtRbM_qHhTeAMzQ7-qzsOS_bBe-P-i2we4gFEntYHwcfxL7TNTLLNEPdItgFRWl7MsMrHNWhviD-TrGoEl9LC4JpLVGBbvq164nwu_Pnf-JVRqD8sRd4NSRvsNi5xzHqM5roY6ad1c37DNOSlemVWdpJ6uqF0f3hKIoMcrkX9GtJE9WWj_BPqwBB0jmzA2xZxX3AQ"
def get_auth_token_via_apple_web():
    """
    POST to the Apple web sign-in endpoint and return the auth_token.
    """
    payload = {
        "identityToken": APPLE_IDENTITY_TOKEN
    }
    headers = {
        "x-api-key":      "shelobs_hevy_web",
        "Accept":         "application/json",
        "Hevy-Platform":  "web",
    }
    resp = requests.post(SIGNIN_APPLE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("auth_token")
    if not token:
        raise RuntimeError(f"Could not find auth_token in response: {data}")
    return token

print(get_auth_token_via_apple_web())