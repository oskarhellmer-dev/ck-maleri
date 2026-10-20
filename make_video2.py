#!/usr/bin/env python3
"""Hero-video v2: ingen dimma/damm, samma Veo 3.1."""
import json, urllib.request, urllib.error, time

KEY = [l.split("=", 1)[1].strip().strip('"')
       for l in open("/home/clawd/.hermes/fal.env") if l.startswith("FAL_KEY")][0]
H = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}

def call(url, data=None, method="POST", timeout=300):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                               headers=H, method=method)
    try:
        return json.load(urllib.request.urlopen(r, timeout=timeout))
    except urllib.error.HTTPError as e:
        return {"__err": e.code, "__body": e.read()[:400].decode("utf-8", "ignore")}

STILL = ("Photograph inside an empty Nordic apartment, seen from low near the floor. A newly sanded "
         "herringbone oak parquet floor with a matte oiled finish, crisp visible wood grain and "
         "natural colour variation between the blocks. Late afternoon sun comes from a tall window "
         "and rakes low across the floor, long soft shadows following the herringbone pattern. "
         "Completely clear air: no haze, no dust, no fog, no smoke, no mist, no glowing light shafts. "
         "Sharp focus, full frame camera, 35 mm lens, f/5.6, natural muted colour, fine film grain. "
         "No people, no text, no watermark.")

MOVE = ("Slow, steady cinematic dolly forward low over the herringbone oak floor, gliding toward the "
        "tall window. The late afternoon light moves gently across the wood grain as the camera "
        "advances. The air is completely clear and clean at all times: no haze, no dust, no fog, no "
        "smoke, no mist, no light shafts, no bloom. Sharp, photorealistic, natural colour, smooth "
        "stabilised movement, shallow depth of field. No people, no text, no watermark.")

NEG = ("haze, fog, dust, smoke, mist, steam, bloom, glow, light shafts, cloudy air, text, watermark, "
       "people, hands, cartoon, distorted wood, warped lines, duplicated boards")

def main():
    print("källbild...", flush=True)
    r = call("https://fal.run/fal-ai/flux-pro/v1.1-ultra",
             {"prompt": STILL, "aspect_ratio": "16:9", "num_images": 1,
              "output_format": "jpeg", "safety_tolerance": "3"})
    if not r.get("images"):
        print("still-fel", str(r)[:300], flush=True); return
    url = r["images"][0]["url"]
    print("still:", url, flush=True)
    d = urllib.request.urlopen(url, timeout=300).read()
    open("/home/clawd/ck-maleri/assets/img/hero2.jpg", "wb").write(d)
    print("sparad", len(d), flush=True)

    print("video veo3.1...", flush=True)
    res = call("https://queue.fal.run/fal-ai/veo3.1/image-to-video",
               {"prompt": MOVE, "image_url": url, "aspect_ratio": "16:9", "duration": "8s",
                "resolution": "1080p", "generate_audio": False, "negative_prompt": NEG})
    if "__err" in res:
        print("submit-fel", res, flush=True); return
    rid = res["request_id"]
    st = res.get("status_url") or f"https://queue.fal.run/fal-ai/veo3.1/image-to-video/requests/{rid}/status"
    for i in range(90):
        time.sleep(6)
        s = call(st, method="GET")
        if "__err" in s:
            print("status-fel", s, flush=True); return
        if i % 5 == 4:
            print("  ", s.get("status"), flush=True)
        if s.get("status") == "COMPLETED":
            out = call(s.get("response_url") or
                       f"https://queue.fal.run/fal-ai/veo3.1/image-to-video/requests/{rid}", method="GET")
            v = (out.get("video") or {}).get("url")
            print("video:", v, flush=True)
            if v:
                data = urllib.request.urlopen(v, timeout=600).read()
                open("/home/clawd/ck-maleri/assets/veo-v2.mp4", "wb").write(data)
                print("SPARAD", len(data), flush=True)
            return
        if s.get("status") in ("FAILED", "ERROR"):
            print("misslyckades", json.dumps(s)[:300], flush=True); return
    print("timeout", flush=True)

main()
