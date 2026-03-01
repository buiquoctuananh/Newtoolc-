#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os,sys,time,json,random,requests,re,socket,uuid,hashlib,base64,threading,itertools
from bs4 import BeautifulSoup
from datetime import datetime

IS_ANDROID=('ANDROID_ROOT' in os.environ or 'ANDROID_DATA' in os.environ or os.path.exists('/system/build.prop'))
IS_IOS=(sys.platform=='darwin' and not os.path.exists('/usr/bin/python3') and os.path.exists(os.path.expanduser('~/Documents')))
IS_ASHELL=('ASHELL' in os.environ or os.path.exists(os.path.expanduser('~/Library/Application Support/com.holzschu.a-Shell')))
W=48 if (IS_ANDROID or IS_IOS or IS_ASHELL) else 70

class C:
    RED='\033[91m';GREEN='\033[92m';YELLOW='\033[93m';BLUE='\033[94m'
    CYAN='\033[96m';WHITE='\033[97m';GRAY='\033[90m';PURPLE='\033[95m'
    BGREEN='\033[92;1m';BYELLOW='\033[93;1m';BCYAN='\033[96;1m';BPURPLE='\033[95;1m'
    BRED='\033[91;1m';BWHITE='\033[97;1m';BOLD='\033[1m';DIM='\033[2m'
    UNDER='\033[4m';END='\033[0m';GOLD='\033[38;5;220m';ORANGE='\033[38;5;208m'
    TEAL='\033[38;5;87m';LIME='\033[38;5;154m';PINK='\033[38;5;213m';INDIGO='\033[38;5;105m'
    BG_RED='\033[48;5;52m';BG_BLUE='\033[48;5;17m';BG_GREEN='\033[48;5;22m';BG_GOLD='\033[48;5;58m'

IS_MOBILE=(IS_ANDROID or IS_IOS or IS_ASHELL)

def strip_ansi(t): return re.sub(r'\033\[[0-9;]*m','',t)
def hide_cursor():
    if not IS_MOBILE: print('\033[?25l',end='',flush=True)
def show_cursor():
    if not IS_MOBILE: print('\033[?25h',end='',flush=True)
def clear_line():
    if not IS_MOBILE: print('\033[2K\033[G',end='',flush=True)

