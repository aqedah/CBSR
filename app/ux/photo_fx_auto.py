# 세로 휴대폰 화면에서 그림 속 인물이 잘리지 않게 초점(fx)을 얼굴 위치로 자동 계산 (2026-11-04 목사님: "스토리 사진에서 인물이 잘려서 보여요")
# 얼굴 찾기: OpenCV YuNet. 사람이 나오는 그림(scene·setting)에서 가장 큰 얼굴이 지금 초점으로 잘릴 때만, 다 보이도록 가장 조금 옮깁니다. 결과는 ux/photo_fx.json(빌드가 적용).
# 쓰는 법: python3 ux/photo_fx_auto.py <yunet.onnx 경로>
import json, os, sys, cv2
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = 0.465          # 휴대폰 세로 화면의 가로/세로 비(400×860)
ZOOM = 1.16        # 스토리 그림의 최대 확대(SKB)

def best_fx(W, H, faces, p0=0.5):
    """가장 큰 얼굴(주인공)이 지금 초점에서 잘리거나 밖에 있을 때만, 그 얼굴이 다 들어오도록 가장 조금 옮긴 값"""
    vw = min(W, H * A / ZOOM)
    if vw >= W or not faces: return None
    x, y, w, h, c = max(faces, key=lambda f: f[2] * f[3])
    m = w * 0.35; a, b = x - m, x + w + m
    inside = lambda p: (W - vw) * p <= a and (W - vw) * p + vw >= b
    if inside(p0): return None
    ok = [i / 100 for i in range(101) if inside(i / 100)]
    if not ok: return None
    return round(min(ok, key=lambda p: abs(p - p0)) * 100)

def main(model):
    P = json.load(open(f'{R}/ux/photos.json'))
    det = None; out = {}; rep = []
    for ph in P:
        f = f"{R}/site/{ph['u'].split('?')[0]}"
        if not os.path.exists(f): continue
        im = cv2.imread(f)
        if im is None: continue
        H, W = im.shape[:2]
        if det is None: det = cv2.FaceDetectorYN.create(model, "", (W, H), 0.75, 0.3, 5000)
        det.setInputSize((W, H)); _, F = det.detect(im)
        faces = [tuple(float(v) for v in r[:4]) + (float(r[-1]),) for r in (F if F is not None else []) if r[2] * r[3] > W * H * 0.0006]
        if ph.get('role') not in ('scene', 'setting'): continue  # 사물·풍경 그림은 그대로
        p0 = float(str(ph.get('fx') or '50%').split('%')[0]) / 100
        x = best_fx(W, H, faces, p0)
        if x is not None:
            out[ph['id']] = f"{x}% 50%"
            rep.append((ph['id'], ph.get('fx'), x, len(faces)))
    json.dump(out, open(f'{R}/ux/photo_fx.json', 'w'), ensure_ascii=False, indent=0, sort_keys=True)
    print(len(out), 'photos'); [print(*r) for r in rep[:40]]

if __name__ == '__main__': main(sys.argv[1])
