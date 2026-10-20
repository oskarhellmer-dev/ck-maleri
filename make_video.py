#!/usr/bin/env python3
"""Gör en rejäl hero-video: bättre källbild + toppmodeller på fal.ai."""
import json, urllib.request, urllib.error, time, os, sys

KEY = [l.split("=", 1)[1].strip().strip('"')
       for l in open("/home/clawd/.hermes/fal.env") if l.startswith("FAL_KEY")][0]
H = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}

def call(url, data=None, method="POST", timeout=180):
    r = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                               headers=H, method=method)
    try:
        return json.load(urllib.request.urlopen(r, timeout=timeout))
    except urllib.error.HTTPError as e:
        return {"__err": e.code, "__body": e.read()[:400].decode("utf-8", "ignore")}

def sync(model, payload, timeout=600):
    return call(f"https://fal.run/{model}", payload, timeout=timeout)

def queue(model, payload, poll=90):
    r = call(f"https://queue.fal.run/{model}", payload)
    if "__err" in r:
        print("  submit-fel", model, r["__err"], r["__body"], flush=True); return None
    rid = r.get("request_id")
    st = r.get("status_url") or f"https://queue.fal.run/{model}/requests/{rid}/status"
    for i in range(poll):
        time.sleep(6)
        s = call(st, method="GET")
        if "__err" in s: print("  status-fel", s, flush=True); return None
        if i % 5 == 4: print("  ", model, s.get("status"), flush=True)
        if s.get("status") == "COMPLETED":
            res = call(s.get("response_url") or f"https://queue.fal.run/{model}/requests/{rid}", method="GET")
            return res
        if s.get("status") in ("FAILED", "ERROR"):
            print("  misslyckades", json.dumps(s)[:300], flush=True); return None
    print("  timeout", model, flush=True); return None

def download(url, path):
    d = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "hermes"}), timeout=600).read()
    open(path, "wb").write(d); return len(d)

STILL = ("Photograph inside an empty Nordic apartment. A newly sanded herringbone oak parquet floor "
         "with a matte oiled finish, visible wood grain and natural variation between the blocks. "
         "Late afternoon sun comes in from a tall window at the left and rakes low across the floor, "
         "long soft shadows in the block pattern, a faint haze of fine sanding dust in the light beam. "
         "Full frame camera, 35 mm lens, f/4, natural muted colour, subtle film grain, no people, "
         "no text, no watermark, not oversaturated.")

def make_still():
    for model, payload in [
        ("fal-ai/flux-pro/v1.1-ultra",
         {"prompt": STILL, "aspect_ratio": "16:9", "num_images": 1, "output_format": "jpeg",
          "safety_tolerance": "3", "raw": False}),
        ("fal-ai/flux-2", {"prompt": STILL, "image_size": {"width": 1344, "height": 768},
                           "num_images": 1, "output_format": "jpeg"}),
    ]:
        print("källbild via", model, flush=True)
        r = sync(model, payload, timeout=300)
        if r and r.get("images"):
            n = download(r["images"][0]["url"], "/home/clawd/ck-maleri/assets/img/hero-new.jpg")
            print("  klar", r["images"][0]["url"][:80], n, flush=True)
            return r["images"][0]["url"]
        print("  fel:", str(r)[:200], flush=True)
    return None

MOVE = ("Slow, steady cinematic dolly forward low over the herringbone oak floor, moving toward the "
        "tall window. The late afternoon light slowly sweeps across the wood grain as the camera glides; "
        "fine sanding dust drifts through the light beam. Smooth stabilised camera movement, shallow depth "
        "of field, natural colour, realistic. No people. No text.")

def make_videos(img_url):
    jobs = [
        ("veo311", "fal-ai/veo3.1/image-to-video",
         {"prompt": MOVE, "image_url": img_url, "aspect_ratio": "16:9", "duration": "8s",
          "resolution": "1080p", "generate_audio": False, "negative_prompt": "text, watermark, people, cartoon, distorted wood"}),
        ("kling25pro", "fal-ai/kling-video/v2.5-turbo/pro/image-to-video",
         {"prompt": MOVE, "image_url": img_url, "duration": "10", "aspect_ratio": "16:9",
          "negative_prompt": "text, watermark, people, blur, distortion"}),
        ("seedance", "fal-ai/bytedance/seedance/v1/pro/image-to-video",
         {"prompt": MOVE, "image_url": img_url, "aspect_ratio": "16:9", "resolution": "1080p",
          "duration": "5", "camera_fixed": False}),
    ]
    for name, model, payload in jobs:
        print("video:", name, model, flush=True)
        res = queue(model, payload)
        if not res:
            continue
        v = (res.get("video") or {}).get("url") or res.get("video_url")
        if not v:
            print("  inget videofält:", json.dumps(res)[:300], flush=True); continue
        try:
            n = download(v, f"/home/clawd/ck-maleri/assets/kandidat-{name}.mp4")
            print("  SPARAD", name, n, v[:90], flush=True)
        except Exception as e:
            print("  nedladdningsfel", repr(e)[:150], flush=True)

if __name__ == "__main__":
    url = make_still()
    print("still-url:", url, flush=True)
    if url:
        make_videos(url)
    print("KLART", flush=True)