def a_divider(char='━',color=C.CYAN): print(f'{color}{char*W}{C.END}')
def a_thin(color=C.GRAY): print(f'{color}{"╌"*W}{C.END}')
def a_center(text,color=C.WHITE,bold=False):
    raw=strip_ansi(text);pad=max(0,(W-len(raw))//2);b=C.BOLD if bold else ''
    print(f'{b}{" "*pad}{color}{text}{C.END}')
def a_box(lines,color=C.CYAN,title=''):
    inner=W-4
    print(f'{color}┌{"─"*(W-2)}┐{C.END}')
    if title:
        raw=strip_ansi(title);pad=max(0,(inner-len(raw))//2);pad_r=max(0,inner-pad-len(raw))
        print(f'{color}│{C.END}  {" "*pad}{C.BWHITE}{C.BOLD}{title}{C.END}{" "*pad_r}  {color}│{C.END}')
        print(f'{color}├{"─"*(W-2)}┤{C.END}')
    for line in lines:
        raw=strip_ansi(line);pad_r=max(0,inner-len(raw))
        print(f'{color}│{C.END}  {line}{" "*pad_r}  {color}│{C.END}')
    print(f'{color}└{"─"*(W-2)}┘{C.END}')
def a_badge(text,kind='info'):
    icons={'success':(C.BGREEN,'✅'),'error':(C.BRED,'❌'),'warning':(C.BYELLOW,'⚠️ '),'info':(C.BCYAN,'ℹ️ '),'wait':(C.YELLOW,'⏳'),'rocket':(C.BPURPLE,'🚀')}
    c,icon=icons.get(kind,(C.WHITE,'•'))
    print(f'  {icon}  {c}{text}{C.END}')
def a_vip_card(username,display_name):
    print();print(f'{C.GOLD}{"▄"*W}{C.END}');inner=W-4
    def _row(text,color=C.BWHITE):
        raw=strip_ansi(text);pad=max(0,(inner-len(raw))//2);pad_r=max(0,inner-pad-len(raw))
        print(f'{C.GOLD}█{C.END} {" "*pad}{color}{text}{C.END}{" "*pad_r} {C.GOLD}█{C.END}')
    _row('');_row('👑  T À I  K H O Ả N  V I P  👑',C.GOLD);_row('─'*min(30,W-8),C.GOLD);_row('')
    dname=display_name[:W-14] if len(display_name)>W-14 else display_name
    _row(f'✦  {dname}  ✦',C.BWHITE)
    uname=username[:W-8] if len(username)>W-8 else username
    _row(f'@{uname}',C.YELLOW);_row('');_row('★  Không giới hạn lượt  ★',C.LIME)
    _row('⚡  Đầy đủ mọi tính năng  ⚡',C.TEAL);_row('')
    print(f'{C.GOLD}{"▀"*W}{C.END}');print()

def d_divider(char='═',color=C.BLUE): print(f'{color}{char*W}{C.END}')
def d_thin(color=C.GRAY): print(f'{color}{"─"*W}{C.END}')
def d_center(text,color=C.WHITE,bold=False):
    raw=strip_ansi(text);pad=max(0,(W-len(raw))//2);b=C.BOLD if bold else ''
    print(f'{b}{" "*pad}{color}{text}{C.END}')
def d_box(lines,color=C.CYAN,title=''):
    inner=W-4
    print(f'{color}╔{"═"*(W-2)}╗{C.END}')
    if title:
        raw=strip_ansi(title);pad=max(0,(W-2-len(raw))//2)
        print(f'{color}║{" "*pad}{C.BWHITE}{title}{C.END}{color}{" "*max(0,W-2-pad-len(raw))}║{C.END}')
        print(f'{color}╠{"═"*(W-2)}╣{C.END}')
    for line in lines:
        raw=strip_ansi(line);pad_r=max(0,inner-len(raw))
        print(f'{color}║  {C.END}{line}{" "*pad_r}  {color}║{C.END}')
    print(f'{color}╚{"═"*(W-2)}╝{C.END}')
def d_badge(text,kind='info'):
    icons={'success':(C.BGREEN,'✔',C.BG_GREEN),'error':(C.BRED,'✘',C.BG_RED),'warning':(C.BYELLOW,'⚠',C.BG_GOLD),'info':(C.BCYAN,'ℹ',C.BG_BLUE),'wait':(C.YELLOW,'⏳',''),'rocket':(C.BPURPLE,'🚀','')}
    c,icon,_=icons.get(kind,(C.WHITE,'·',''))
    print(f'  {c}{icon}  {C.END}{C.WHITE}{text}{C.END}')
def d_vip_card(username,display_name):
    print();print(f'{C.GOLD}{"▀"*W}{C.END}')
    lines=[
        f'{C.GOLD}{"═"*60:^{W}}{C.END}',
        f'{"":>{(W//2)-10}}{C.GOLD}👑  V I P  A C C O U N T  👑{C.END}',
        f'{C.GOLD}{"═"*60:^{W}}{C.END}','',
        f'{"":>{(W//2)-14}}{C.BWHITE}✦  {C.GOLD}{display_name}{C.END}  {C.BWHITE}✦{C.END}',
        f'{"":>{(W//2)-10}}{C.DIM}{C.YELLOW}@{username}{C.END}','',
        f'{"":>{(W//2)-16}}{C.LIME}★  Không giới hạn lượt sử dụng  ★{C.END}',
        f'{"":>{(W//2)-14}}{C.GOLD}{"─"*28}{C.END}',
        f'{"":>{(W//2)-18}}{C.TEAL}⚡  Truy cập đầy đủ mọi tính năng  ⚡{C.END}','',
    ]
    for line in lines: print(line);time.sleep(0.03)
    print(f'{C.GOLD}{"▄"*W}{C.END}');print()

def ui_divider(char=None,color=None):
    if IS_MOBILE: a_divider(char or '━',color or C.CYAN)
    else: d_divider(char or '═',color or C.BLUE)
def ui_thin(color=None):
    if IS_MOBILE: a_thin(color or C.GRAY)
    else: d_thin(color or C.GRAY)
def ui_center(text,color=C.WHITE,bold=False):
    if IS_MOBILE: a_center(text,color,bold)
    else: d_center(text,color,bold)
def ui_box(lines,color=C.CYAN,title=''):
    if IS_MOBILE: a_box(lines,color,title)
    else: d_box(lines,color,title)
def ui_badge(text,kind='info'):
    if IS_MOBILE: a_badge(text,kind)
    else: d_badge(text,kind)
def ui_vip_card(username,display_name):
    if IS_MOBILE: a_vip_card(username,display_name)
    else: d_vip_card(username,display_name)

class Spinner:
    FRAMES=['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    def __init__(self,msg='',color=C.CYAN): self.msg=msg;self.color=color;self._stop=threading.Event();self._t=None
    def _spin(self):
        hide_cursor()
        for f in itertools.cycle(self.FRAMES):
            if self._stop.is_set(): break
            clear_line();print(f'  {self.color}{f}{C.END}  {C.WHITE}{self.msg}{C.END}',end='',flush=True);time.sleep(0.08)
        clear_line();show_cursor()
    def start(self):
        if IS_MOBILE: print(f'  {self.color}⟳{C.END}  {C.WHITE}{self.msg}…{C.END}');return
        self._t=threading.Thread(target=self._spin,daemon=True);self._t.start()
    def stop(self,ok=True,msg=''):
        label=msg or self.msg
        if IS_MOBILE:
            icon=f'{C.BGREEN}✅{C.END}' if ok else f'{C.BRED}❌{C.END}'
            print(f'  {icon}  {C.WHITE}{label}{C.END}');return
        self._stop.set()
        if self._t: self._t.join()
        icon=f'{C.BGREEN}✔{C.END}' if ok else f'{C.BRED}✘{C.END}'
        print(f'  {icon}  {C.WHITE}{label}{C.END}')

def progress_bar(pct,width,color=C.CYAN,bg=C.GRAY):
    filled=int(width*pct/100)
    return f'{color}{"█"*filled}{bg}{"░"*(width-filled)}{C.END}'
def animate_progress(label='',duration=1.0):
    if IS_MOBILE:
        bw=max(8,W-len(strip_ansi(label))-10);bar=progress_bar(100,bw)
        print(f'  {C.BCYAN}{label}{C.END} {bar} {C.BYELLOW}100%{C.END}');return
    hide_cursor();steps,bw=40,36
    for i in range(steps+1):
        pct=int(i*100/steps);bar=progress_bar(pct,bw)
        clear_line();print(f'  {C.BCYAN}{label}{C.END} {bar} {C.BYELLOW}{pct:>3}%{C.END}',end='',flush=True)
        time.sleep(duration/steps)
    print();show_cursor()
def type_print(text,color=C.WHITE,delay=0.018):
    if IS_MOBILE: print(f'{color}{text}{C.END}');return
    hide_cursor()
    for ch in text: print(f'{color}{ch}{C.END}',end='',flush=True);time.sleep(delay)
    show_cursor();print()
def pulse_banner(text,color=C.CYAN):
    if IS_MOBILE: print(f'{color}{text[:W]}{C.END}');return
    pad=max(0,(W-len(text))//2);colors=[C.BLUE,C.CYAN,C.BCYAN,C.BWHITE,C.BCYAN,C.CYAN,C.BLUE]
    hide_cursor()
    for c in colors: print(f'\r{" "*pad}{c}{text}{C.END}',end='',flush=True);time.sleep(0.045)
    print();show_cursor()
def slide_in(lines,delay=0.03):
    hide_cursor()
    for line in lines: print(line);(time.sleep(delay) if not IS_MOBILE else None)
    show_cursor()

def clr(): os.system('cls' if os.name=='nt' else 'clear')

def _mobile_logo():
    inner=W-2
    return [
        f'{C.BCYAN}┌{"─"*inner}┐{C.END}',
        f'{C.BCYAN}│{C.END}  {C.BWHITE}⚡ {C.GOLD}OLM {C.BCYAN}MASTER{C.END}  {C.GRAY}·{C.END}  {C.BPURPLE}AUTO SOLVER{C.END}{" "*max(0,inner-32)}  {C.BCYAN}│{C.END}',
        f'{C.BCYAN}│{C.END}  {C.GRAY}bởi Tuấn Anh{C.END}{" "*max(0,inner-18)}{C.BPURPLE}v3.2{C.END}  {C.BCYAN}│{C.END}',
        f'{C.BCYAN}└{"─"*inner}┘{C.END}',
    ]
def _desktop_logo():
    return [
        f"  {C.BCYAN}┌─────────────────────────────────────────────────────────────┐{C.END}",
        f"  {C.BCYAN}│{C.END}  {C.BWHITE}  ██████╗ {C.CYAN}██╗     {C.BCYAN}███╗   ███╗{C.END}   {C.GOLD}M A S T E R{C.END}   {C.BPURPLE}v3.2{C.END}  {C.BCYAN}│{C.END}",
        f"  {C.BCYAN}│{C.END}  {C.BWHITE} ██╔═══██╗{C.CYAN}██║     {C.BCYAN}████╗ ████║{C.END}   {C.GRAY}AUTO SOLVER{C.END}         {C.BCYAN}│{C.END}",
        f"  {C.BCYAN}│{C.END}  {C.BWHITE} ██║   ██║{C.CYAN}██║     {C.BCYAN}██╔████╔██║{C.END}   {C.GRAY}by Tuấn Anh{C.END}         {C.BCYAN}│{C.END}",
        f"  {C.BCYAN}│{C.END}  {C.BWHITE} ╚██████╔╝{C.CYAN}███████╗{C.BCYAN}██║╚██╔╝██║{C.END}                         {C.BCYAN}│{C.END}",
        f"  {C.BCYAN}│{C.END}  {C.BWHITE}  ╚═════╝ {C.CYAN}╚══════╝{C.BCYAN}╚═╝ ╚═╝ ╚═╝{C.END}                         {C.BCYAN}│{C.END}",
        f"  {C.BCYAN}└─────────────────────────────────────────────────────────────┘{C.END}",
    ]
def header(title='',subtitle='',animated=False):
    clr();print()
    if IS_MOBILE:
        a_divider('━',C.BCYAN)
        for line in _mobile_logo(): print(line)
        a_divider('━',C.BCYAN)
        if title:
            a_thin(C.GRAY);a_center(f'◈  {title}  ◈',C.BYELLOW,bold=True)
            if subtitle: a_center(subtitle[:W-4],C.GRAY)
            a_thin(C.GRAY)
    else:
        d_divider('═',C.BLUE);logo=_desktop_logo()
        if animated: slide_in(logo,delay=0.03)
        else:
            for line in logo: print(line)
        d_divider('═',C.BLUE)
        if title:
            d_thin(C.GRAY);d_center(f'◈  {title}  ◈',C.BCYAN,bold=True)
            if subtitle: d_center(subtitle,C.GRAY)
            d_thin(C.GRAY)
    print()

def prompt_input(label,icon='▶',color=C.YELLOW):
    if IS_MOBILE:
        print(f'\n  {C.CYAN}▸{C.END} {color}{label}{C.END}');print(f'  {C.GOLD}›{C.END} ',end='',flush=True)
    else:
        print(f'\n  {C.CYAN}{icon} {C.END}{color}{label}{C.END}',end='');print(f'  {C.GRAY}›{C.END} ',end='')
    try: return input('')
    except (EOFError,KeyboardInterrupt): print();return ''

def pause(msg=None,color=C.GRAY):
    if msg is None: msg='  ↵ Nhấn Enter để tiếp tục…'
    try: input(f'\n{color}{msg}{C.END}')
    except (EOFError,KeyboardInterrupt): pass

def menu_select(title,options:dict):
    ui_thin(C.GRAY);ui_center(f'  {title}  ',C.BYELLOW,bold=True);ui_thin(C.GRAY);print()
    keys=list(options.keys())
    for k,v in options.items():
        if k in ('3','4','0','q'): kc,vc=C.BRED,C.GRAY
        elif k=='5': kc,vc=C.GRAY,C.GRAY
        else: kc,vc=C.BYELLOW,C.WHITE
        label=strip_ansi(v);label=label[:W-10] if len(label)>W-10 else label
        print(f'  {C.DIM}│{C.END}  {kc}[{k}]{C.END}  {vc}{label}{C.END}')
    print();ui_thin(C.GRAY)
    return prompt_input(f'Chọn ({"/".join(keys)})',icon='◆',color=C.BYELLOW).strip()

HEADERS={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'accept':'application/json, text/javascript, */*; q=0.01',
    'accept-language':'vi-VN,vi;q=0.9,en-US;q=0.8',
    'x-requested-with':'XMLHttpRequest',
    'origin':'https://olm.vn',
    'referer':'https://olm.vn/'
}

def get_appdata_dir():
    home=os.path.expanduser('~')
    is_ios_path=('/var/mobile' in home or '/private/var/mobile' in home)
    if IS_IOS or IS_ASHELL or is_ios_path:
        data_dir=os.path.join(home,'Documents','.olmdata')
        os.makedirs(data_dir,exist_ok=True)
        return data_dir
    if IS_ANDROID: return os.path.expanduser('~/.cache/google-chrome')
    if os.name=='nt': return os.path.join(os.getenv('LOCALAPPDATA',os.path.expanduser('~/AppData/Local')),'Microsoft','Windows','INetCache','IE')
    return os.path.expanduser('~/.local/share/olm')

def get_device_hash():
    try: host=socket.gethostname()
    except: host='iphone'
    try: node=uuid.getnode()
    except: node=0
    return hashlib.sha256(f'{host}{node}'.encode()).hexdigest()[:8]

def get_license_path(): os.makedirs(get_appdata_dir(),exist_ok=True);return os.path.join(get_appdata_dir(),f'.{get_device_hash()}sc')
def get_trial_path(): os.makedirs(get_appdata_dir(),exist_ok=True);return os.path.join(get_appdata_dir(),f'.{get_device_hash()}tr')

def encrypt_data(data):
    json_data=json.dumps(data);key='OLMSECURE2024'
    encrypted=bytes(b^key[i%len(key)].encode()[0] for i,b in enumerate(json_data.encode()))
    base85=base64.b85encode(encrypted).decode()
    checksum=hashlib.sha256(json_data.encode()).hexdigest()[:12]
    noise=hashlib.md5(os.urandom(8)).hexdigest()[:8]
    return f'{noise}{checksum}{base85}{noise[::-1]}'

def decrypt_data(encrypted):
    try:
        noise=encrypted[:8];base85=encrypted[20:-8];noise_rev=encrypted[-8:]
        if noise[::-1]!=noise_rev: return None
        decoded=base64.b85decode(base85);key='OLMSECURE2024'
        decrypted=bytes(b^key[i%len(key)].encode()[0] for i,b in enumerate(decoded))
        return json.loads(decrypted.decode())
    except: return None

def load_license():
    path=get_license_path()
    if not os.path.exists(path): return None
    try:
        with open(path,'r') as f: return decrypt_data(f.read())
    except: return None

def save_license(data):
    try:
        with open(get_license_path(),'w') as f: f.write(encrypt_data(data))
        return True
    except: return False

def is_trial_used():
    path=get_trial_path()
    if not os.path.exists(path): return False
    try:
        with open(path,'r') as f: d=decrypt_data(f.read());return bool(d and d.get('used') and d.get('device')==get_device_hash())
    except: return False

def mark_trial_used():
    try:
        with open(get_trial_path(),'w') as f: f.write(encrypt_data({'used':True,'device':get_device_hash(),'ts':int(time.time())}))
        return True
    except: return False

def check_vip(username):
    try:
        r=requests.get('https://raw.githubusercontent.com/thieunangbiettuot/ToolOLM/main/vip_users.txt',timeout=5)
        if r.status_code==200: return username in [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass
    return False

def generate_olm_key():
    now=datetime.now()
    try: host=socket.gethostname()
    except: host='iphone'
    try: node=uuid.getnode()
    except: node=0
    device_id=hashlib.md5(f'{host}{node}'.encode()).hexdigest()[:16]
    h=hashlib.sha256(f'{device_id}{now.timestamp()}{random.randint(1000,9999)}'.encode()).hexdigest()
    return f'OLMFREE-{now:%d%m}-{h[:4].upper()}-{h[4:8].upper()}'

LINK_SERVICES=[{'api':'https://link4m.co/api-shorten/v2','token':'698b226d9150d31d216157a5'}]

def create_short_link(url):
    for svc in LINK_SERVICES:
        try:
            r=requests.get(svc['api'],params={'api':svc['token'],'url':url},headers={'User-Agent':'Mozilla/5.0'},timeout=8)
            if r.status_code==200:
                d=r.json()
                if d.get('status')=='success': return d.get('shortenedUrl')
        except: pass
        time.sleep(random.uniform(0.5,1.2))
    return None

def get_public_ip():
    try: return requests.get('https://api.ipify.org',timeout=5).text
    except: return '127.0.0.1'

def handle_key_generation():
    key=generate_olm_key()
    real_url=f'https://keyfreedailyolmvip.blogspot.com/2026/02/blog-post.html?ma={key}'
    sp=Spinner('Đang tạo liên kết bảo mật…',C.CYAN);sp.start()
    short_link=create_short_link(real_url)
    sp.stop(bool(short_link),'Liên kết đã sẵn sàng' if short_link else 'Không thể tạo liên kết')
    if not short_link: return None
    link_display=short_link[:W-6] if len(short_link)>W-6 else short_link
    print()
    ui_box([
        f'{C.BCYAN}🔗 Liên kết xác thực:{C.END}','',
        f'  {C.BWHITE}{link_display}{C.END}','',
        f'{C.GRAY}  1. Mở link → hoàn thành xác thực{C.END}',
        f'{C.GRAY}  2. Sao chép key → dán vào bên dưới{C.END}',
    ],C.CYAN,title='KÍCH HOẠT KEY')
    print()
    user_key=prompt_input('Nhập key của bạn',icon='🔑').strip()
    if user_key!=key: ui_badge('Key không hợp lệ!','error');pause();return None
    return {'key':key,'remain':5,'expire':datetime.now().strftime('%Y-%m-%d'),'ip':get_public_ip()}

def load_saved_accounts():
    path=os.path.join(get_appdata_dir(),'accounts.json')
    if os.path.exists(path):
        try:
            with open(path,'r',encoding='utf-8') as f: return json.load(f),path
        except: pass
    return {},path

def save_accounts(accounts):
    _,path=load_saved_accounts()
    try:
        with open(path,'w',encoding='utf-8') as f: json.dump(accounts,f,ensure_ascii=False,indent=2)
        return True
    except: return False

def select_saved_account():
    accounts,_=load_saved_accounts()
    if not accounts: return None,None
    account_list=list(accounts.items());print();entries=[]
    for i,(name,d) in enumerate(account_list):
        n_d=name[:W-16] if len(name)>W-16 else name
        entries.append(f'{C.BYELLOW}{i+1}.{C.END} {C.WHITE}{n_d}{C.END}  {C.GRAY}{d.get("saved_at","")}{C.END}')
    entries.append(f'{C.BRED}0.{C.END}  {C.GRAY}Đăng nhập tài khoản mới{C.END}')
    ui_box(entries,C.CYAN,title='TÀI KHOẢN ĐÃ LƯU')
    choice=prompt_input(f'Chọn (0–{len(account_list)})',icon='◆').strip()
    if choice=='0': return None,None
    if choice.isdigit():
        idx=int(choice)-1
        if 0<=idx<len(account_list):
            name,d=account_list[idx];return d.get('username'),d.get('password')
    return None,None

def save_current_account(name,username,password):
    accounts,_=load_saved_accounts()
    accounts[name]={'username':username,'password':password,'saved_at':datetime.now().strftime('%d/%m/%Y %H:%M')}
    ui_badge(f'Đã lưu: {name}' if save_accounts(accounts) else 'Không thể lưu','success')

def login_olm():
    header('ĐĂNG NHẬP','Nhập thông tin tài khoản OLM',animated=True)
    saved_u,saved_p=select_saved_account()
    if saved_u and saved_p:
        use_saved=prompt_input('Dùng tài khoản đã lưu? (y/n)',icon='◆').strip().lower()
        if use_saved=='y': username,password=saved_u,saved_p
        else: username=prompt_input('Tên đăng nhập',icon='👤');password=prompt_input('Mật khẩu',icon='🔑')
    else: username=prompt_input('Tên đăng nhập',icon='👤');password=prompt_input('Mật khẩu',icon='🔑')
    if not username or not password: ui_badge('Không được để trống!','error');pause();return None,None,None,None
    session=requests.Session();session.headers.update(HEADERS);print()
    sp=Spinner('Đang kết nối đến OLM…',C.CYAN);sp.start()
    try:
        session.get('https://olm.vn/dangnhap',headers=HEADERS)
        csrf=session.cookies.get('XSRF-TOKEN')
        payload={'_token':csrf,'username':username,'password':password,'remember':'true','device_id':'0b48f4d6204591f83dc40b07f07af7d4','platform':'web'}
        h2=HEADERS.copy();h2['x-csrf-token']=csrf
        session.post('https://olm.vn/post-login',data=payload,headers=h2)
        check_res=session.get('https://olm.vn/thong-tin-tai-khoan/info',headers=HEADERS)
        match=re.search(r'name="name".*?value="(.*?)"',check_res.text)
        if match and match.group(1).strip():
            user_name=match.group(1).strip()
            sp.stop(True,f'Đăng nhập thành công ─ {user_name}')
            user_id=None
            for cn,cv in session.cookies.get_dict().items():
                if 'remember_web' in cn and '%7C' in cv:
                    try:
                        parts=cv.split('%7C')
                        if parts and parts[0].isdigit(): user_id=parts[0];break
                    except: pass
            if not user_id:
                ids=re.findall(r'\b\d{10,}\b',check_res.text);user_id=ids[0] if ids else username
            if not saved_u or saved_u!=username:
                if prompt_input('Lưu tài khoản này? (y/n)',icon='💾').strip().lower()=='y':
                    save_current_account(user_name,username,password)
            return session,user_id,user_name,username
        else: sp.stop(False,'Sai tên đăng nhập hoặc mật khẩu');pause();return None,None,None,None
    except Exception as e: sp.stop(False,f'Lỗi kết nối: {e}');pause();return None,None,None,None

def get_assignments_fixed(session,pages_to_scan=5):
    header('QUÉT BÀI TẬP',f'Đang quét {pages_to_scan} trang…')
    assignments=[];seen_links=set()
    for page in range(1,pages_to_scan+1):
        url=('https://olm.vn/lop-hoc-cua-toi?action=login' if page==1 else f'https://olm.vn/lop-hoc-cua-toi/page-{page}?action=login')
        animate_progress(f'Trang {page}/{pages_to_scan}',duration=0.6)
        try:
            response=session.get(url,headers=HEADERS,timeout=10)
            if response.status_code!=200: ui_badge(f'Lỗi HTTP {response.status_code} trang {page}','error');continue
            soup=BeautifulSoup(response.text,'html.parser')
            rows=soup.find_all('tr',class_='my-gived-courseware-item')
            if not rows: ui_badge(f'Trang {page}: không có bài','warning');continue
            page_count=0
            for row in rows:
                link_tags=row.find_all('a',class_='olm-text-link')
                if not link_tags: continue
                main_link=link_tags[0];href=main_link.get('href');link_text=main_link.get_text(strip=True)
                if href and any(s in link_text for s in ['(Toán','(Ngữ văn','(Tiếng Anh','(Tin học']): continue
                if not href: continue
                tds=row.find_all('td')
                if len(tds)<2: continue
                loai_raw=tds[1].get_text(strip=True)
                is_video='[Video]' in loai_raw or 'Video' in loai_raw
                is_ly_thuyet='[Lý thuyết]' in loai_raw
                is_kiem_tra='[Kiểm tra]' in loai_raw or '[Kiem tra]' in loai_raw
                is_tu_luan='[Tự luận]' in loai_raw or '[Tu luan]' in loai_raw
                is_bai_tap=not(is_video or is_ly_thuyet or is_kiem_tra)
                if is_tu_luan or is_kiem_tra: continue
                should_process=False
                status_spans=(main_link.find_all('span',class_='message-static-item') or row.find_all('span',class_='message-static-item'))
                if not status_spans:
                    status_spans=[s for s in row.find_all('span',class_='alert-warning') if s.get_text(strip=True) not in ['Hóa học','Toán','Ngữ văn','Tiếng Anh','Tin học','Lịch sử','Địa lý','Giáo dục công dân']]
                if not status_spans: should_process=True
                else:
                    for span in status_spans:
                        st=span.get_text(strip=True).lower()
                        if 'chưa' in st or 'làm tiếp' in st: should_process=True;break
                        elif ('điểm' in st and 'đúng' in st) or 'đã xem' in st: should_process=False;break
                if should_process and href not in seen_links:
                    seen_links.add(href)
                    mon=row.find('span',class_='alert');mon_text=mon.get_text(strip=True) if mon else 'Khác'
                    ten_bai=re.sub(r'\([^)]*\)','',link_text).strip()
                    status='Chưa làm'
                    if status_spans:
                        for span in status_spans:
                            st=span.get_text(strip=True)
                            if 'chưa' in st.lower() or 'làm tiếp' in st.lower(): status=st;break
                    full_url=href if href.startswith('http') else 'https://olm.vn'+href
                    assignments.append({'title':ten_bai[:60],'subject':mon_text[:20],'type':loai_raw.replace('[','').replace(']','').strip()[:15],'status':status,'url':full_url,'page':page,'is_video':is_video,'is_ly_thuyet':is_ly_thuyet,'is_bai_tap':is_bai_tap,'is_kiem_tra':is_kiem_tra,'is_tu_luan':is_tu_luan})
                    page_count+=1
            ui_badge(f'Trang {page}: {page_count} bài cần làm','success' if page_count>0 else 'warning')
        except Exception as e: ui_badge(f'Lỗi trang {page}: {e}','error')
    print()
    if assignments:
        v=sum(1 for a in assignments if a['is_video']);lt=sum(1 for a in assignments if a['is_ly_thuyet']);bt=sum(1 for a in assignments if a['is_bai_tap'])
        ui_box([f'{C.BWHITE}Tổng:{C.END}  {C.BYELLOW}{len(assignments)} bài cần làm{C.END}','',f'  🎬 Video:       {C.BLUE}{v}{C.END}',f'  📖 Lý thuyết:   {C.CYAN}{lt}{C.END}',f'  📝 Bài tập:     {C.LIME}{bt}{C.END}'],C.CYAN,title='KẾT QUẢ QUÉT')
    else: ui_badge('Không tìm thấy bài tập nào cần làm','warning')
    pause();return assignments

def display_assignments_table(assignments):
    if not assignments: return
    print();ui_divider('─',C.PURPLE);ui_center('📚  DANH SÁCH BÀI CẦN LÀM  📚',C.BPURPLE,bold=True);ui_divider('─',C.PURPLE);print()
    for idx,item in enumerate(assignments,1):
        max_t=W-4;title=(item['title'][:max_t-1]+'…' if len(item['title'])>max_t else item['title'])
        tc=C.BLUE if item['is_video'] else(C.CYAN if item['is_ly_thuyet'] else C.LIME)
        ic='🎬' if item['is_video'] else('📖' if item['is_ly_thuyet'] else '📝')
        sc=C.BRED if 'chưa' in item['status'].lower() else C.BYELLOW
        print(f'  {C.BYELLOW}[{idx}]{C.END} {ic} {tc}{item["type"]}{C.END}  {C.GRAY}{item["subject"]}{C.END}')
        print(f'  {C.WHITE}{title}{C.END}');print(f'  {sc}→ {item["status"]}{C.END}');a_thin(C.GRAY)
    print()

def _get_csrf(session,url):
    token=session.cookies.get('XSRF-TOKEN')
    if not token:
        r=session.get(url,timeout=10);m=re.search(r'<meta name="csrf-token" content="([^"]+)"',r.text)
        token=m.group(1) if m else ''
    return token

def _parse_url_ids(url):
    id_cate=None;id_courseware=None
    ic=re.search(r'[?&]i_c=(\d+)',url)
    if ic: id_courseware=ic.group(1)
    cm=re.search(r'-(\d+)(?:[?#]|$)',url)
    if cm: id_cate=cm.group(1)
    return id_cate,id_courseware

def _extract_page_params(html):
    params={}
    for key,pats in {
        'id_school':[r"id_school['\"]?\s*[=:]\s*['\"]?(\d+)",r"'id_school'\s*:\s*'(\d+)'"],
        'id_group': [r"id_group['\"]?\s*[=:]\s*['\"]?(\d+)",r"'id_group'\s*:\s*'(\d+)'"],
        'type_vip': [r"type_vip['\"]?\s*[=:]\s*['\"]?(\d+)",r"'type_vip'\s*:\s*'(\d+)'"],
        'id_grade': [r"id_grade['\"]?\s*[=:]\s*['\"]?(\d+)"],
    }.items():
        for pat in pats:
            m=re.search(pat,html)
            if m: params[key]=m.group(1);break
    return params

def _count_questions_from_html(html):
    for pat in [
        r'count_problems\s*[=:]\s*["\']?(\d+)',
        r'total_q\s*[=:]\s*["\']?(\d+)',
        r'"total"\s*:\s*"?(\d+)"?',
        r'var\s+total\s*=\s*(\d+)',
        r"'total'\s*:\s*'?(\d+)'?",
    ]:
        m=re.search(pat,html)
        if m and int(m.group(1))>0: return int(m.group(1))
    soup=BeautifulSoup(html,'html.parser')
    for cls in [['quiz-item'],['question-item'],['q-item'],['problem-item']]:
        items=soup.find_all(class_=cls[0])
        if items: return len(items)
    return 0

def extract_quiz_info(session,url,is_video=False):
    try:
        id_cate,id_courseware=_parse_url_ids(url)
        resp=session.get(url,timeout=10);html=resp.text
        page_params=_extract_page_params(html)
        if not id_courseware:
            for pat in [r'id_courseware\s*[=:]\s*["\']?(\d+)',r'data-courseware\s*=\s*["\'](\d+)["\']']:
                m=re.search(pat,html)
                if m: id_courseware=m.group(1);break
        if not id_cate:
            for pat in [r'id_cate\s*[=:]\s*["\']?(\d+)',r"'id_cate'\s*:\s*'(\d+)'",r'-(\d{8,})(?:[?#]|$)']:
                m=re.search(pat,html)
                if m: id_cate=m.group(1);break
        qscript_list=''
        for pat in [
            r'qscript_list\s*[=:]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',
            r'quiz_list\s*[=:]\s*["\'](\d{6,}(?:,\d{6,})*)["\']',
            r'"quiz_list"\s*:\s*"(\d+(?:,\d+)*)"',
            r"'quiz_list'\s*:\s*'(\d+(?:,\d+)*)'",
            r'\bvar\s+quiz_list\s*=\s*["\'](\d+(?:,\d+)+)["\']',
        ]:
            m=re.search(pat,html)
            if m: qscript_list=m.group(1);break
        if not qscript_list:
            m=re.search(r'\b(\d{9,}(?:,\d{9,})+)\b',html)
            if m: qscript_list=m.group(1)
        csrf=session.cookies.get('XSRF-TOKEN','')
        h=HEADERS.copy();h['x-csrf-token']=csrf;h['referer']=url
        try: session.post('https://olm.vn/course/tmp-script/get-script-by-ids',data={'qscript_list':qscript_list},headers=h,timeout=8)
        except: pass
        total_q=_count_questions_from_html(html)
        if total_q==0 and qscript_list:
            total_q=len([q for q in qscript_list.split(',') if q.strip()])
        return qscript_list,total_q,id_courseware,id_cate,html,page_params
    except: return None,0,None,None,'',{}

def create_data_log_for_normal(total_questions,target_score=100):
    correct_needed=(round((target_score/100)*total_questions) if target_score not in(100,0) else(total_questions if target_score==100 else 0))
    correct_needed=max(0,min(total_questions,correct_needed))
    results=random.sample([1]*correct_needed+[0]*(total_questions-correct_needed),total_questions)
    data_log=[];total_time=0
    for i,ok in enumerate(results):
        t=random.randint(10,30)+(i%5);total_time+=t
        order=[0,1,2,3];random.shuffle(order)
        ans_idx='0' if ok else str(random.randint(1,3))
        data_log.append({
            'q_params':json.dumps([json.dumps({'js':'','order':order})]),
            'a_params':json.dumps([json.dumps([ans_idx])]),
            'result':ok,'correct':ok,'wrong':0 if ok else 1,'a_index':i,'time_spent':t
        })
    return data_log,total_time,correct_needed

def _resolve_expired(session,assignment,html):
    """Nếu bài quá hạn, trả về assignment mới với URL pass_expired=1 và html mới."""
    if 'quá hạn' not in html: return assignment,html
    url=assignment['url'];sep='&' if '?' in url else '?'
    expired_url=url+sep+'pass_expired=1'
    try:
        new_html=session.get(expired_url,timeout=10).text
        return {**assignment,'url':expired_url},new_html
    except: return assignment,html

def submit_assignment(session,assignment,user_id):
    try:
        qscript_list,total_questions,id_courseware,id_cate,html,page_params=extract_quiz_info(session,assignment['url'],assignment['is_video'])

        # Xử lý bài quá hạn → retry với pass_expired=1
        if 'quá hạn' in html:
            assignment,html=_resolve_expired(session,assignment,html)
            qscript_list,total_questions,id_courseware,id_cate,html,page_params=extract_quiz_info(session,assignment['url'],assignment['is_video'])

        if assignment['is_video']:
            return handle_video_submission(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params)
        if total_questions==0: return False
        data_log,total_time,correct_needed=create_data_log_for_normal(total_questions,100)
        csrf=_get_csrf(session,assignment['url']);ct=int(time.time())
        payload={
            'id_user':user_id,'id_cate':id_cate or '0','id_grade':page_params.get('id_grade','10'),
            'id_courseware':id_courseware or '0','id_group':page_params.get('id_group','6148789559'),
            'id_school':page_params.get('id_school','0'),'time_init':str(ct-total_time),'name_user':'',
            'type_vip':page_params.get('type_vip','0'),'time_spent':str(total_time),
            'data_log':json.dumps(data_log,separators=(',',':')),'score':'100',
            'answered':str(total_questions),'correct':str(correct_needed),
            'count_problems':str(total_questions),'missed':str(total_questions-correct_needed),
            'time_stored':str(ct),'date_end':str(ct),'ended':'1','save_star':'1',
        }
        h=HEADERS.copy();h['x-csrf-token']=csrf;h['referer']=assignment['url']
        r=session.post('https://olm.vn/course/teacher-static',data=payload,headers=h,timeout=15)
        return r.status_code==200
    except: return False

def handle_video_submission(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params):
    for method in [try_video_simple_method,try_video_with_quiz,try_video_complex_method]:
        if method(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params): return True
        time.sleep(0.5)
    return False

def try_video_simple_method(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params):
    try:
        csrf=_get_csrf(session,assignment['url']);ct=int(time.time())
        data_log=[{'answer':'["0"]','params':'{"js":""}','result':[1],'wrong_skill':[],'correct_skill':[],'type':[11],'id':f'vid{random.randint(100000,999999)}','marker':1}]
        payload={'id_user':user_id,'id_cate':id_cate or '0','id_grade':page_params.get('id_grade','10'),'id_courseware':id_courseware or '0','id_group':page_params.get('id_group','6148789559'),'id_school':page_params.get('id_school','0'),'time_spent':str(random.randint(300,900)),'type_vip':page_params.get('type_vip','0'),'score':'100','data_log':json.dumps(data_log,separators=(',',':')),'date_end':str(ct),'ended':'1','save_star':'1'}
        h=HEADERS.copy();h['x-csrf-token']=csrf;h['referer']=assignment['url']
        return session.post('https://olm.vn/course/teacher-static',data=payload,headers=h,timeout=10).status_code==200
    except: return False

def try_video_with_quiz(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params):
    try:
        if not qscript_list or total_questions==0: return False
        csrf=_get_csrf(session,assignment['url']);ct=int(time.time())
        data_log=[{'answer':'["0"]','params':'{"js":""}','result':[1],'wrong_skill':[],'correct_skill':[],'type':[11],'id':f'vid{random.randint(100000,999999)}','marker':i+1} for i in range(min(total_questions,5))]
        payload={'id_user':user_id,'id_cate':id_cate or '0','id_grade':page_params.get('id_grade','10'),'id_courseware':id_courseware or '0','id_group':page_params.get('id_group','6148789559'),'id_school':page_params.get('id_school','0'),'time_spent':str(random.randint(300,900)),'type_vip':page_params.get('type_vip','0'),'score':'100','data_log':json.dumps(data_log,separators=(',',':')),'date_end':str(ct),'ended':'1','save_star':'1','correct':str(len(data_log)),'count_problems':str(len(data_log))}
        h=HEADERS.copy();h['x-csrf-token']=csrf;h['referer']=assignment['url']
        return session.post('https://olm.vn/course/teacher-static',data=payload,headers=h,timeout=10).status_code==200
    except: return False

def try_video_complex_method(session,assignment,user_id,qscript_list,total_questions,id_courseware,id_cate,html,page_params):
    try:
        csrf=_get_csrf(session,assignment['url']);ct=int(time.time());ts=random.randint(600,1200)
        data_log=[{'answer':'["0"]','params':'{"js":""}','result':[1],'wrong_skill':[],'correct_skill':[],'type':[11],'id':f'vid{random.randint(100000,999999)}','marker':1}]
        if qscript_list and total_questions>0:
            order=[0,1,2,3];random.shuffle(order)
            data_log.append({'answer':'["0"]','label':['A'],'params':json.dumps({'js':'','order':order}),'result':[1],'wrong_skill':[],'correct_skill':[],'type':[1],'id':f'q{random.randint(100000,999999)}','marker':2})
        payload={'id_user':user_id,'id_cate':id_cate or '0','id_grade':page_params.get('id_grade','10'),'id_courseware':id_courseware or '0','id_group':page_params.get('id_group','6148789559'),'id_school':page_params.get('id_school','0'),'time_init':'','name_user':'','type_vip':page_params.get('type_vip','530'),'time_spent':str(ts),'score':'100','data_log':json.dumps(data_log,separators=(',',':')),'total_time':str(ts),'current_time':'3','correct':str(len(data_log)),'totalq':'0','count_problems':str(len(data_log)),'date_end':str(ct),'ended':'1','save_star':'1'}
        h=HEADERS.copy();h['x-csrf-token']=csrf;h['referer']=assignment['url']
        return session.post('https://olm.vn/course/teacher-static',data=payload,headers=h,timeout=10).status_code==200
    except: return False

license_data=None

def _deduct_use(is_vip,remaining_uses):
    global license_data
    if not is_vip and license_data:
        remaining_uses-=1
        save_license({'key':license_data['key'],'remain':remaining_uses,'expire':license_data['expire'],'ip':license_data['ip']})
        print(f'\n  {C.GOLD}⚡  Số lượt còn lại: {C.BYELLOW}{remaining_uses}{C.END}')
    return remaining_uses

def solve_from_link(session,user_id,is_vip,remaining_uses):
    header('GIẢI BÀI TỪ LINK','Dán link bài tập OLM vào bên dưới')
    url=prompt_input('Link (https://olm.vn/…)',icon='🔗')
    if not url.startswith('https://olm.vn/'): ui_badge('Link phải là link OLM!','error');pause();return False,remaining_uses
    try:
        sp=Spinner('Đang phân tích bài…');sp.start()
        resp=session.get(url,timeout=10)
        is_video='video' in url.lower() or '[Video]' in resp.text
        is_ly_thuyet='ly-thuyet' in url.lower() or '[Lý thuyết]' in resp.text
        sp.stop(True,'Phân tích xong')
        assignment={'title':'Bài từ link','subject':'Tự chọn','type':'Video' if is_video else('Lý thuyết' if is_ly_thuyet else 'Bài tập'),'status':'Chưa làm','url':url,'page':1,'is_video':is_video,'is_ly_thuyet':is_ly_thuyet,'is_bai_tap':not(is_video or is_ly_thuyet),'is_kiem_tra':False,'is_tu_luan':False}
        url_show=url[:W-8]+'…' if len(url)>W-8 else url
        ui_box([f'  URL:  {C.WHITE}{url_show}{C.END}',f'  Loại: {C.CYAN}{assignment["type"]}{C.END}'],C.CYAN,title='THÔNG TIN BÀI')
        if prompt_input('Giải bài này? (y/n)',icon='◆').strip().lower()!='y': ui_badge('Đã hủy thao tác','warning');pause();return False,remaining_uses
        sp2=Spinner('Đang nộp bài…',C.LIME);sp2.start()
        success=submit_assignment(session,assignment,user_id)
        sp2.stop(success,'🎉 Nộp bài thành công!' if success else 'Nộp bài thất bại')
        if success: remaining_uses=_deduct_use(is_vip,remaining_uses)
        pause();return success,remaining_uses
    except Exception as e: ui_badge(f'Lỗi: {e}','error');pause();return False,remaining_uses

def solve_specific_from_list(session,user_id,is_vip,remaining_uses,assignments=None):
    if assignments is None:
        pages_input=prompt_input('Số trang quét (mặc định: 3)',icon='📄').strip()
        pages_to_scan=int(pages_input) if pages_input.isdigit() and int(pages_input)>0 else 3
        assignments=get_assignments_fixed(session,pages_to_scan)
    if not assignments: return False,remaining_uses
    header('CHỌN BÀI ĐỂ GIẢI');display_assignments_table(assignments)
    selection=prompt_input('Chọn bài (0=tất cả, hoặc 1,2,3…)',icon='◆').strip()
    if selection=='0': indices=list(range(len(assignments)))
    else:
        indices=[]
        for part in selection.split(','):
            p=part.strip()
            if p.isdigit():
                idx=int(p)-1
                if 0<=idx<len(assignments): indices.append(idx)
        if not indices: ui_badge('Lựa chọn không hợp lệ','error');pause();return False,remaining_uses
    total=len(indices);success_count=0;print()
    for i,assignment_idx in enumerate(indices,1):
        assignment=assignments[assignment_idx];title=assignment['title'][:W-14]
        ui_thin(C.GRAY);print(f'  {C.BYELLOW}[{i}/{total}]{C.END}  {C.WHITE}{title}{C.END}')
        if not is_vip and remaining_uses<=0: ui_badge('Hết lượt! Vui lòng lấy key mới.','error');break
        sp=Spinner('Đang xử lý…',C.CYAN);sp.start()
        success=submit_assignment(session,assignment,user_id)
        sp.stop(success,'🎉 Thành công!' if success else '✘ Thất bại')
        if success: success_count+=1;remaining_uses=_deduct_use(is_vip,remaining_uses)
        if i<total: print(f'  {C.GRAY}⏸  Chờ 1s…{C.END}');time.sleep(1)
    print()
    ui_box([f'Đã xử lý:   {C.BYELLOW}{total} bài{C.END}',f'{C.BGREEN}Thành công: {C.BYELLOW}{success_count} bài{C.END}',f'{C.BRED}Thất bại:   {C.BYELLOW}{total-success_count} bài{C.END}'],C.CYAN,title='KẾT QUẢ')
    pause();return success_count>0,remaining_uses

def print_tutorial():
    header('HƯỚNG DẪN SỬ DỤNG','Đọc kỹ trước khi sử dụng')
    sections=[
        ('👑  TÀI KHOẢN VIP',C.GOLD,['  • Kiểm tra tự động từ danh sách VIP','  • Không giới hạn lượt sử dụng']),
        ('🆓  TÀI KHOẢN FREE',C.CYAN,['  • Lần đầu: 1 lượt thử miễn phí','  • Mỗi key: 5 lượt/ngày','  • Hết lượt: vào lại tool và lấy key mới','  • Đổi IP: cần lấy key mới']),
        ('📝  LÀM BÀI TẬP',C.LIME,['  • Chọn 0 để giải tất cả bài','  • Chọn 1,2,3 để giải nhiều bài cụ thể']),
        ('⚠️   LỖI THƯỜNG GẶP',C.YELLOW,['  • Lỗi 403: Bài đã được nộp trước đó','  • Lỗi link: Thử lại hoặc đổi IP']),
    ]
    for title,color,lines in sections:
        print(f'\n  {color}{C.BOLD}{title}{C.END}');ui_thin(color)
        for line in lines: print(f'  {C.WHITE}{line}{C.END}')
    print();ui_divider();pause()

def main_menu(session,user_id,user_name,is_vip,remaining_uses):
    global license_data
    while True:
        header('MENU CHÍNH')
        name_d=user_name[:W-22] if len(user_name)>W-22 else user_name
        ui_thin(C.GRAY)
        if is_vip: print(f'  {C.GOLD}👑 VIP{C.END}  {C.BWHITE}{name_d}{C.END}  {C.LIME}✦ Không giới hạn{C.END}')
        else:
            bw=max(8,W-len(name_d)-16);bar=progress_bar(min(remaining_uses*20,100),bw)
            print(f'  {C.BCYAN}👤{C.END}  {C.BWHITE}{name_d}{C.END}  {bar}  {C.BYELLOW}{remaining_uses}/5{C.END}')
        ui_thin(C.GRAY);print()
        if not is_vip and remaining_uses<=0:
            print(f'  {C.BRED}⚡ Hết lượt sử dụng!{C.END}  {C.GRAY}Vui lòng lấy key mới{C.END}\n')
            new_lic=handle_key_generation()
            if new_lic:
                save_license(new_lic);license_data=new_lic
                ui_badge(f'Đăng ký thành công! Còn {new_lic["remain"]} lượt','success')
                remaining_uses=new_lic['remain']
            else: ui_badge('Không thể đăng ký key','error');return False,remaining_uses
        choice=menu_select('LỰA CHỌN CHỨC NĂNG',{'1':'🚀  Tự động hoàn thành bài tập','2':'🔗  Giải bài từ link OLM','3':'↩️   Đăng xuất','4':'🚪  Thoát chương trình','5':'❓  Hướng dẫn sử dụng'})
        if choice=='1':
            pages_input=prompt_input('Số trang quét (mặc định: 3)',icon='📄').strip()
            pages=int(pages_input) if pages_input.isdigit() and int(pages_input)>0 else 3
            assignments=get_assignments_fixed(session,pages)
            if assignments: _,remaining_uses=solve_specific_from_list(session,user_id,is_vip,remaining_uses,assignments)
        elif choice=='2': _,remaining_uses=solve_from_link(session,user_id,is_vip,remaining_uses)
        elif choice=='3':
            sp=Spinner('Đang đăng xuất…',C.YELLOW);sp.start()
            time.sleep(1);sp.stop(True,'Đã đăng xuất');pause();return False,remaining_uses
        elif choice=='4': print();ui_center('Cảm ơn bạn đã sử dụng OLM Master! 👋',C.BCYAN);print();time.sleep(0.5);sys.exit(0)
        elif choice=='5': print_tutorial()
        else: ui_badge('Lựa chọn không hợp lệ!','error');time.sleep(0.5)
    return True,remaining_uses

def main():
    global license_data
    clr();print()
    a_divider('━',C.BCYAN);a_center('⚡  OLM MASTER  ⚡',C.GOLD,bold=True)
    a_center('AUTO SOLVER  ·  v3.2',C.BCYAN);a_center('bởi Tuấn Anh',C.GRAY);a_divider('━',C.BCYAN)
    print();time.sleep(0.3)
    print_tutorial()
    while True:
        session,user_id,user_name,actual_username=login_olm()
        if not(session and user_id and user_name):
            if prompt_input('Thử lại? (y/n)',icon='◆').strip().lower()!='y': ui_badge('Tạm biệt! 👋','info');time.sleep(0.5);break
            continue
        sp=Spinner('Đang kiểm tra quyền hạn…',C.GOLD);sp.start()
        is_vip=check_vip(actual_username);sp.stop(True,'Quyền hạn đã xác nhận')
        if is_vip:
            ui_vip_card(actual_username,user_name);pause('  ↵ Nhấn Enter để vào menu chính…')
            main_menu(session,user_id,user_name,True,float('inf'))
        else:
            license_data=load_license();today=datetime.now().strftime('%Y-%m-%d');current_ip=get_public_ip()
            if(license_data and license_data.get('expire')==today and license_data.get('ip')==current_ip and license_data.get('remain',0)>0):
                remaining_uses=license_data['remain']
                ui_badge(f'Tài khoản FREE — Còn {remaining_uses} lượt','info')
                pause('  ↵ Nhấn Enter để vào menu chính…')
            elif not is_trial_used():
                ui_badge('Chào mừng lần đầu! Bạn có 1 lượt thử miễn phí.','info');print()
                mark_trial_used()
                trial_lic={'key':'TRIAL','remain':1,'expire':today,'ip':current_ip}
                save_license(trial_lic);license_data=trial_lic;remaining_uses=1
                pause('  ↵ Nhấn Enter để vào menu chính…')
            else:
                ui_badge('Tài khoản FREE — Vui lòng lấy key mới','warning')
                new_lic=handle_key_generation()
                if new_lic:
                    save_license(new_lic);license_data=new_lic;remaining_uses=new_lic['remain']
                    ui_badge(f'Đăng ký thành công! Còn {remaining_uses} lượt','success')
                    pause('  ↵ Nhấn Enter để vào menu chính…')
                else: ui_badge('Không thể đăng ký key','error');pause();continue
            _,remaining_uses=main_menu(session,user_id,user_name,False,remaining_uses)

if __name__=='__main__':
    try: main()
    except KeyboardInterrupt:
        show_cursor();print(f'\n\n  {C.YELLOW}Đã dừng chương trình.{C.END}\n');sys.exit(0)
    except Exception as e:
        show_cursor();print(f'\n  {C.BRED}Lỗi không mong muốn:{C.END} {e}\n');pause()
