import qrcode,json,datetime
out={}
for n in range(1,366):
    d=datetime.date(2027,1,1)+datetime.timedelta(n-1)
    if d.weekday()!=6: continue
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=0,version=3); q.add_data(f'https://aqedah.github.io/CBSR/?ldr={n}'); q.make(fit=False)
    m=q.get_matrix(); assert len(m)==29
    bits=''.join('1' if c else '0' for r in m for c in r); bits+='0'*((-len(bits))%4)
    out[n]=format(int(bits,2),'0%dx'%(len(bits)//4))
print(len(out),list(out)[:5])
json.dump(out,open('qr27.json','w'))
# 11-21: 체험판(2026) 주일 QR은 ?ldr26=날 (317–365일 가운데 주일). guide.html의 QR26에 같은 방식으로 넣었습니다.
