#UPDATE19
import os,sys,time,json,random,requests,re,socket,uuid,hashlib,base64,threading,itertools,shutil
from bs4 import BeautifulSoup
from datetime import datetime

IS_ANDROID=('ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ or os.path.exists('/system/build.prop'))
IS_IOS=(sys.platform=='darwin' and not os.path.exists('/usr/bin/python3') and os.path.exists(os.path.expanduser('~/Documents')))
IS_ASHELL=('ASHELL' in os.environ or os.path.exists(os.path.expanduser('~/Library/Application Support/com.holzschu.a-Shell')))
IS_MOBILE=(IS_ANDROID or IS_IOS or IS_ASHELL)

def _tw():
    try:
        c=shutil.get_terminal_size(fallback=(80,24)).columns
        return min(c,48) if IS_MOBILE else min(max(c-4,64),110)
    except: return 44 if IS_MOBILE else 76

W=_tw()

class C:
    RED='\033[91m';GREEN='\033[92m';YELLOW='\033[93m';BLUE='\033[94m'
    CYAN='\033[96m';WHITE='\033[97m';GRAY='\033[90m';PURPLE='\033[95m'
    BGREEN='\033[92;1m';BYELLOW='\033[93;1m';BCYAN='\033[96;1m';BPURPLE='\033[95;1m'
    BRED='\033[91;1m';BWHITE='\033[97;1m';BOLD='\033[1m';DIM='\033[2m'
    END='\033[0m';GOLD='\033[38;5;220m';LIME='\033[38;5;154m'
    TEAL='\033[38;5;87m';PINK='\033[38;5;213m';ORANGE='\033[38;5;208m'
    SKY='\033[38;5;117m';MINT='\033[38;5;121m';ROSE='\033[38;5;210m'

def sa(t): return re.sub(r'\033\[[0-9;]*m','',t)

def vl(t):
    t=sa(t); n=0
    for ch in t:
        cp=ord(ch)
        if (0x1F300<=cp<=0x1FAFF or 0x2600<=cp<=0x26FF or 0x2700<=cp<=0x27BF or
            0x4E00<=cp<=0x9FFF or 0x3400<=cp<=0x4DBF or 0xAC00<=cp<=0xD7AF or
            0xFF01<=cp<=0xFF60 or 0xFFE0<=cp<=0xFFE6): n+=2
        else: n+=1
    return n

def hc():
    if not IS_MOBILE: print('\033[?25l',end='',flush=True)
def sc():
    if not IS_MOBILE: print('\033[?25h',end='',flush=True)
def cl():
    if not IS_MOBILE: print('\033[2K\033[G',end='',flush=True)
def clr(): os.system('cls' if os.name=='nt' else 'clear')
def rw():
    global W; W=_tw()

def ui_sep(color=C.TEAL):
    rw(); ch='-' if IS_MOBILE else '═'
    print(f'{color}{ch*W}{C.END}')

def ui_thin(color=C.GRAY):
    rw(); print(f'{color}{"─"*W}{C.END}')

def ui_mid(text,color=C.WHITE,bold=False):
    rw(); p=max(0,(W-vl(text))//2)
    print(f'{C.BOLD if bold else ""}{" "*p}{color}{text}{C.END}')

def _brow(line,vc=C.TEAL):
    rpad=max(0,W-2-2-vl(line))
    print(f'{vc}║{C.END}  {line}{" "*rpad}{vc}║{C.END}')

def ui_box(lines,color=C.TEAL,title='',tc=None):
    rw(); tc=tc or C.BWHITE; h=W-2
    print(f'{color}╔{"═"*h}╗{C.END}')
    if title:
        p=max(0,(h-vl(title))//2)
        print(f'{color}║{C.END}{" "*p}{tc}{C.BOLD}{title}{C.END}{" "*(h-p-vl(title))}{color}║{C.END}')
        print(f'{color}╠{"═"*h}╣{C.END}')
    for ln in lines: _brow(ln,color)
    print(f'{color}╚{"═"*h}╝{C.END}')

def ui_panel(lines,color=C.TEAL,title='',tc=None):
    rw(); tc=tc or C.BWHITE; h=W-2
    print(f'{color}┌{"─"*h}┐{C.END}')
    if title:
        p=max(0,(h-vl(title))//2)
        print(f'{color}│{C.END}{" "*p}{tc}{C.BOLD}{title}{C.END}{" "*(h-p-vl(title))}{color}│{C.END}')
        print(f'{color}├{"─"*h}┤{C.END}')
    for ln in lines:
        rpad=max(0,h-2-vl(ln))
        print(f'{color}│{C.END}  {ln}{" "*rpad}{color}│{C.END}')
    print(f'{color}└{"─"*h}┘{C.END}')

def ui_tag(text,kind='info'):
    cfg={
        'ok':  (C.BGREEN, '✓','▏'),
        'err': (C.BRED,   '✗','▏'),
        'warn':(C.BYELLOW,'!','▏'),
        'info':(C.TEAL,   'i','▏'),
        'wait':(C.YELLOW, '…','▏'),
        'star':(C.GOLD,   '★','▏'),
        'lock':(C.ROSE,   '⊘','▏'),
    }
    c,ic,bar=cfg.get(kind,(C.WHITE,'>','▏'))
    print(f'  {C.DIM}{bar}{C.END}  {c}{ic}{C.END}  {C.WHITE}{text}{C.END}')

class Spinner:
    F=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    def __init__(self,msg='',color=C.TEAL):
        self.msg=msg; self.color=color
        self._e=threading.Event(); self._t=None
    def _run(self):
        hc()
        for f in itertools.cycle(self.F):
            if self._e.is_set(): break
            cl(); print(f'  {C.DIM}▏{C.END}  {self.color}{f}{C.END}  {C.WHITE}{self.msg}{C.END}',end='',flush=True)
            time.sleep(0.08)
        cl(); sc()
    def start(self):
        if IS_MOBILE: print(f'  {C.DIM}▏{C.END}  {self.color}▸{C.END}  {C.WHITE}{self.msg}{C.END}'); return
        self._t=threading.Thread(target=self._run,daemon=True); self._t.start()
    def stop(self,ok=True,msg=''):
        lbl=msg or self.msg
        if IS_MOBILE:
            print(f'  {C.DIM}▏{C.END}  {C.BGREEN if ok else C.BRED}{"✓" if ok else "✗"}{C.END}  {C.WHITE}{lbl}{C.END}'); return
        self._e.set()
        if self._t: self._t.join()
        print(f'  {C.DIM}▏{C.END}  {C.BGREEN if ok else C.BRED}{"✓" if ok else "✗"}{C.END}  {C.WHITE}{lbl}{C.END}')

def pbar(pct,w,col=C.TEAL,bg=C.GRAY):
    f=int(w*pct/100)
    return f'{col}{"█"*f}{bg}{"░"*(w-f)}{C.END}'

def anim_prog(label='',dur=0.8):
    rw()
    if IS_MOBILE:
        bw=max(8,W-vl(label)-10)
        print(f'  {C.DIM}▏{C.END}  {C.TEAL}{label}{C.END}  {pbar(100,bw)}'); return
    hc(); steps=34; bw=min(24,W-vl(label)-18)
    for i in range(steps+1):
        p=int(i*100/steps); b=pbar(p,bw)
        cl(); print(f'  {C.DIM}▏{C.END}  {C.TEAL}{label}{C.END}  {b}  {C.BYELLOW}{p:>3}%{C.END}',end='',flush=True)
        time.sleep(dur/steps)
    print(); sc()

class ScanBar:
    """Một thanh progress duy nhất cập nhật in-place suốt quá trình quét nhiều trang."""
    def __init__(self,total,label='Đang quét'):
        self.total=total; self.label=label; self._started=False
    def _render(self,pg,found,note=''):
        rw()
        pct=int(pg*100/self.total) if self.total else 100
        bw=max(10,W-vl(self.label)-28)
        b=pbar(pct,bw)
        info=f'{C.BYELLOW}{pg}/{self.total}{C.END}  {C.GRAY}·{C.END}  {C.LIME}+{found}{C.END}'
        if note: info+=f'  {C.GRAY}{note}{C.END}'
        if IS_MOBILE:
            print(f'  {C.DIM}▏{C.END}  {C.TEAL}{self.label}{C.END}  {b}  {info}')
        else:
            cl(); print(f'  {C.DIM}▏{C.END}  {C.TEAL}{self.label}{C.END}  {b}  {info}',end='',flush=True)
    def start(self):
        if not IS_MOBILE: hc()
        self._render(0,0); self._started=True
    def update(self,pg,found,note=''):
        self._render(pg,found,note)
    def done(self,found):
        if IS_MOBILE: return
        bw=max(10,W-vl(self.label)-28)
        b=pbar(100,bw,col=C.LIME)
        cl()
        print(f'  {C.DIM}▏{C.END}  {C.TEAL}{self.label}{C.END}  {b}  {C.BGREEN}✓{C.END}  {C.BWHITE}{found} bài{C.END}')
        sc()

def _logo():
    rw(); h=W-2; lines=[]
    lines.append(f'{C.TEAL}╔{"═"*h}╗{C.END}')
    def _r(l,r=''):
        ct=f' {l}  {C.DIM}│{C.END}  {r}'
        pad=max(0,h-vl(ct)-1)
        lines.append(f'{C.TEAL}║{C.END}{ct}{" "*pad} {C.TEAL}║{C.END}')
    _r(f'{C.BWHITE}OLM MASTER{C.END}  {C.GOLD}v3.6{C.END}',f'{C.LIME}AUTO SOLVER{C.END}')
    _r(f'{C.GRAY}by Tuan Anh{C.END}',f'{C.GRAY}olm.vn automation{C.END}')
    lines.append(f'{C.TEAL}╚{"═"*h}╝{C.END}')
    return lines

def _show_ads():
    rw()
    ui_panel([
        f'  {C.ORANGE}{C.BOLD}🛒  TUẤN ANH STUDIO{C.END}',
        f'  {C.YELLOW}BÁN TẤT CẢ CÁC TÀI KHOẢN PREMIUM{C.END}',
        f'',
        f'  {C.SKY}FB   :{C.END}  {C.BWHITE}fb.com/tuan.anh.317239{C.END}',
        f'  {C.LIME}ZALO :{C.END}  {C.BWHITE}0975711254{C.END}',
        f'',
        f'  {C.GOLD}💛  Mua tài khoản để ủng hộ admin nhé!{C.END}',
    ],C.ORANGE,title='📢  QUẢNG CÁO',tc=C.ORANGE)

def header(title='',sub='',anim=False,ads=False):
    clr(); print()
    logo=_logo()
    if anim and not IS_MOBILE:
        hc()
        for ln in logo: print(ln); time.sleep(0.03)
        sc()
    else:
        for ln in logo: print(ln)
    if ads:
        print(); _show_ads()
    if title:
        print()
        ui_mid(f'  {title}  ',C.BYELLOW,bold=True)
        if sub: ui_mid(sub[:W],C.GRAY)
        ui_thin(C.GRAY)
    print()

def ask(label,color=C.YELLOW):
    print(f'\n  {C.DIM}▏{C.END}  {color}{label}{C.END}  {C.GRAY}:{C.END} ',end='',flush=True)
    try: return input('')
    except (EOFError,KeyboardInterrupt): print(); return ''

def pause(msg=None):
    m=msg or f'{C.GRAY}  Nhấn Enter để tiếp tục{C.END}'
    try: input(f'\n{m}')
    except (EOFError,KeyboardInterrupt): pass

def menu(title,opts:dict):
    rw(); print()
    ui_sep(C.TEAL)
    ui_mid(f'  {title}  ',C.BYELLOW,bold=True)
    ui_thin(C.GRAY); print()
    keys=list(opts.keys())
    for k,v in opts.items():
        if k in ('0','q','3','4'): kc,vc,dot=C.ROSE,C.GRAY,'○'
        elif k=='5': kc,vc,dot=C.GRAY,C.GRAY,'○'
        else: kc,vc,dot=C.GOLD,C.WHITE,'◆'
        lbl=sa(v)[:W-10]
        print(f'  {C.DIM}▏{C.END}  {kc}[{k}]{C.END}  {C.DIM}{dot}{C.END}  {vc}{lbl}{C.END}')
    print()
    return ask(f'Chọn ({"/".join(keys)})',color=C.BYELLOW).strip()

_CHROME=['128','129','130','131','132','133','134','135']
_WIN=['10.0','11.0']
_LANG=['vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7','vi-VN,vi;q=0.9,en;q=0.8']

def _dev_profile():
    d=os.path.join(os.path.expanduser('~'),'.olmdata'); os.makedirs(d,exist_ok=True)
    p=os.path.join(d,'.dp.json')
    _required={'ua','lang','device_id','cv'}
    try:
        if os.path.exists(p):
            with open(p,'r') as f: prof=json.load(f)
            if _required.issubset(prof.keys()): return prof
            os.remove(p)
    except: pass
    cv=random.choice(_CHROME); wv=random.choice(_WIN); lg=random.choice(_LANG)
    ua=f'Mozilla/5.0 (Windows NT {wv}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{cv}.0.0.0 Safari/537.36'
    did=hashlib.sha256(os.urandom(32)).hexdigest()[:32]
    prof={'ua':ua,'lang':lg,'device_id':did,'cv':cv}
    try:
        with open(p,'w') as f: json.dump(prof,f)
    except: pass
    return prof

def _acc_profile(uname):
    b=_dev_profile()
    h=hashlib.md5(f"{b['device_id']}_{uname}".encode()).hexdigest()
    return {**b,'device_id':h}

_prof=_acc_profile('__init__')

def _hdrs():
    return {'user-agent':_prof['ua'],'accept':'application/json, text/javascript, */*; q=0.01','accept-language':_prof['lang'],'x-requested-with':'XMLHttpRequest','origin':'https://olm.vn','referer':'https://olm.vn/'}

def _ajax(ref=None):
    h=_hdrs()
    if ref: h['referer']=ref
    return h

HEADERS=_hdrs()

def _sh(extra=None,ajax=True,ref=None):
    h=_ajax(ref) if ajax else _hdrs()
    if extra: h.update(extra)
    return h

def _appdir():
    hm=os.path.expanduser('~')
    if IS_IOS or IS_ASHELL or '/var/mobile' in hm: d=os.path.join(hm,'Documents','.olmdata')
    elif IS_ANDROID:
        cands=[os.path.join(hm,'.olmdata'),os.path.join(hm,'.local','share','olm'),os.path.join(os.getcwd(),'.olmdata')]
        d=next((p for p in cands if os.access(os.path.dirname(p) or '.',os.W_OK)),cands[0])
    elif os.name=='nt': d=os.path.join(os.getenv('LOCALAPPDATA',os.path.join(hm,'AppData','Local')),'OLMMaster')
    else: d=os.path.join(hm,'.local','share','olm')
    os.makedirs(d,exist_ok=True); return d

def _devhash():
    try: host=socket.gethostname()
    except: host='x'
    try: node=uuid.getnode()
    except: node=0
    return hashlib.sha256(f'{host}{node}'.encode()).hexdigest()[:8]

def _licpath(): os.makedirs(_appdir(),exist_ok=True); return os.path.join(_appdir(),f'.{_devhash()}sc')
def _kgpath(): os.makedirs(_appdir(),exist_ok=True); return os.path.join(_appdir(),f'.{_devhash()}kg')

USES_PER_KEY=5
MAX_KEYS_PER_DAY=3

def _load_kg():
    p=_kgpath()
    if not os.path.exists(p): return {'date':'','n':0,'dev':_devhash()}
    try:
        with open(p,'r') as f: d=json.load(f)
        if d.get('dev')!=_devhash(): return {'date':'','n':0,'dev':_devhash()}
        return d
    except: return {'date':'','n':0,'dev':_devhash()}

def _save_kg(d):
    try:
        with open(_kgpath(),'w') as f: json.dump(d,f); return True
    except: return False

def _keys_today():
    td=datetime.now().strftime('%Y-%m-%d'); d=_load_kg()
    return d.get('n',0) if d.get('date')==td else 0

def _rec_key():
    td=datetime.now().strftime('%Y-%m-%d'); d=_load_kg()
    if d.get('date')!=td: d={'date':td,'n':0,'dev':_devhash()}
    d['n']=d.get('n',0)+1; _save_kg(d)

def _enc(data):
    s=json.dumps(data); k='OLMSECURE2024'
    e=bytes(b^k[i%len(k)].encode()[0] for i,b in enumerate(s.encode()))
    b85=base64.b85encode(e).decode(); cs=hashlib.sha256(s.encode()).hexdigest()[:12]
    ns=hashlib.md5(os.urandom(8)).hexdigest()[:8]
    return f'{ns}{cs}{b85}{ns[::-1]}'

def _dec(enc):
    try:
        ns=enc[:8]; b85=enc[20:-8]; nr=enc[-8:]
        if ns[::-1]!=nr: return None
        raw=base64.b85decode(b85); k='OLMSECURE2024'
        dec=bytes(b^k[i%len(k)].encode()[0] for i,b in enumerate(raw))
        return json.loads(dec.decode())
    except: return None

def _load_lic():
    p=_licpath()
    if not os.path.exists(p): return None
    try:
        with open(p,'r') as f: return _dec(f.read())
    except: return None

def _save_lic(d):
    try:
        with open(_licpath(),'w') as f: f.write(_enc(d)); return True
    except: return False

def _fetch(url):
    try:
        r=requests.get(url,timeout=5)
        if r.status_code==200: return [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass
    return []

def check_vip(uname):
    if uname in _fetch('https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/refs/heads/main/ultra_vip'): return 'ultra'
    if uname in _fetch('https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/main/vip_users.txt'): return 'vip'
    return False

def _gen_key():
    now=datetime.now()
    try: host=socket.gethostname()
    except: host='x'
    try: node=uuid.getnode()
    except: node=0
    did=hashlib.md5(f'{host}{node}'.encode()).hexdigest()[:16]
    h=hashlib.sha256(f'{did}{now.timestamp()}{random.randint(1000,9999)}'.encode()).hexdigest()
    return f'OLMFREE-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}'

LIN4M_TOKEN='698b226d9150d31d216157a5'

def _short(url):
    try:
        r=requests.get('https://link4m.co/api-shorten/v2',params={'api':LIN4M_TOKEN,'url':url},headers={'User-Agent':'Mozilla/5.0'},timeout=8)
        if r.status_code==200:
            d=r.json()
            if d.get('status')=='success': return d.get('shortenedUrl')
    except: pass
    time.sleep(random.uniform(0.5,1.0)); return None

def _pubip():
    try: return requests.get('https://api.ipify.org',timeout=5).text
    except: return '127.0.0.1'

def key_flow():
    kt=_keys_today()
    if kt>=MAX_KEYS_PER_DAY:
        ui_tag(f'Đã đạt giới hạn {MAX_KEYS_PER_DAY} key/ngày','err')
        ui_tag('Vui lòng quay lại vào ngày mai','warn'); pause(); return None
    ui_tag(f'Còn {MAX_KEYS_PER_DAY-kt}/{MAX_KEYS_PER_DAY} key hôm nay','info')
    key=_gen_key(); real=f'https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html?ma={key}'
    sp=Spinner('Đang tạo liên kết…',C.TEAL); sp.start()
    lnk=_short(real)
    sp.stop(bool(lnk),'Sẵn sàng' if lnk else 'Không thể tạo liên kết')
    if not lnk: return None
    ld=lnk[:W-6] if len(lnk)>W-6 else lnk
    print()
    ui_panel([
        f'{C.TEAL}Liên kết:{C.END}','',
        f'  {C.BWHITE}{ld}{C.END}','',
        f'{C.GRAY}  1. Mở link và hoàn thành xác thực{C.END}',
        f'{C.GRAY}  2. Sao chép key rồi dán vào đây{C.END}',
    ],C.TEAL,title='KÍCH HOẠT KEY',tc=C.GOLD)
    print()
    uk=ask('Nhập key').strip()
    if uk!=key: ui_tag('Key không hợp lệ','err'); pause(); return None
    _rec_key()
    return {'key':key,'remain':USES_PER_KEY,'expire':datetime.now().strftime('%Y-%m-%d'),'ip':_pubip()}

def _load_accs():
    p=os.path.join(_appdir(),'accounts.json')
    if os.path.exists(p):
        try:
            with open(p,'r',encoding='utf-8') as f: return json.load(f),p
        except: pass
    return {},p

def _save_accs(accs):
    _,p=_load_accs()
    try:
        with open(p,'w',encoding='utf-8') as f: json.dump(accs,f,ensure_ascii=False,indent=2); return True
    except: return False

def _del_acc_menu():
    accs,_=_load_accs()
    if not accs: ui_tag('Không có tài khoản nào đã lưu','warn'); return
    lst=list(accs.items()); print(); rows=[]
    for i,(nm,d) in enumerate(lst):
        n=nm[:W-18] if len(nm)>W-18 else nm
        rows.append(f'{C.GOLD}{i+1}.{C.END}  {C.WHITE}{n}{C.END}  {C.GRAY}{d.get("saved_at","")}{C.END}')
    rows.append(f'{C.ROSE}0.{C.END}  {C.GRAY}Huỷ{C.END}')
    ui_panel(rows,C.ROSE,title='XÓA TÀI KHOẢN',tc=C.BRED)
    ch=ask(f'Chọn tài khoản cần xóa (0–{len(lst)})').strip()
    if ch=='0' or not ch: return
    if ch.isdigit():
        idx=int(ch)-1
        if 0<=idx<len(lst):
            nm,d=lst[idx]
            disp=nm[:W-22] if len(nm)>W-22 else nm
            cf=ask(f'Xác nhận xóa "{disp}"? (y/n)').strip().lower()
            if cf=='y':
                del accs[nm]; _save_accs(accs)
                ui_tag(f'Đã xóa tài khoản: {disp}','ok')
            else:
                ui_tag('Đã huỷ','info')
        else:
            ui_tag('Lựa chọn không hợp lệ','err')
    time.sleep(0.5)

def _sel_acc():
    accs,_=_load_accs()
    if not accs: return None,None
    while True:
        lst=list(accs.items()); print(); rows=[]
        for i,(nm,d) in enumerate(lst):
            n=nm[:W-18] if len(nm)>W-18 else nm
            rows.append(f'{C.GOLD}{i+1}.{C.END}  {C.WHITE}{n}{C.END}  {C.GRAY}{d.get("saved_at","")}{C.END}')
        rows.append(f'{C.ROSE}0.{C.END}  {C.GRAY}Tài khoản khác{C.END}')
        rows.append(f'{C.BRED}x.{C.END}  {C.GRAY}Xóa tài khoản{C.END}')
        ui_panel(rows,C.TEAL,title='TÀI KHOẢN ĐÃ LƯU',tc=C.SKY)
        ch=ask(f'Chọn (0–{len(lst)} hoặc x=xóa)').strip().lower()
        if ch=='0': return None,None
        if ch=='x':
            _del_acc_menu()
            accs,_=_load_accs()
            if not accs: return None,None
            continue
        if ch.isdigit():
            idx=int(ch)-1
            if 0<=idx<len(lst):
                nm,d=lst[idx]; return d.get('username'),d.get('password')
        return None,None

def _store_acc(name,uname,pw):
    accs,_=_load_accs()
    accs[name]={'username':uname,'password':pw,'saved_at':datetime.now().strftime('%d/%m/%Y %H:%M')}
    _save_accs(accs)

def login_olm():
    global _prof,HEADERS
    header('ĐĂNG NHẬP',anim=True,ads=True)
    su,sp=_sel_acc()
    if su and sp:
        username,password=su,sp
    else:
        username=ask('Tên đăng nhập'); password=ask('Mật khẩu')
    if not username or not password: ui_tag('Không được để trống','err'); pause(); return None,None,None,None
    _prof=_acc_profile(username); HEADERS=_hdrs()
    session=requests.Session(); session.headers.update(HEADERS); print()
    sp2=Spinner('Đang đăng nhập…',C.TEAL); sp2.start()
    try:
        session.get('https://olm.vn/dangnhap',headers=HEADERS)
        csrf=session.cookies.get('XSRF-TOKEN')
        pl={'_token':csrf,'username':username,'password':password,'remember':'true','device_id':_prof['device_id'],'platform':'web'}
        session.post('https://olm.vn/post-login',data=pl,headers=_sh({'x-csrf-token':csrf}))
        res=session.get('https://olm.vn/thong-tin-tai-khoan/info',headers=HEADERS)
        m=re.search(r'name="name".*?value="(.*?)"',res.text)
        if m and m.group(1).strip():
            uname=m.group(1).strip(); sp2.stop(True,uname)
            uid=None
            for cn,cv in session.cookies.get_dict().items():
                if 'remember_web' in cn and '%7C' in cv:
                    try:
                        pts=cv.split('%7C')
                        if pts and pts[0].isdigit(): uid=pts[0]; break
                    except: pass
            if not uid:
                ids=re.findall(r'\b\d{10,}\b',res.text); uid=ids[0] if ids else username
            if not su or su!=username:
                _store_acc(uname,username,password)
            return session,uid,uname,username
        sp2.stop(False,'Sai tên đăng nhập hoặc mật khẩu'); pause(); return None,None,None,None
    except Exception: sp2.stop(False,'Lỗi hệ thống'); pause(); return None,None,None,None

def _vip_card(uname,dname,tier='vip'):
    rw(); h=W-2; bc=C.GOLD if tier=='ultra' else C.TEAL
    print()
    print(f'{bc}╔{"═"*h}╗{C.END}')
    def _r(l,r=''):
        ct=f'  {l}  {C.DIM}│{C.END}  {r}'
        pad=max(0,h-vl(ct)-1)
        print(f'{bc}║{C.END}{ct}{" "*pad} {bc}║{C.END}')
    lbl=f'{C.GOLD}✦ ULTRA VIP ✦{C.END}' if tier=='ultra' else f'{C.TEAL}✧ VIP ✧{C.END}'
    _r(lbl)
    print(f'{bc}╠{"═"*h}╣{C.END}')
    _r(f'{C.BWHITE}{dname[:W-10]}{C.END}',f'{C.GRAY}@{uname[:W-22]}{C.END}')
    _r(f'{C.LIME}{"Kiểm tra + Luyện tập không giới hạn" if tier=="ultra" else "Luyện tập không giới hạn"}{C.END}')
    print(f'{bc}╚{"═"*h}╝{C.END}')
    print()

def _is_done(span_text):
    if not span_text: return False
    t=span_text.lower()
    if re.search(r'\b0\s*%',t): return False
    if re.search(r'điểm[:\s]+0\b',t): return False
    return True

def get_assignments(session,npages=5,all_mode=False):
    lbl='TẤT CẢ BÀI' if all_mode else 'BÀI CHƯA HOÀN THÀNH'
    header('QUÉT BÀI TẬP',lbl)
    asgns=[]; seen=set()
    bar=ScanBar(npages,'Đang quét'); bar.start()
    for pg in range(1,npages+1):
        url=('https://olm.vn/lop-hoc-cua-toi?action=login' if pg==1 else f'https://olm.vn/lop-hoc-cua-toi/page-{pg}?action=login')
        try:
            resp=session.get(url,headers=HEADERS,timeout=10)
            if resp.status_code!=200: bar.update(pg,len(asgns)); continue
            soup=BeautifulSoup(resp.text,'html.parser')
            rows=soup.find_all('tr',class_='my-gived-courseware-item')
            if not rows: bar.update(pg,len(asgns)); continue
            for row in rows:
                lts=row.find_all('a',class_='olm-text-link')
                if not lts: continue
                ml=lts[0]; href=ml.get('href'); txt=ml.get_text(strip=True)
                if not href: continue
                tds=row.find_all('td')
                if len(tds)<2: continue
                lr=tds[1].get_text(strip=True)
                iv='[Video]' in lr
                ilt='[Lý thuyết]' in lr
                ikt='[Kiểm tra]' in lr or '[Kiem tra]' in lr
                itl='[Tự luận]' in lr or '[Tu luan]' in lr
                ifile='/file-' in (href or '')
                ibt=not(iv or ilt or ikt or ifile)
                if itl: continue
                ss=ml.find('span',class_='message-static-item')
                if not ss: ss=row.find('span',class_='message-static-item')
                span_txt=ss.get_text(strip=True) if ss else ''
                done=_is_done(span_txt)
                if not all_mode and done: continue
                fu=href if href.startswith('http') else 'https://olm.vn'+href
                if fu in seen: continue
                seen.add(fu)
                mon=row.find('span',class_='alert'); mt=mon.get_text(strip=True) if mon else 'Khác'
                tb=re.sub(r'\([^)]*\)','',txt).strip().replace(span_txt,'').strip()
                if done: disp='Đã làm'
                elif not span_txt: disp='Chưa nộp'
                else: disp=span_txt
                asgns.append({'title':tb[:60],'subject':mt[:20],'type':lr.replace('[','').replace(']','').strip()[:15],'status':disp,'done':done,'url':fu,'page':pg,'is_video':iv,'is_ly_thuyet':ilt,'is_bai_tap':ibt,'is_kiem_tra':ikt,'is_tu_luan':False})
            bar.update(pg,len(asgns))
        except Exception: bar.update(pg,len(asgns),'lỗi')
    bar.done(len(asgns)); print()
    if asgns:
        v=sum(1 for a in asgns if a['is_video']); lt=sum(1 for a in asgns if a['is_ly_thuyet'])
        bt=sum(1 for a in asgns if a['is_bai_tap']); kt=sum(1 for a in asgns if a['is_kiem_tra'])
        dn=sum(1 for a in asgns if a.get('done'))
        rows_p=[
            f'  {C.BWHITE}{len(asgns)} bài{C.END}','',
            f'  {C.TEAL}Video{C.END}         {C.BWHITE}{v}{C.END}',
            f'  {C.SKY}Lý thuyết{C.END}     {C.BWHITE}{lt}{C.END}',
            f'  {C.LIME}Bài tập{C.END}       {C.BWHITE}{bt}{C.END}',
            f'  {C.GOLD}Kiểm tra{C.END}      {C.BWHITE}{kt}{C.END}',
        ]
        if all_mode: rows_p+=['',f'  {C.MINT}Đã làm{C.END}        {C.BWHITE}{dn}{C.END}',f'  {C.ROSE}Chưa làm{C.END}      {C.BWHITE}{len(asgns)-dn}{C.END}']
        ui_panel(rows_p,C.TEAL,title=f'KẾT QUẢ  —  {lbl}')
    else: ui_tag('Không tìm thấy bài tập nào','warn')
    pause(); return asgns

def _show_list(asgns):
    if not asgns: return
    print()
    for idx,it in enumerate(asgns,1):
        rw(); mt=W-10
        title=it['title'][:mt-1]+'…' if len(it['title'])>mt else it['title']
        if it['is_video']:        tc,tag=C.TEAL, 'VIDEO     '
        elif it['is_ly_thuyet']:  tc,tag=C.SKY,  'LÝ THUYẾT'
        elif it['is_kiem_tra']:   tc,tag=C.GOLD, 'KIỂM TRA '
        else:                     tc,tag=C.LIME, 'BÀI TẬP  '
        is_done=it.get('done',False)
        num_col=C.MINT if is_done else C.GOLD
        sc2=C.MINT if is_done else C.ROSE
        done_mark=f'  {C.DIM}✓{C.END}' if is_done else ''
        print(f'  {C.DIM}▏{C.END}  {num_col}[{idx:2d}]{C.END}  {tc}{C.BOLD}{tag}{C.END}  {C.GRAY}{it["subject"][:14]}{C.END}{done_mark}')
        print(f'  {C.DIM}▏{C.END}       {C.BWHITE if not is_done else C.GRAY}{title}{C.END}')
        print(f'  {C.DIM}▏{C.END}       {sc2}{it["status"]}{C.END}')
        ui_thin(C.GRAY)
    print()

def _csrf(session,url):
    t=session.cookies.get('XSRF-TOKEN')
    if not t:
        r=session.get(url,timeout=10); m=re.search(r'<meta name="csrf-token" content="([^"]+)"',r.text)
        t=m.group(1) if m else ''
    return t

def _pids(url):
    ic=re.search(r'[?&]i_c=(\d+)',url); cm=re.search(r'-(\d+)(?:[?#]|$)',url)
    return cm.group(1) if cm else None, ic.group(1) if ic else None

def _pp(html):
    params={}
    for k,pats in {'id_school':[r"id_school['\"]?\s*[=:]\s*['\"]?(\d+)"],'id_group':[r"id_group['\"]?\s*[=:]\s*['\"]?(\d+)"],'type_vip':[r"type_vip['\"]?\s*[=:]\s*['\"]?(\d+)"],'id_grade':[r"id_grade['\"]?\s*[=:]\s*['\"]?(\d+)"]}.items():
        for p in pats:
            m=re.search(p,html)
            if m: params[k]=m.group(1); break
    return params

def _find_olm_list(node):
    if not isinstance(node,dict): return None
    if node.get('type')=='olm-list': return node
    for c in node.get('children',[]):
        r=_find_olm_list(c)
        if r: return r
    return None

_XK=b'1047823200'

def _xd(b64):
    try:
        raw=base64.b64decode(b64)
        return json.loads(bytes(b^_XK[i%len(_XK)] for i,b in enumerate(raw)).decode())
    except: return None

def _find_fill(node):
    if not isinstance(node,dict): return None
    if node.get('type')=='fillme-input': return str(node.get('content',''))
    for c in node.get('children',[]):
        r=_find_fill(c)
        if r is not None: return r
    return None

def _pqa(q,idx):
    try:
        qt=q.get('q_type',1); rj=q.get('json_content','')
        jc=_xd(rj) if isinstance(rj,str) else rj
        if not jc and isinstance(rj,str):
            try: jc=json.loads(rj)
            except: pass
        if not jc: return None
        root=jc.get('root',{})
        if qt==2:
            ans=_find_fill(root)
            return {'id':q.get('id',0),'idx':idx,'q_type':2,'list_type':'fillme','lock_pos':False,'correct_inds':[],'total_options':0,'fillme_answer':ans or ''}
        ol=_find_olm_list(root)
        if not ol: return None
        items=ol.get('children',[]); n=len(items)
        lt=ol.get('listType',''); nm=ol.get('name','')
        if qt==13 or nm=='true-false' or lt in ('true-false','truefalse'): lt='true-false'
        elif lt not in ('multichoice',): lt='singlechoice'
        ci=[i for i,it in enumerate(items) if it.get('correct',False)]
        return {'id':q.get('id',0),'idx':idx,'q_type':qt,'list_type':lt,'lock_pos':ol.get('lockOptionPosition',False),'correct_inds':ci,'total_options':n}
    except: return None

def _fetch_ans(session,qlib,url,id_sub='11',id_cate=None):
    if not qlib: return {}
    csrf=session.cookies.get('XSRF-TOKEN','')
    h=_sh({'x-csrf-token':csrf,'content-type':'application/x-www-form-urlencoded; charset=UTF-8'},ref=url)
    try:
        data=f'qlib_list={qlib}&id_subject={id_sub}&cv_q=1&encodeXORBase64=true'
        if id_cate: data+=f'&id_skill={id_cate}'
        r=session.post('https://olm.vn/course/question/get-question-of-ids',data=data,headers=h,timeout=10)
        if r.status_code!=200: return {}
        qs=r.json()
        if not isinstance(qs,list): return {}
        return {idx:info for idx,q in enumerate(qs) for info in [_pqa(q,idx)] if info}
    except: return {}

def _parse_video(html):
    res={'list_quiz':[],'list_marker':[],'video_url':None}
    try:
        m=re.search(r'list_quiz\s*:\s*JSON\.parse\(\'(.*?)\'\)',html)
        if m: res['list_quiz']=json.loads(m.group(1))
        m=re.search(r'list_marker\s*:\s*(\[.*?\])\s*,',html,re.DOTALL)
        if m:
            try: res['list_marker']=json.loads(m.group(1))
            except: pass
        m=re.search(r'video_url\s*:\s*["\']([^"\']+)["\']',html)
        if m: res['video_url']=m.group(1)
    except: pass
    return res

def _vid_dur(html):
    try:
        soup=BeautifulSoup(html,'html.parser')
        sp=soup.find('span',class_='mejs__duration')
        if sp:
            pts=sp.get_text(strip=True).split(':')
            if len(pts)==2: return int(pts[0])*60+int(pts[1])
            if len(pts)==3: return int(pts[0])*3600+int(pts[1])*60+int(pts[2])
    except: pass
    m=re.search(r'mejs__duration[^>]*>\s*(\d+):(\d+)(?::(\d+))?',html,re.DOTALL)
    if m:
        if m.group(3): return int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))
        return int(m.group(1))*60+int(m.group(2))
    for p in [r'duration["\']?\s*[=:]\s*["\']?(\d{2,4})["\']?',r'"length"\s*:\s*(\d{2,4})']:
        m=re.search(p,html)
        if m:
            v=int(m.group(1))
            if 60<=v<=7200: return v
    return None

def _yt_dur(session,html,vurl=None):
    try:
        vid=None
        if vurl:
            m=re.search(r'[?&]v=([A-Za-z0-9_-]{11})',vurl)
            if m: vid=m.group(1)
        if not vid:
            m=re.search(r'youtube\.com/embed/([A-Za-z0-9_-]{11})[?&"\'<\s]',html)
            if m: vid=m.group(1)
        if not vid: return None
        _s=requests.Session(); _s.headers.update({'User-Agent':'Mozilla/5.0','Accept-Language':'en-US'})
        r=_s.get(f'https://www.youtube.com/watch?v={vid}',timeout=10)
        ms=re.findall(r'"lengthSeconds"\s*:\s*"(\d+)"',r.text)
        if ms:
            v=max(int(x) for x in ms)
            if v>=30: return v
    except: pass
    return None

def _est_dur(html):
    for p in [r'duration["\']?\s*[=:]\s*["\']?(\d{2,4})',r'"length"\s*:\s*(\d{2,4})',r'totalTime\s*[=:]\s*(\d{2,4})']:
        m=re.search(p,html)
        if m:
            v=int(m.group(1))
            if 60<=v<=7200: return v
    return 480

def _count_q(html):
    for p in [r'count_problems\s*[=:]\s*["\']?(\d+)',r'total_q\s*[=:]\s*["\']?(\d+)',r'"total"\s*:\s*"?(\d+)"?']:
        m=re.search(p,html)
        if m and int(m.group(1))>0: return int(m.group(1))
    soup=BeautifulSoup(html,'html.parser')
    for cls in ['quiz-item','question-item','q-item','problem-item']:
        it=soup.find_all(class_=cls)
        if it: return len(it)
    return 0

def _vid_qs(session,id_cate,html,url):
    id_sub=None
    for p in [r"id_subject['\"]?\s*[=:]\s*['\"]?(\d+)"]:
        m=re.search(p,html)
        if m: id_sub=m.group(1); break
    if not id_sub: id_sub='3'
    csrf=session.cookies.get('XSRF-TOKEN','')
    h=_sh({'x-csrf-token':csrf,'content-type':'application/x-www-form-urlencoded; charset=UTF-8'},ref=url)
    try:
        r=session.post('https://olm.vn/course/question/get-question-of-ids',data=f'id_subject={id_sub}&id_skill={id_cate}&cv_q=1',headers=h,timeout=10)
        if r.status_code!=200: return []
        qs=r.json()
        if not isinstance(qs,list): return []
        return [info for idx,q in enumerate(qs) for info in [_pqa(q,idx)] if info]
    except: return []

def _mk_vid_log(vqs,dur,mts=None):
    if not vqs:
        return [{'answer':'["0"]','params':'{"js":""}','result':[1],'wrong_skill':[],'correct_skill':[],'type':[11],'id':f'vid{random.randint(100000,999999)}','marker':0}],dur or 600
    d=dur or 600; nq=len(vqs); log=[]
    for i,q in enumerate(vqs):
        ci=q.get('correct_inds',[]); to=q.get('total_options',4)
        lp=q.get('lock_pos',False); qid=q.get('id',random.randint(100000000000,999999999999))
        ord2=list(range(to))
        if not lp: random.shuffle(ord2)
        co=ci[0] if ci else 0
        try: pos=ord2.index(co)
        except: pos=0
        mk=(mts[i] if mts and i<len(mts) else int((i+1)*d/(nq+1)))
        log.append({'answer':json.dumps([str(pos)]),'label':[chr(65+pos)],'params':json.dumps({'js':'','order':ord2}),'result':[1],'wrong_skill':[],'correct_skill':[],'type':[1],'id':qid,'marker':mk})
    return log,d

def _mk_log_correct(qi):
    log=[]; tt=0
    for idx in sorted(qi.keys()):
        inf=qi[idx]; qt=inf.get('q_type',1); lt=inf.get('list_type','singlechoice')
        ci=inf.get('correct_inds',[]); to=inf.get('total_options',4)
        t=random.randint(90,180); tt+=t
        if lt=='fillme' or qt==2:
            ans=inf.get('fillme_answer','0')
            log.append({'q_params':json.dumps([json.dumps({'js':''})]),'a_params':json.dumps([json.dumps([str(ans)])]),'result':1,'correct':1,'wrong':0,'a_index':idx,'time_spent':t}); continue
        ord2=list(range(to))
        if not inf.get('lock_pos',False): random.shuffle(ord2)
        if lt=='true-false' or qt==13:
            arr=[str(1 if i in ci else 0) for i in range(to)]
            ap=json.dumps([json.dumps(arr)])
        elif lt=='multichoice':
            ap=json.dumps([json.dumps([str(i) for i in sorted(ci)])])
        else:
            co=ci[0] if ci else 0
            ap=json.dumps([json.dumps([str(co)])])
        log.append({'q_params':json.dumps([json.dumps({'js':'','order':ord2})]),'a_params':ap,'result':1,'correct':1,'wrong':0,'a_index':idx,'time_spent':t})
    return log,tt,len(log)

def _mk_log_rand(nq,score=100):
    cn=(round((score/100)*nq) if score not in (100,0) else (nq if score==100 else 0))
    cn=max(0,min(nq,cn)); results=random.sample([1]*cn+[0]*(nq-cn),nq)
    log=[]; tt=0
    for i,ok in enumerate(results):
        t=random.randint(120,180); tt+=t
        ord2=list(range(4)); random.shuffle(ord2)
        ai='0' if ok else str(random.randint(1,3))
        log.append({'q_params':json.dumps([json.dumps({'js':'','order':ord2})]),'a_params':json.dumps([json.dumps([ai])]),'result':ok,'correct':ok,'wrong':0 if ok else 1,'a_index':i,'time_spent':t})
    return log,tt,cn

def _quiz_info(session,url,is_video=False):
    try:
        id_cate,id_cw=_pids(url)
        resp=session.get(url,timeout=10); html=resp.text
        pp=_pp(html)
        if not id_cw:
            for p in [r'id_courseware\s*[=:]\s*["\']?(\d+)']:
                m=re.search(p,html)
                if m: id_cw=m.group(1); break
        if not id_cate:
            for p in [r'id_cate\s*[=:]\s*["\']?(\d+)',r"'id_cate'\s*:\s*'(\d+)'",r'-(\d{8,})(?:[?#]|$)']:
                m=re.search(p,html)
                if m: id_cate=m.group(1); break
        dv=_parse_video(html) if is_video else {}
        qlib=''; qscr=''; id_sub='11'
        for p in [r"id_subject['\"]?\s*[=:]\s*['\"]?(\d+)"]:
            m=re.search(p,html)
            if m: id_sub=m.group(1); break
        if is_video:
            if dv.get('list_quiz'): qscr=','.join(str(q) for q in dv['list_quiz'])
            if not qscr:
                for p in [r'qscript_list\s*[=:]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',r'quiz_list\s*[=:]\s*["\'](\d{6,}(?:,\d{6,})*)["\']']:
                    m=re.search(p,html)
                    if m: qscr=m.group(1); break
        else:
            for p in [r'"list_quiz"\s*:\s*"(\d+(?:,\d+)*)"',r"'list_quiz'\s*:\s*'(\d+(?:,\d+)*)'",]:
                m=re.search(p,html,re.DOTALL)
                if m: qlib=m.group(1); break
            for p in [r'"id_subject"\s*:\s*"(\d+)"']:
                m=re.search(p,html,re.DOTALL)
                if m: id_sub=m.group(1); break
        tq=_count_q(html)
        if tq==0:
            ids=qlib or qscr
            if ids: tq=len([q for q in ids.split(',') if q.strip()])
        vdur=None
        if is_video:
            vdur=_vid_dur(html)
            if not vdur: vdur=_yt_dur(session,html,dv.get('video_url'))
            if not vdur:
                lm=dv.get('list_marker',[])
                mts=[int(mk['t']) for mk in lm if isinstance(mk,dict) and 't' in mk]
                if mts: vdur=int(mts[-1]/0.80)
            if not vdur: vdur=_est_dur(html)
        return qscr,qlib,id_sub,tq,id_cw,id_cate,html,pp,vdur,dv
    except: return None,'','11',0,None,None,'',{},None,{}

def _fix_expired(session,a,html):
    if 'quá hạn' not in html: return a,html
    url=a['url']; sep='&' if '?' in url else '?'
    eu=url+sep+'pass_expired=1'
    try: nh=session.get(eu,timeout=10).text; return {**a,'url':eu},nh
    except: return a,html

def _sub_video(session,a,uid,qscr,tq,id_cw,id_cate,html,pp,vdur=None,dv=None):
    if dv is None: dv={}
    lm=dv.get('list_marker',[]); mts=[int(mk['t']) for mk in lm if isinstance(mk,dict) and 't' in mk]
    dur=vdur or _vid_dur(html) or _yt_dur(session,html,dv.get('video_url'))
    if not dur and mts: dur=int(mts[-1]/0.80)
    if not dur: dur=_est_dur(html)
    log=[]; nq=0
    if id_cate:
        vqs=_vid_qs(session,id_cate,html,a['url'])
        if vqs:
            mt=mts if len(mts)==len(vqs) else None
            log,_=_mk_vid_log(vqs,dur,mt); nq=len(log)
    if not log and mts:
        log=[{'answer':json.dumps(['0']),'label':['A'],'params':json.dumps({'js':'','order':[0,1]}),'result':[1],'wrong_skill':[],'correct_skill':[],'type':[1],'id':random.randint(100000000000,999999999999),'marker':mt2} for mt2 in mts]
        nq=len(log)
    if not log and qscr:
        ids=[q for q in qscr.split(',') if q.strip()]
        if ids:
            n=len(ids)
            log=[{'answer':json.dumps(['0']),'label':['A'],'params':json.dumps({'js':'','order':[0,1]}),'result':[1],'wrong_skill':[],'correct_skill':[],'type':[1],'id':random.randint(100000000000,999999999999),'marker':int(dur*(i+1)/(n+1))} for i in range(n)]
            nq=n
    if not log:
        log=[{'answer':'["0"]','params':'{"js":""}','result':[1],'wrong_skill':[],'correct_skill':[],'type':[11],'id':f'vid{random.randint(100000,999999)}','marker':int(dur*0.95)}]
        nq=0
    ct=min(log[-1].get('marker',int(dur*0.95)),dur)
    csrf=_csrf(session,a['url']); ts=int(time.time())
    pl={'id_user':uid,'id_cate':id_cate or '0','id_grade':pp.get('id_grade','10'),'id_courseware':id_cw or '0','id_group':pp.get('id_group','0'),'id_school':pp.get('id_school','0'),'time_init':'','name_user':'','type_vip':pp.get('type_vip','0'),'time_spent':str(dur),'total_time':str(dur),'current_time':str(ct),'score':'100','data_log':json.dumps(log,separators=(',',':')),'correct':str(nq),'totalq':str(nq),'count_problems':str(nq),'date_end':str(ts),'ended':'1','save_star':'1'}
    h=_sh({'x-csrf-token':csrf},ref=a['url'])
    r=session.post('https://olm.vn/course/teacher-static',data=pl,headers=h,timeout=15)
    return r.status_code==200

def _find_node(node,t):
    if not isinstance(node,dict): return None
    if node.get('type')==t: return node
    for c in node.get('children',[]):
        r=_find_node(c,t)
        if r: return r
    return None

def _find_fill2(node):
    if not isinstance(node,dict): return None
    if node.get('type')=='fillme-input': return node.get('content','')
    for c in node.get('children',[]):
        r=_find_fill2(c)
        if r is not None: return r
    return None

def _parse_exam_q(q):
    qt=q.get('q_type',1); qid=q.get('id',0)
    data=_xd(q.get('json_content',''))
    fb={'id':qid,'q_type':qt,'answer':'["0"]','label':['A'],'order':[0,1,2,3],'result_val':[1],'type_flag':[1]}
    if not data: return fb
    root=data.get('root',{})
    if qt==2:
        ans=_find_fill2(root)
        return {'id':qid,'q_type':2,'answer':json.dumps([str(ans or '')]),'label':[],'order':[],'result_val':[1],'type_flag':[2]}
    olm=_find_node(root,'olm-list')
    if not olm: return fb
    items=olm.get('children',[]); lt=olm.get('listType','singlechoice')
    lock=olm.get('lockOptionPosition',False); n=len(items)
    ci=[i for i,it in enumerate(items) if it.get('correct')]
    ord2=list(range(n))
    if not lock: random.shuffle(ord2)
    if qt==13 or lt in ('true-false','truefalse'):
        return {'id':qid,'q_type':13,'answer':json.dumps([('1' if i in ci else '0') for i in range(n)]),'label':[],'order':ord2,'result_val':[1]*n,'type_flag':[13]}
    if lt=='multichoice':
        os2=sorted(ci); rp=sorted([ord2.index(c) for c in ci if c in ord2])
        return {'id':qid,'q_type':1,'answer':json.dumps([str(c) for c in os2]),'label':[chr(65+r) for r in rp],'order':ord2,'result_val':[1],'type_flag':[1]}
    co=ci[0] if ci else 0; rp=ord2.index(co) if co in ord2 else 0
    return {'id':qid,'q_type':1,'answer':json.dumps([str(co)]),'label':[chr(65+rp)],'order':ord2,'result_val':[1],'type_flag':[1]}

def _exam_log(ql,pm):
    log=[]
    for qid in ql:
        p=pm.get(qid)
        if not p:
            o=list(range(4)); random.shuffle(o)
            log.append({'answer':'["0"]','label':['A'],'params':json.dumps({'js':'','order':o}),'result':[1],'wrong_skill':[],'correct_skill':[],'type':[1],'idq':int(qid),'score':1,'chk':1}); continue
        e={'answer':p['answer'],'params':json.dumps({'js':'','order':p['order']}) if p['order'] else '{"js":""}','result':p['result_val'],'wrong_skill':[],'correct_skill':[],'type':p['type_flag'],'idq':int(p['id']),'score':1,'chk':1}
        if p.get('label'): e['label']=p['label']
        log.append(e)
    return log

def _wrong_answer(p):
    """Tạo answer sai chắc chắn: chọn original index KHÁC với đáp án đúng."""
    try:
        qt=p.get('q_type',1); tf=p.get('type_flag',[1])
        # True-false: đảo ngược từng vị trí
        if qt==13 or (tf and tf[0]==13):
            arr=json.loads(p['answer']); flipped=[str(1-int(x)) for x in arr]
            return json.dumps(flipped),[]
        # Multichoice / fillme: dùng lại đúng (khó làm sai có chủ đích) — đặt index 0 nếu đúng không phải 0
        if qt==2: return json.dumps(['__wrong__']),[]
        # Singlechoice: lấy correct original index rồi chọn index khác
        cor_list=json.loads(p['answer'])  # vd: ["2"]
        cor_idx=int(cor_list[0]) if cor_list else 0
        # tổng số options = len(order) nếu có, không thì dùng 4
        n_opts=len(p.get('order') or []); n_opts=n_opts if n_opts>=2 else 4
        wrong_opts=[i for i in range(n_opts) if i!=cor_idx]
        wi=random.choice(wrong_opts) if wrong_opts else (cor_idx+1)%n_opts
        o=p.get('order') or list(range(n_opts))
        return json.dumps([str(wi)]),[chr(65+o.index(wi))] if wi in o else [chr(65+wi)]
    except:
        return '["1"]',['B']

def _exam_log_partial(ql,pm,n_correct):
    """Tạo log kiểm tra với n_correct câu đúng, phần còn lại sai."""
    n=len(ql); n_correct=max(0,min(n,n_correct))
    correct_set=set(random.sample(range(n),n_correct)); log=[]; correct_qids=set()
    for idx,qid in enumerate(ql):
        is_cor=idx in correct_set
        if is_cor: correct_qids.add(qid)
        p=pm.get(qid)
        if not p:
            # Câu không có dữ liệu: đúng → index 0, sai → index 1 (luôn khác nhau)
            o=list(range(4)); random.shuffle(o)
            ai='0' if is_cor else '1'
            sc=1 if is_cor else 0
            log.append({'answer':f'["{ai}"]','label':[chr(65+int(ai))],'params':json.dumps({'js':'','order':o}),'result':[sc],'wrong_skill':[],'correct_skill':[],'type':[1],'idq':int(qid),'score':sc,'chk':sc}); continue
        if is_cor:
            e={'answer':p['answer'],'params':json.dumps({'js':'','order':p['order']}) if p.get('order') else '{"js":""}','result':p['result_val'],'wrong_skill':[],'correct_skill':[],'type':p['type_flag'],'idq':int(p['id']),'score':1,'chk':1}
            if p.get('label'): e['label']=p['label']
        else:
            # Tạo đáp án sai chắc chắn bằng original index khác với đáp án đúng
            w_ans,w_lbl=_wrong_answer(p)
            o=p.get('order') or list(range(4))
            e={'answer':w_ans,'params':json.dumps({'js':'','order':o}),'result':[0],'wrong_skill':[],'correct_skill':[],'type':p.get('type_flag',[1]),'idq':int(p['id']),'score':0,'chk':0}
            if w_lbl: e['label']=w_lbl
        log.append(e)
    return log,correct_qids

def _get_exam_nq(session,url):
    """Lấy số câu hỏi của bài kiểm tra từ URL (không cần nộp)."""
    try:
        resp=session.get(url,timeout=10); ql=_exam_ql(resp.text)
        return len(ql)
    except: return 0

def _choose_log(n,tsec,end_ts):
    s=end_ts-tsec; log=[]
    for i in range(n):
        log.append({'ind':i,'t':int(s+tsec*0.6*(i+1)/n+random.uniform(-2,2)),'l':i+1})
    for _ in range(random.randint(n,n*3)):
        i=random.randint(0,n-1)
        log.append({'ind':i,'t':int(s+tsec*random.uniform(0.65,0.98)),'l':i+1})
    return log

def _exam_ql(html):
    m=re.search(r'list_quiz\s*:\s*(\[[^\]]+\])',html)
    if m:
        try:
            items=json.loads(m.group(1))
            ids=[str(it['id_script']) for it in items if it.get('id_script')]
            if ids: return ids
        except: pass
    ids=re.findall(r'data-id-quiz=["\'](\d+)["\']',html)
    if ids: return list(dict.fromkeys(ids))
    for p in [r'quiz_list\s*[=:]\s*\[([^\]]+)\]']:
        m=re.search(p,html)
        if m:
            found=re.findall(r'\d{9,}',m.group(1))
            if found: return list(dict.fromkeys(found))
    return []

def _exam_sid(html):
    mb=re.search(r'var\s+data_exam\s*=\s*\{([^}]+)\}',html,re.DOTALL)
    if mb:
        m=re.search(r'_id\s*:\s*["\']([a-f0-9]{24})["\']',mb.group(1))
        if m: return m.group(1)
    m=re.search(r'_id\s*:\s*["\']([a-f0-9]{24})["\']',html)
    if m: return m.group(1)
    return ''

def _exam_tl(html):
    mb=re.search(r'var\s+data_exam\s*=\s*\{([^}]+)\}',html,re.DOTALL)
    if mb:
        m=re.search(r'time_limit\s*:\s*(\d+)',mb.group(1))
        if m:
            v=int(m.group(1)); return v if v>=300 else v*60
    return 45*60

def _detect_type(url,html):
    es=[
        'kiem-tra' in url.lower(),
        '[Kiểm tra]' in html or '[Kiem tra]' in html,
        'type_exam' in html,
        bool(re.search(r'var\s+data_exam\s*=',html)),
        bool(_exam_ql(html)) and not bool(re.search(r'"list_quiz"\s*:\s*"(\d+(?:,\d+)*)"',html)),
    ]
    vs=['video' in url.lower(),'[Video]' in html,'list_marker' in html]
    ls=['ly-thuyet' in url.lower(),'[Lý thuyết]' in html]
    ikt=sum(es)>=2; iv=any(vs) and not ikt; ilt=any(ls) and not ikt
    return ikt,iv,ilt,not(iv or ilt or ikt)

def sub_exam(session,a,uid,tsec=None,target_correct=None):
    try:
        url=a['url']; resp=session.get(url,timeout=12); html=resp.text
        if 'quá hạn' in html:
            a,html=_fix_expired(session,a,html); url=a['url']
            resp=session.get(url,timeout=12); html=resp.text
        pp=_pp(html); id_cate=''
        for p in [r'id_category\s*:\s*["\'](\d+)["\']',r'id_cate\s*[=:]\s*["\']?(\d+)']:
            m=re.search(p,html)
            if m: id_cate=m.group(1); break
        _,id_cw=_pids(url)
        if not id_cw:
            for p in [r'id_courseware\s*:\s*["\'](\d+)["\']',r'id_courseware\s*[=:]\s*["\']?(\d+)']:
                m=re.search(p,html)
                if m: id_cw=m.group(1); break
        id_sub=pp.get('id_subject','3')
        if not id_sub:
            m=re.search(r'id_subject\s*:\s*["\'](\d+)["\']',html)
            if m: id_sub=m.group(1)
        sid=_exam_sid(html); ql=_exam_ql(html)
        if not ql: return False,'Không hỗ trợ dạng bài'
        n=len(ql); pm={}
        csrf=_csrf(session,url)
        h=_sh({'x-csrf-token':csrf,'content-type':'application/x-www-form-urlencoded; charset=UTF-8'},ref=url)
        try:
            ra=session.post('https://olm.vn/course/question/get-question-of-ids',data=f'qlib_list={",".join(ql)}&id_subject={id_sub}&id_skill={id_cate}&cv_q=1&encodeXORBase64=true',headers=h,timeout=15)
            if ra.status_code==200:
                qs=ra.json()
                if isinstance(qs,list):
                    for q in qs:
                        if q.get('id'): pm[str(q['id'])]=_parse_exam_q(q)
        except: pass
        if not tsec: tsec=int(_exam_tl(html)*0.70)
        ct=int(time.time())
        # Xây dựng log theo target_correct
        use_partial=(target_correct is not None and 0<=target_correct<n)
        if use_partial:
            dl,correct_qids=_exam_log_partial(ql,pm,target_correct)
            actual_correct=target_correct
        else:
            dl=_exam_log(ql,pm); correct_qids=set(ql); actual_correct=n
        cl2=_choose_log(n,tsec,ct)
        pl=[('id_user','-1'),('id_cate',id_cate or '0'),('id_grade',pp.get('id_grade','10')),('id_courseware',id_cw or '0'),('id_group',pp.get('id_group','0')),('id_school',pp.get('id_school','0')),('time_init',''),('name_user',''),('type_vip','1'),('time_spent',str(tsec)),('tl_score','0'),('tn_score',str(actual_correct)),('ended','1'),('missed',str(n-actual_correct)),('correct',str(actual_correct)),('wrong',str(n-actual_correct)),('times',str(len(cl2))),('score',str(actual_correct)),('max_score',str(n)),('type_exam','1'),('time_stored',str(ct)),('save_star','1')]
        for qid in ql: pl.append(('quiz_list[]',qid))
        for qid in ql: pl.append((f'score_list[{qid}]','1' if qid in correct_qids else '0'))
        pl+=[('date_end',str(ct-random.randint(5,20))),('_id',sid),('nx',''),('_score','0'),('data_log',json.dumps(dl,separators=(',',':'))),('iframe','false'),('count_redo','0')]
        for idx,e in enumerate(cl2):
            pl+=[(f'choose_log[{idx}][ind]',str(e['ind'])),(f'choose_log[{idx}][t]',str(e['t'])),(f'choose_log[{idx}][l]',str(e['l']))]
        r=session.post('https://olm.vn/course/teacher-static',data=pl,headers=h,timeout=15)
        if r.status_code==200:
            msg=f'Đúng {actual_correct}/{n} câu'
            try:
                rd=r.json()
                if isinstance(rd,dict):
                    sv=rd.get('score') or rd.get('total_score')
                    if sv is not None: msg=f'Điểm {sv}/{n}'
            except: pass
            return True,msg
        return False,'Lỗi hệ thống'
    except Exception: return False,'Lỗi hệ thống'

def sub_asgn(session,a,uid,exam_sec=None,target_correct=None):
    try:
        if a.get('is_kiem_tra'): return sub_exam(session,a,uid,exam_sec,target_correct)
        res=_quiz_info(session,a['url'],a['is_video'])
        if res is None or res[0] is None: return False,'Lỗi hệ thống'
        qscr,qlib,id_sub,tq,id_cw,id_cate,html,pp,vdur,dv=res
        if 'quá hạn' in html:
            a,html=_fix_expired(session,a,html)
            res2=_quiz_info(session,a['url'],a['is_video'])
            if res2 and res2[0] is not None:
                qscr,qlib,id_sub,tq,id_cw,id_cate,html,pp,vdur,dv=res2
        if a['is_video']:
            ok=_sub_video(session,a,uid,qscr,tq,id_cw,id_cate,html,pp,vdur,dv)
            return (ok,'Hoàn thành') if ok else (False,'Lỗi hệ thống')
        if tq==0: return False,'Không hỗ trợ dạng bài'
        qi=_fetch_ans(session,qlib,a['url'],id_sub,id_cate) if qlib else {}
        if qi: dl,tt,cc=_mk_log_correct(qi)
        else: dl,tt,cc=_mk_log_rand(tq,100)
        csrf=_csrf(session,a['url']); ct=int(time.time())
        pl={'id_user':uid,'id_cate':id_cate or '0','id_grade':pp.get('id_grade','10'),'id_courseware':id_cw or '0','id_group':pp.get('id_group','6148789559'),'id_school':pp.get('id_school','0'),'time_init':str(ct-tt),'name_user':'','type_vip':pp.get('type_vip','0'),'time_spent':str(tt),'data_log':json.dumps(dl,separators=(',',':')),'score':'100','answered':str(len(dl)),'correct':str(cc),'count_problems':str(len(dl)),'missed':'0','time_stored':str(ct),'date_end':str(ct),'ended':'1','save_star':'1'}
        h=_sh({'x-csrf-token':csrf},ref=a['url'])
        r=session.post('https://olm.vn/course/teacher-static',data=pl,headers=h,timeout=15)
        if r.status_code==200: return True,'Hoàn thành'
        return False,'Lỗi hệ thống'
    except Exception: return False,'Lỗi hệ thống'

lic_data=None

def _deduct(is_vip):
    global lic_data
    if is_vip or not lic_data: return
    lic_data['remain']=max(0,lic_data.get('remain',0)-1); _save_lic(lic_data)

def _rem():
    global lic_data
    if not lic_data: return 0
    return max(0,lic_data.get('remain',0))

def solve_link(session,uid,is_vip,is_ultra=False):
    header('GIẢI BÀI TỪ LINK')
    if not is_vip and _rem()<=0:
        ui_tag('Hết lượt — lấy key mới để tiếp tục','err'); pause(); return False
    url=ask('Link OLM').strip()
    if not url.startswith('https://olm.vn/'): ui_tag('Link không hợp lệ','err'); pause(); return False
    try:
        sp=Spinner('Đang phân tích…',C.TEAL); sp.start()
        resp=session.get(url,timeout=10); html=resp.text
        ikt,iv,ilt,ibt=_detect_type(url,html)
        sp.stop(True,'Phân tích xong')
        lbl='Kiểm tra' if ikt else ('Video' if iv else ('Lý thuyết' if ilt else 'Bài tập'))
        tc2=C.GOLD if ikt else (C.TEAL if iv else (C.SKY if ilt else C.LIME))
        us=url[:W-8]+'…' if len(url)>W-8 else url
        print()
        ui_panel([
            f'  {C.GRAY}URL{C.END}   {C.DIM}▏{C.END}  {C.WHITE}{us}{C.END}',
            f'  {C.GRAY}Loại{C.END}  {C.DIM}▏{C.END}  {tc2}{C.BOLD}{lbl}{C.END}',
        ],C.TEAL,title='THÔNG TIN BÀI')
        if ikt and not is_ultra:
            print()
            ui_tag('Bài kiểm tra chỉ dành cho ULTRA VIP','lock')
            ui_tag('Liên hệ admin để nâng cấp','info')
            pause(); return False
        a={'title':'Bài từ link','subject':'','type':lbl,'status':'Chưa làm','url':url,'page':1,'is_video':iv,'is_ly_thuyet':ilt,'is_bai_tap':ibt,'is_kiem_tra':ikt,'is_tu_luan':False}
        exam_sec=None; exam_target_correct=None
        if ikt:
            ti=ask('Thời gian làm bài (phút)').strip()
            try: exam_sec=int(ti)*60 if ti else None
            except: exam_sec=None
            sc_ch=ask('Tùy chọn điểm? (y/n)').strip().lower()
            if sc_ch=='y':
                sp_nq=Spinner('Đang lấy thông tin bài…',C.TEAL); sp_nq.start()
                nq=_get_exam_nq(session,url); sp_nq.stop(nq>0,f'{nq} câu hỏi' if nq>0 else 'Không lấy được')
                if nq>0:
                    ui_tag(f'Bài kiểm tra có tổng {nq} câu hỏi','info')
                    tc_inp=ask(f'Muốn làm đúng bao nhiêu câu? (0–{nq}, Enter = tất cả)').strip()
                    if tc_inp.isdigit():
                        tc=int(tc_inp); tc=max(0,min(nq,tc)); exam_target_correct=tc
                        ui_tag(f'Sẽ làm đúng {tc}/{nq} câu','star')
        print()
        sp2=Spinner('Đang nộp bài…',C.LIME if not ikt else C.GOLD); sp2.start()
        ok,msg=sub_asgn(session,a,uid,exam_sec,exam_target_correct)
        if not ok and msg=='Không hỗ trợ dạng bài' and not ikt and is_ultra:
            sp2.stop(False,'Đang thử lại…')
            sp3=Spinner('Thử phương thức kiểm tra…',C.GOLD); sp3.start()
            ok,msg=sub_exam(session,{**a,'is_kiem_tra':True,'is_bai_tap':False},uid,exam_sec,exam_target_correct)
            sp3.stop(ok,msg)
        else:
            sp2.stop(ok,msg)
        print()
        if ok:
            _deduct(is_vip)
            ui_tag(msg,'ok')
            if not is_vip: ui_tag(f'Lượt còn lại: {_rem()}/{USES_PER_KEY}','star')
        else:
            ui_tag(msg,'err')
        pause(); return ok
    except Exception: ui_tag('Lỗi hệ thống','err'); pause(); return False

def solve_list(session,uid,is_vip,asgns=None,is_ultra=False):
    if asgns is None:
        ni=ask('Số trang quét (mặc định 3)').strip()
        np2=int(ni) if ni.isdigit() and int(ni)>0 else 3
        asgns=get_assignments(session,np2)
    if not asgns: return False
    header('CHỌN BÀI'); _show_list(asgns)
    sel=ask('Chọn bài  (0 = tất cả  |  1,2,3 = cụ thể)').strip()
    if sel=='0': idxs=list(range(len(asgns)))
    else:
        idxs=[]
        for pt in sel.split(','):
            p2=pt.strip()
            if p2.isdigit():
                i=int(p2)-1
                if 0<=i<len(asgns): idxs.append(i)
        if not idxs: ui_tag('Lựa chọn không hợp lệ','err'); pause(); return False
    has_kt=any(asgns[i]['is_kiem_tra'] for i in idxs)
    exam_sec=None; exam_score_custom=False
    if has_kt and is_ultra:
        ti=ask('Thời gian làm bài kiểm tra (phút)').strip()
        try: exam_sec=int(ti)*60 if ti else None
        except: exam_sec=None
        sc_ch=ask('Tùy chọn điểm bài kiểm tra? (y/n)').strip().lower()
        if sc_ch=='y': exam_score_custom=True
    total=len(idxs); ok_cnt=0; skip=0; print()
    for i,ai in enumerate(idxs,1):
        a=asgns[ai]; title=a['title'][:W-12]
        ui_thin(C.GRAY)
        print(f'  {C.DIM}▏{C.END}  {C.GOLD}[{i}/{total}]{C.END}  {C.WHITE}{title}{C.END}')
        if a.get('is_kiem_tra') and not is_ultra:
            ui_tag('Yêu cầu ULTRA VIP','lock'); skip+=1
            if i<total: time.sleep(0.2)
            continue
        if not is_vip and _rem()<=0:
            ui_tag('Hết lượt','err'); break
        # Hỏi số câu đúng nếu là kiểm tra và người dùng đã chọn tùy chỉnh điểm
        exam_target_correct=None
        if a.get('is_kiem_tra') and exam_score_custom and is_ultra:
            sp_nq=Spinner('Đang lấy thông tin bài…',C.TEAL); sp_nq.start()
            nq=_get_exam_nq(session,a['url']); sp_nq.stop(nq>0,f'{nq} câu hỏi' if nq>0 else 'Không lấy được')
            if nq>0:
                ui_tag(f'Bài này có tổng {nq} câu hỏi','info')
                tc_inp=ask(f'Muốn làm đúng bao nhiêu câu? (1–{nq}, Enter = tất cả)').strip()
                if tc_inp.isdigit():
                    tc=int(tc_inp); tc=max(0,min(nq,tc)); exam_target_correct=tc
                    ui_tag(f'Sẽ làm đúng {tc}/{nq} câu','star')
        sp=Spinner('Đang xử lý…',C.TEAL); sp.start()
        ok,msg=sub_asgn(session,a,uid,exam_sec,exam_target_correct)
        if not ok and msg=='Không hỗ trợ dạng bài' and not a.get('is_kiem_tra') and is_ultra:
            sp.stop(False,'Đang thử lại…')
            sp2=Spinner('Thử phương thức kiểm tra…',C.GOLD); sp2.start()
            ok,msg=sub_exam(session,{**a,'is_kiem_tra':True,'is_bai_tap':False},uid,exam_sec,exam_target_correct)
            sp2.stop(ok,msg)
        else:
            sp.stop(ok,msg)
        if ok: ok_cnt+=1; _deduct(is_vip)
        if i<total: time.sleep(0.8)
    print()
    done=total-skip
    ui_panel([
        f'  {C.GRAY}Đã xử lý{C.END}        {C.BWHITE}{done}/{total}{C.END}',
        f'  {C.LIME}Thành công{C.END}       {C.BWHITE}{ok_cnt}{C.END}',
        f'  {C.ROSE}Thất bại{C.END}         {C.BWHITE}{done-ok_cnt}{C.END}',
        f'  {C.GOLD}Bỏ qua (ULTRA){C.END}   {C.BWHITE}{skip}{C.END}',
    ],C.TEAL,title='KẾT QUẢ')
    if not is_vip and ok_cnt>0: ui_tag(f'Lượt còn lại: {_rem()}/{USES_PER_KEY}','star')
    pause(); return ok_cnt>0

def show_help():
    header('HƯỚNG DẪN SỬ DỤNG',ads=True)
    secs=[
        ('★  VIP / ULTRA VIP',C.GOLD,[
            f'Không giới hạn lượt sử dụng',
            f'ULTRA VIP: làm được cả bài kiểm tra',
        ]),
        ('⚡  TÀI KHOẢN FREE',C.TEAL,[
            f'Mỗi key: {USES_PER_KEY} lượt  ·  Tối đa {MAX_KEYS_PER_DAY} key/ngày',
            f'Hết key: chờ ngày mai',
        ]),
        ('📋  BÀI TẬP & VIDEO',C.LIME,[
            'Chọn 0 để giải tất cả, hoặc 1,2,3 để chọn cụ thể',
            'Đáp án lấy từ API OLM — video dùng thời lượng thực',
        ]),
        ('📝  BÀI KIỂM TRA',C.GOLD,[
            'Chỉ ULTRA VIP mới làm được',
            'Bài tập không giải được sẽ tự fallback sang kiểm tra (ULTRA)',
        ]),
    ]
    for title,col,lines in secs:
        print(f'\n  {col}{C.BOLD}{title}{C.END}')
        ui_thin(col)
        for ln in lines: print(f'  {C.DIM}▏{C.END}  {C.WHITE}{ln}{C.END}')
    print(); ui_sep(C.TEAL); pause()

def main_menu(session,uid,uname,is_vip,is_ultra=False):
    global lic_data
    if is_vip:
        header(ads=True)
        if not IS_MOBILE:
            hc()
            for i in range(5,0,-1):
                cl(); print(f'  {C.GRAY}Quảng cáo sẽ tắt sau {C.BYELLOW}{i}s{C.END}{C.GRAY}...{C.END}',end='',flush=True)
                time.sleep(1)
            cl(); sc()
        else:
            time.sleep(5)
    while True:
        header(ads=not is_vip)
        rw(); nd=uname[:W-24] if len(uname)>W-24 else uname
        if is_ultra:
            ui_panel([
                f'  {C.GOLD}✦ ULTRA VIP{C.END}  {C.BWHITE}{nd}{C.END}',
                f'  {C.LIME}Kiểm tra + Luyện tập không giới hạn{C.END}',
            ],C.GOLD)
        elif is_vip:
            ui_panel([
                f'  {C.TEAL}✧ VIP{C.END}  {C.BWHITE}{nd}{C.END}',
                f'  {C.LIME}Luyện tập không giới hạn{C.END}',
            ],C.TEAL)
        else:
            rem=_rem(); bw=max(10,W-len(nd)-22); b=pbar(min(rem*(100//USES_PER_KEY),100),bw)
            kl=MAX_KEYS_PER_DAY-_keys_today()
            ui_panel([
                f'  {C.BWHITE}{nd}{C.END}',
                f'  {b}  {C.BYELLOW}{rem}/{USES_PER_KEY} lượt{C.END}  {C.GRAY}·  {kl} key còn lại hôm nay{C.END}',
            ],C.TEAL)
        print()
        if not is_vip and _rem()<=0:
            kl=MAX_KEYS_PER_DAY-_keys_today()
            if kl>0:
                ui_tag(f'Hết lượt — còn {kl} key có thể tạo hôm nay','warn'); print()
                nl=key_flow()
                if nl:
                    _save_lic(nl); lic_data=nl
                    ui_tag(f'Key mới — {USES_PER_KEY} lượt  ·  còn {MAX_KEYS_PER_DAY-_keys_today()} key hôm nay','ok')
                    continue
                ch=menu('HẾT LƯỢT',{'4':'Đăng xuất','5':'Thoát','6':'Hướng dẫn'})
            else:
                ui_tag(f'Đã dùng hết {MAX_KEYS_PER_DAY} key hôm nay','err'); print()
                ch=menu('HẾT KEY HÔM NAY',{'4':'Đăng xuất','5':'Thoát','6':'Hướng dẫn'})
            if ch=='4':
                sp=Spinner('Đang đăng xuất…',C.TEAL); sp.start(); time.sleep(0.8); sp.stop(True,'Đã đăng xuất'); pause(); return False
            elif ch=='5': print(); ui_mid('Cảm ơn bạn đã sử dụng OLM Master',C.TEAL); print(); time.sleep(0.4); sys.exit(0)
            elif ch=='6': show_help()
            continue
        ch=menu('CHỨC NĂNG',{
            '1':'Bài chưa làm  (chỉ quét chưa làm)',
            '2':'Quét toàn bộ  (kể cả đã làm)',
            '3':'Giải bài từ link',
            '4':'Đăng xuất',
            '5':'Thoát',
            '6':'Hướng dẫn',
        })
        if ch=='1':
            ni=ask('Số trang quét (mặc định 3)').strip()
            np2=int(ni) if ni.isdigit() and int(ni)>0 else 3
            ag=get_assignments(session,np2,all_mode=False)
            if ag: solve_list(session,uid,is_vip,ag,is_ultra)
        elif ch=='2':
            ni=ask('Số trang quét (mặc định 5)').strip()
            np2=int(ni) if ni.isdigit() and int(ni)>0 else 5
            ag=get_assignments(session,np2,all_mode=True)
            if ag: solve_list(session,uid,is_vip,ag,is_ultra)
        elif ch=='3': solve_link(session,uid,is_vip,is_ultra)
        elif ch=='4':
            sp=Spinner('Đang đăng xuất…',C.TEAL); sp.start(); time.sleep(0.8); sp.stop(True,'Đã đăng xuất'); pause(); return False
        elif ch=='5': print(); ui_mid('Cảm ơn bạn đã sử dụng OLM Master',C.TEAL); print(); time.sleep(0.4); sys.exit(0)
        elif ch=='6': show_help()
        else: ui_tag('Không hợp lệ','err'); time.sleep(0.4)
    return True

def main():
    global lic_data
    clr(); print()
    for ln in _logo(): print(ln); time.sleep(0.035)
    print(); _show_ads(); time.sleep(0.15)
    show_help()
    while True:
        session,uid,uname,actual=login_olm()
        if not(session and uid and uname):
            if ask('Thử lại? (y/n)').strip().lower()!='y': ui_tag('Tạm biệt','info'); time.sleep(0.4); break
            continue
        sp=Spinner('Đang kiểm tra quyền hạn…',C.GOLD); sp.start()
        tier=check_vip(actual); sp.stop(True,'Xong')
        is_vip=(tier in ('vip','ultra')); is_ultra=(tier=='ultra')
        if is_vip:
            _vip_card(actual,uname,tier); pause('  Nhấn Enter để tiếp tục…')
            main_menu(session,uid,uname,is_vip,is_ultra)
        else:
            lic_data=_load_lic(); kl=MAX_KEYS_PER_DAY-_keys_today()
            if lic_data and lic_data.get('remain',0)>0:
                ui_tag(f'FREE — còn {lic_data["remain"]}/{USES_PER_KEY} lượt  ·  {kl} key còn lại hôm nay','info')
                pause('  Nhấn Enter để tiếp tục…')
            elif kl>0:
                ui_tag(f'Cần key để tiếp tục  ·  còn {kl}/{MAX_KEYS_PER_DAY} key hôm nay','warn')
                nl=key_flow()
                if nl:
                    _save_lic(nl); lic_data=nl
                    ui_tag(f'Key mới — {USES_PER_KEY} lượt  ·  còn {MAX_KEYS_PER_DAY-_keys_today()} key hôm nay','ok')
                    pause('  Nhấn Enter để tiếp tục…')
                else: ui_tag('Không thể tạo key','err'); pause(); continue
            else:
                ui_tag(f'Đã dùng hết {MAX_KEYS_PER_DAY} key hôm nay — quay lại vào ngày mai','err'); pause(); continue
            main_menu(session,uid,uname,False)

if __name__=='__main__':
    import traceback as _tb
    try: main()
    except KeyboardInterrupt:
        sc(); print(f'\n\n  {C.TEAL}Đã dừng.{C.END}\n'); sys.exit(0)
    except Exception:
        sc(); _tb.print_exc(); pause()
