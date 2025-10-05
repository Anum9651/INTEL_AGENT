# app.py  — PREMIUM HACKATHON VERSION

import os
import base64
import datetime as dt
from typing import List, Dict, Any

import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="INTEL-AGENT", layout="wide", initial_sidebar_state="expanded")
st.set_option("client.showErrorDetails", True)

# ------------------------------------------------------------------
# Session boot
# ------------------------------------------------------------------
ss = st.session_state
ss.setdefault("digest_data", None)
ss.setdefault("chat_messages", [
    {"role": "assistant", "content": "👋 Hello! I'm your AI intelligence assistant. Ask me about competitive signals, strategic insights, or next steps."}
])
ss.setdefault("competitors", [])
ss.setdefault("selected_competitors", [])
ss.setdefault("safe_disable_bg", False)
ss.setdefault("last_error", None)

# ------------------------------------------------------------------
# Helpers: error reporting
# ------------------------------------------------------------------
def show_error_box(prefix: str, err: Exception):
    ss.last_error = f"{prefix}: {type(err).__name__}: {err}"
    with st.expander("⚠️ Show error details", expanded=False):
        st.exception(err)

def _b64(path: str) -> str | None:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ------------------------------------------------------------------
# Background (IMAGE - robust)
# ------------------------------------------------------------------
def set_image_background(image_path: str, disabled: bool = False):
    try:
        if disabled:
            raise FileNotFoundError("Background disabled by user")
        data = _b64(image_path)
        if not data:
            raise FileNotFoundError(image_path)
        st.markdown(
            f"""
            <style>
              .stApp {{
                background: url(data:image/jpg;base64,{data});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
              }}
              .bg-overlay {{ 
                position: fixed; 
                inset: 0; 
                z-index: -1;
                background: radial-gradient(circle at 30% 10%, rgba(0,0,0,.45), rgba(0,0,0,.60) 45%, rgba(0,0,0,.80) 100%);
                pointer-events: none; 
              }}
              .stApp, .stMain, .block-container {{ position: relative; z-index: 0; }}
            </style>
            <div class="bg-overlay"></div>
            """,
            unsafe_allow_html=True,
        )
    except Exception:
        st.markdown(
            """
            <style>
              .stApp { background: radial-gradient(ellipse at top, #1a0f3a 0%, #0a0520 50%, #050210 100%) !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

set_image_background("assets/img_bg1.jpg", disabled=ss.safe_disable_bg)

# ------------------------------------------------------------------
# Fonts & Core CSS
# ------------------------------------------------------------------
def embed_argentum_fonts():
    fonts = [
        ("assets/fonts/Argentumblack-8MG0.ttf", 900),
        ("assets/fonts/Argentumshine-Yzpo.ttf", 600),
        ("assets/fonts/Argentumwhite-rgL7.ttf", 300),
    ]
    blobs = []
    for path, weight in fonts:
        data = _b64(path)
        if data:
            blobs.append(
                f"@font-face{{font-family:'Argentum';src:url(data:font/truetype;base64,{data}) format('truetype');font-weight:{weight};font-style:normal;font-display:swap;}}"
            )
    if blobs:
        st.markdown("<style>"+ "\n".join(blobs) +"</style>", unsafe_allow_html=True)

embed_argentum_fonts()

core_css = """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --primary:#00eaff; --accent:#a855f7; --success:#00ff88; --warning:#ffaa00; --danger:#ff4466;
  --glass-bg:rgba(10,15,30,.85); --glass-border:rgba(0,234,255,.25); --card-bg:rgba(15,20,35,.90);
  --text:#fff; --muted:#c7d0db;
}
*{box-sizing:border-box}
.stApp{color:var(--text);font-family:'Space Grotesk','Argentum',system-ui,sans-serif}
.block-container{max-width:1400px !important;padding:1.25rem 1.25rem 2rem !important}

/* === ENHANCED LOGO === */
.hero-section{text-align:center;padding:2.2rem 1.2rem .8rem;margin:-.6rem -.6rem .4rem;position:relative}
.hero-logo{width:110px;height:110px;margin:0 auto;
  background:linear-gradient(135deg,var(--primary) 0%,var(--accent) 50%,#4f46e5 100%);
  border-radius:24px;display:flex;align-items:center;justify-content:center;
  box-shadow:0 15px 50px rgba(0,234,255,.7),0 0 80px rgba(0,234,255,.4);
  border:3px solid rgba(0,234,255,.4);position:relative;overflow:hidden;
  animation:logoPulse 3s ease-in-out infinite;
  transform-style:preserve-3d}

.hero-logo::before{content:'';position:absolute;inset:-50%;
  background:linear-gradient(45deg,transparent,rgba(255,255,255,.3),transparent);
  animation:logoShine 4s linear infinite}

.hero-logo::after{content:'⚡';font-size:54px;
  filter:drop-shadow(0 0 12px rgba(255,255,255,1));
  animation:logoFloat 3s ease-in-out infinite}

@keyframes logoPulse{
  0%, 100%{box-shadow:0 15px 50px rgba(0,234,255,.7),0 0 80px rgba(0,234,255,.4);transform:scale(1)}
  50%{box-shadow:0 20px 70px rgba(0,234,255,1),0 0 120px rgba(0,234,255,.6);transform:scale(1.03)}
}

@keyframes logoShine{
  0%{transform:translateX(-100%) translateY(-100%) rotate(45deg)}
  100%{transform:translateX(100%) translateY(100%) rotate(45deg)}
}

@keyframes logoFloat{
  0%, 100%{transform:translateY(0) rotate(-5deg)}
  50%{transform:translateY(-5px) rotate(5deg)}
}

.hero-subtitle{color:var(--muted);max-width:760px;margin:0 auto .4rem;font-size:1.05rem}

/* === SECTION TITLES WITH GLOW === */
.section-title{font-family:'Orbitron',sans-serif;font-size:1.2rem;font-weight:800;margin:.7rem 0 1rem;
  padding:.6rem 0 .6rem 1.2rem;border-left:5px solid var(--primary);color:var(--primary);
  text-shadow:0 0 25px rgba(0,234,255,.7);position:relative;overflow:hidden}

.section-title::before{content:'';position:absolute;left:0;top:0;bottom:0;width:5px;
  background:linear-gradient(180deg,var(--primary),var(--accent));
  box-shadow:0 0 20px rgba(0,234,255,.8);animation:sectionGlow 2s ease-in-out infinite}

@keyframes sectionGlow{
  0%,100%{opacity:1;box-shadow:0 0 20px rgba(0,234,255,.8)}
  50%{opacity:.7;box-shadow:0 0 30px rgba(0,234,255,1)}
}

/* === PREMIUM CARDS WITH SHIMMER === */
.glass-card{
  background:var(--card-bg);
  backdrop-filter:blur(24px) saturate(170%);
  border:1px solid var(--glass-border);
  border-radius:16px;
  padding:20px 22px;
  margin:.8rem 0;
  box-shadow:0 10px 40px rgba(0,0,0,.65),0 0 60px rgba(0,234,255,.08);
  transition:all .4s cubic-bezier(0.4,0,0.2,1);
  position:relative;
  overflow:hidden;
}

.glass-card::before{
  content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(0,234,255,.08),transparent);
  transition:left .6s;pointer-events:none;
}

.glass-card:hover::before{left:100%}

.glass-card:hover{
  transform:translateY(-4px);
  box-shadow:0 20px 60px rgba(0,0,0,.8),0 0 80px rgba(0,234,255,.2),0 0 0 1px rgba(0,234,255,.3) inset;
  border-color:rgba(0,234,255,.4);
}

.card-header{display:flex;justify-content:space-between;gap:10px;margin-bottom:.5rem;align-items:center}
.card-title{font-weight:800;font-size:1.1rem;color:var(--primary)}

/* === PULSING BADGES === */
.card-badge{padding:6px 14px;border-radius:999px;border:1px solid rgba(0,234,255,.5);color:var(--primary);
  background:rgba(0,234,255,.18);font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;
  box-shadow:0 0 20px rgba(0,234,255,.3);animation:badgePulse 3s ease-in-out infinite}

@keyframes badgePulse{
  0%,100%{box-shadow:0 0 20px rgba(0,234,255,.3);transform:scale(1)}
  50%{box-shadow:0 0 30px rgba(0,234,255,.5);transform:scale(1.02)}
}

.card-badge.warning{color:var(--warning);border-color:rgba(255,170,0,.5);background:rgba(255,170,0,.18);
  box-shadow:0 0 20px rgba(255,170,0,.3)}
.card-badge.success{color:var(--success);border-color:rgba(0,255,136,.5);background:rgba(0,255,136,.18);
  box-shadow:0 0 20px rgba(0,255,136,.3)}
.card-badge.danger{color:var(--danger);border-color:rgba(255,68,102,.5);background:rgba(255,68,102,.18);
  box-shadow:0 0 20px rgba(255,68,102,.3)}

.meta-tags{display:flex;gap:8px;flex-wrap:wrap;margin:.2rem 0 .5rem}
.meta-tag{
  padding:7px 12px;
  border-radius:8px;
  border:1px solid rgba(255,255,255,.15);
  color:#cbd5e1;
  background:rgba(30,35,50,.8);
  font-size:12px;
  font-weight:500;
  backdrop-filter:blur(10px);
}

.card-content{
  margin:.5rem 0;
  line-height:1.7;
  color:rgba(255,255,255,.92);
  background:rgba(20,25,40,.6);
  padding:12px 14px;
  border-radius:10px;
  border:1px solid rgba(255,255,255,.08);
}

.insight-box{
  margin-top:.6rem;
  padding:12px 14px;
  background:rgba(0,234,255,.12);
  border-left:4px solid var(--primary);
  border-radius:9px;
  line-height:1.6;
  box-shadow:0 4px 15px rgba(0,234,255,.15);
}

.insight-box strong{
  color:var(--primary);
  text-shadow:0 0 10px rgba(0,234,255,.6);
}

/* === COMPETITION CARDS WITH BOTTOM LINE === */
.comp-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:1rem 0}
.comp-card{background:rgba(12,16,28,.9);border:1px solid rgba(0,234,255,.25);border-radius:14px;padding:16px 18px;
  transition:all .4s cubic-bezier(0.4,0,0.2,1);backdrop-filter:blur(10px);
  box-shadow:0 4px 20px rgba(0,0,0,.5);position:relative;overflow:hidden}

.comp-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--primary),transparent);
  transform:scaleX(0);transition:transform .4s}

.comp-card:hover::after{transform:scaleX(1)}

.comp-card:hover{transform:translateY(-3px);box-shadow:0 12px 35px rgba(0,234,255,.3);border-color:rgba(0,234,255,.5)}

.comp-line{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:#cbd5e1;margin:.3rem 0}
.comp-bad{padding:3px 10px;border-radius:999px;font-weight:800;border:1px solid rgba(255,255,255,.15);font-size:11px}
.comp-bad.low{color:#10b981;border-color:#10b98166;background:rgba(16,185,129,.1)}
.comp-bad.med{color:#f59e0b;border-color:#f59e0b66;background:rgba(245,158,11,.1)}
.comp-bad.high{color:#ef4444;border-color:#ef444466;background:rgba(239,68,68,.1)}
.comp-bad.crit{color:#fb7185;border-color:#fb718566;background:rgba(251,113,133,.1)}

/* === ADVANCED BUTTONS === */
.stButton>button{
  width:100%;
  padding:13px 18px;
  border-radius:12px;
  color:#00eaff;
  background:linear-gradient(135deg,rgba(0,234,255,.08) 0%,rgba(79,70,229,.08) 100%);
  border:2px solid rgba(0,234,255,.3);
  font-weight:800;
  letter-spacing:.08em;
  text-transform:uppercase;
  transition:all .4s cubic-bezier(0.4,0,0.2,1);
  text-shadow:0 0 15px rgba(0,234,255,.6);
  position:relative;
  overflow:hidden;
  box-shadow:0 4px 15px rgba(0,234,255,.2);
}

.stButton>button::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(0,234,255,.2),rgba(79,70,229,.2));
  opacity:0;transition:opacity .4s;
}

.stButton>button:hover::before{opacity:1}

.stButton>button:hover{
  transform:translateY(-3px) scale(1.01);
  border-color:rgba(0,234,255,.8);
  background:linear-gradient(135deg,rgba(0,234,255,.15) 0%,rgba(79,70,229,.15) 100%);
  box-shadow:0 10px 40px rgba(0,234,255,.5),0 0 60px rgba(0,234,255,.3);
  color:#fff;
  text-shadow:0 0 20px rgba(0,234,255,1);
}

.stButton>button:active{
  transform:translateY(-1px) scale(0.99);
}

/* === TAB BAR STYLING === */
.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(10,15,25,.6);padding:8px;border-radius:14px;border:1px solid rgba(0,234,255,.2)}
.stTabs [data-baseweb="tab"]{
  height:auto;padding:10px 20px;border-radius:10px;color:#9fb3c8;font-weight:700;
  transition:all .3s;background:transparent;border:1px solid transparent;
  text-shadow:0 0 5px rgba(0,234,255,.3)}
.stTabs [data-baseweb="tab"]:hover{color:var(--primary);background:rgba(0,234,255,.08);
  border-color:rgba(0,234,255,.3);text-shadow:0 0 15px rgba(0,234,255,.6)}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,rgba(0,234,255,.2),rgba(79,70,229,.15)) !important;
  color:#fff !important;border:1px solid rgba(0,234,255,.5) !important;
  box-shadow:0 0 20px rgba(0,234,255,.4),0 4px 15px rgba(0,0,0,.5) !important;
  text-shadow:0 0 20px rgba(0,234,255,.8) !important}

/* links */
a{
  color:var(--primary);
  text-decoration:none;
  transition:all .2s;
}

a:hover{
  color:#fff;
  text-shadow:0 0 15px rgba(0,234,255,.8);
}

/* scrollbar */
::-webkit-scrollbar{width:10px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3)}
::-webkit-scrollbar-thumb{background:rgba(0,234,255,.4);border-radius:5px}
::-webkit-scrollbar-thumb:hover{background:rgba(0,234,255,.6)}
</style>
"""
html(core_css, height=0)

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
st.markdown(
    """
<div class="hero-section">
  <div class="hero-logo"></div>
  <h1 style="font-family:'Argentum','Orbitron',sans-serif !important;font-size:clamp(2rem,5.5vw,3.8rem);font-weight:900 !important;letter-spacing:.14em;margin:.6rem 0;color:#fff;text-shadow:0 0 10px rgba(255,255,255,.8),0 0 20px rgba(0,234,255,.8),0 0 30px rgba(0,234,255,.6),0 0 40px rgba(0,234,255,.5),0 0 60px rgba(0,234,255,.4),2px 2px 4px rgba(0,0,0,.8);animation:titleGlow 3s ease-in-out infinite alternate">INTEL-AGENT</h1>
  <p class="hero-subtitle">AI-Powered Competitive Intelligence Platform — turn data into actionable strategy.</p>
</div>
<style>
@keyframes titleGlow{
  0%{text-shadow:0 0 10px rgba(255,255,255,.8),0 0 20px rgba(0,234,255,.8),0 0 30px rgba(0,234,255,.6),0 0 40px rgba(0,234,255,.5),2px 2px 4px rgba(0,0,0,.8)}
  100%{text-shadow:0 0 15px rgba(255,255,255,1),0 0 30px rgba(0,234,255,1),0 0 45px rgba(0,234,255,.8),0 0 60px rgba(0,234,255,.6),0 0 80px rgba(0,234,255,.5),2px 2px 4px rgba(0,0,0,.8)}
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Control Center")
    st.toggle("Disable Background", key="safe_disable_bg", help="Enable if the background hides content on your machine.")
    company = st.text_input("🏢 Company", "Acme CRM", key="sb_company")
    industry = st.selectbox("🏷️ Industry",
                            ["CRM", "DevTools", "E-commerce", "Fintech", "Design Tools", "Marketing Automation"],
                            index=0, key="sb_industry")
    rss_url = st.text_input("📡 Sample RSS (manual)", "https://vercel.com/changelog/rss.xml", key="sb_rss")
    gh_repo = st.text_input("🔗 Sample GitHub", "https://github.com/vercel/vercel", key="sb_gh")
    demo_mode = st.toggle("🎭 Demo Mode", value=False, key="sb_demo")
    try:
        from services.storage import get_events, set_events, clear_events
        count = len(get_events() or [])
    except Exception as e:
        count = 0
        show_error_box("Storage import", e)
    st.metric("Intelligence Items", count)

    try:
        from utils.config import has_groq_key
        ready = has_groq_key() or demo_mode
    except Exception:
        ready = demo_mode
    st.success("🟢 Ready") if ready else st.warning("Add GROQ_API_KEY or enable Demo Mode.")

    if st.button("🗑️ Clear All Data", use_container_width=True):
        try:
            clear_events()
            ss.digest_data = None
            ss.chat_messages = [{"role": "assistant", "content": "👋 Data cleared! Ready for new intelligence."}]
            st.success("✓ Reset complete")
            st.rerun()
        except Exception as e:
            show_error_box("Clear data", e)

# ------------------------------------------------------------------
# Shared UI helpers
# ------------------------------------------------------------------
def render_glass_card(title="", badge="", badge_type="primary", meta_items=None, content="", insight="", link="#"):
    bmap = {"primary": "", "danger": "danger", "warning": "warning", "success": "success"}
    bcls = bmap.get(badge_type, "")
    meta_html = ""
    if meta_items:
        meta_html = '<div class="meta-tags">' + "".join([f'<span class="meta-tag">{m}</span>' for m in meta_items]) + "</div>"
    content_html = f'<div class="card-content">{content}</div>' if content else ""
    insight_html = f'<div class="insight-box"><strong>💡</strong> {insight}</div>' if insight else ""
    link_html = f'<a href="{link}" target="_blank" class="meta-tag">Open source →</a>' if link and link != "#" else ""
    st.markdown(
        f"""
<div class="glass-card">
  <div class="card-header">
    <div class="card-title">{title}</div>
    {f'<span class="card-badge {bcls}">{badge}</span>' if badge else ''}
  </div>
  {meta_html}
  {content_html}
  {insight_html}
  {link_html}
</div>
""",
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------------
# Built-in catalog
# ------------------------------------------------------------------
CATALOG: Dict[str, List[Dict[str, Any]]] = {
    "CRM": [
        {"name": "Salesforce", "site": "https://salesforce.com", "rss": "https://www.salesforce.com/blog/feed/"},
        {"name": "HubSpot", "site": "https://hubspot.com", "rss": "https://blog.hubspot.com/marketing/rss.xml"},
        {"name": "Zoho CRM", "site": "https://zoho.com/crm", "rss": "https://www.zoho.com/blog/feed.xml"},
        {"name": "Pipedrive", "site": "https://pipedrive.com", "rss": "https://www.pipedrive.com/en/blog/rss"},
    ],
    "DevTools": [
        {"name": "Vercel", "site": "https://vercel.com", "rss": "https://vercel.com/changelog/rss.xml", "github": "https://github.com/vercel/vercel"},
        {"name": "Netlify", "site": "https://netlify.com", "rss": "https://www.netlify.com/blog/index.xml"},
        {"name": "Render", "site": "https://render.com", "rss": "https://render.com/blog/rss.xml"},
    ],
    "E-commerce": [
        {"name": "Shopify", "site": "https://shopify.com", "rss": "https://www.shopify.com/partners/blog.atom"},
        {"name": "BigCommerce", "site": "https://bigcommerce.com", "rss": "https://www.bigcommerce.com/blog/feed/"},
        {"name": "WooCommerce", "site": "https://woocommerce.com", "rss": "https://woocommerce.com/feed/"},
    ],
    "Fintech": [
        {"name": "Stripe", "site": "https://stripe.com", "rss": "https://stripe.com/blog/feed.rss"},
        {"name": "Adyen", "site": "https://www.adyen.com", "rss": "https://www.adyen.com/blog/rss.xml"},
        {"name": "Square", "site": "https://squareup.com", "rss": "https://squareup.com/us/en/press/feed"},
    ],
    "Design Tools": [
        {"name": "Figma", "site": "https://figma.com", "rss": "https://www.figma.com/blog/feed.xml"},
        {"name": "Sketch", "site": "https://www.sketch.com", "rss": "https://www.sketch.com/feed.xml"},
        {"name": "Adobe XD", "site": "https://www.adobe.com/products/xd.html", "rss": ""},
    ],
    "Marketing Automation": [
        {"name": "Mailchimp", "site": "https://mailchimp.com", "rss": "https://mailchimp.com/resources/rss/"},
        {"name": "Klaviyo", "site": "https://www.klaviyo.com", "rss": "https://www.klaviyo.com/blog/rss.xml"},
        {"name": "ActiveCampaign", "site": "https://www.activecampaign.com", "rss": "https://www.activecampaign.com/blog/feed"},
    ],
}

def discover_competitors(industry_key: str) -> List[Dict[str, Any]]:
    base = [dict(c) for c in CATALOG.get(industry_key, [])]
    for c in base:
        c.setdefault("rss", ""); c.setdefault("github", "")
        c["selected"] = True; c["threat"] = "Medium"; c["threat_score"] = 50
    return base

def score_threats(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    try:
        import feedparser
    except Exception:
        feedparser = None
    now = dt.datetime.utcnow()
    for c in items:
        score = 20 + (25 if c.get("rss") else 0) + (15 if c.get("github") else 0)
        recent = 0
        if feedparser and c.get("rss"):
            try:
                fp = feedparser.parse(c["rss"])
                if getattr(fp, "entries", None):
                    e = fp.entries[0]
                    if getattr(e, "published_parsed", None):
                        pub = dt.datetime(*e.published_parsed[:6])
                        days = (now - pub).days
                        recent = 10 if days <= 7 else 6 if days <= 30 else 3 if days <= 90 else 0
            except Exception:
                pass
        score += recent
        if c["name"].lower() in ("salesforce","shopify","stripe","figma","vercel","hubspot","square","adyen"):
            score += 15
        elif len(c["name"]) <= 6:
            score += 5
        score = max(0, min(100, score))
        c["threat_score"] = score
        c["threat"] = "Critical" if score >= 80 else "High" if score >= 65 else "Medium" if score >= 40 else "Low"
    return items

def fetch_competitor_updates(company: str, industry: str, selected: List[Dict[str, Any]], demo: bool=False) -> List[Dict[str, Any]]:
    """Produce normalized events for the Live feed and digest.
    - Always return at least 1 event per selected competitor in Demo Mode.
    - Include consistent fields so storage never rejects/silently drops."""
    events: List[Dict[str, Any]] = []
    try:
        import feedparser  # optional
    except Exception:
        feedparser = None

    now_iso = dt.datetime.utcnow().isoformat() + "Z"

    for c in selected:
        # Real RSS if available + not demo
        if not demo and feedparser and c.get("rss"):
            try:
                feed = feedparser.parse(c["rss"])
                for e in (getattr(feed, "entries", []) or [])[:3]:
                    title = getattr(e, "title", "Update")
                    link  = getattr(e, "link", c.get("site", "#"))
                    summary = (getattr(e, "summary", "") or "").strip()
                    events.append({
                        "company": company,
                        "competitor": c["name"],
                        "industry": industry,
                        "source_type": "rss",
                        "source_url": link,
                        "title": f"{c['name']}: {title}",
                        "raw": summary or title,
                        "summary": "",
                        "category": "Features",
                        "impact": 3,            # default; classifier can update later
                        "confidence": 70,       # %
                        "published_at": now_iso
                    })
            except Exception:
                # fail soft—continue into demo record if demo=True
                pass

        # Guaranteed demo record (and fallback if feedparser missing)
        if demo or not feedparser or not c.get("rss"):
            events.append({
                "company": company,
                "competitor": c["name"],
                "industry": industry,
                "source_type": "demo",
                "source_url": c.get("site", "#"),
                "title": f"{c['name']} announces new {industry} capabilities",
                "raw": f"Demo intel: {c['name']} shipped automation & AI enhancements for {industry}.",
                "summary": "",
                "category": "Launch",
                "impact": 3,
                "confidence": 80,
                "published_at": now_iso
            })

    return events


# ------------------------------------------------------------------
# Main tabs
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Discovery", "📊 Intelligence Digest", "💬 AI Chat", "⚡ Live Monitoring"])

# ------------------------------------------------------------------
# TAB 1: Discovery
# ------------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">🔍 Competitor Discovery</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Auto-Discover Competitors", use_container_width=True):
        with st.spinner("Scanning competitive landscape..."):
            try:
                ss.competitors = discover_competitors(industry)
                ss.competitors = score_threats(ss.competitors)
                st.success(f"✓ Found {len(ss.competitors)} competitors in {industry}")
                st.rerun()
            except Exception as e:
                show_error_box("Discovery", e)
    
    if ss.competitors:
        st.markdown('<div class="section-title">⚔️ Threat Assessment</div>', unsafe_allow_html=True)
        st.markdown('<div class="comp-grid">', unsafe_allow_html=True)
        
        for idx, comp in enumerate(ss.competitors):
            threat_class = {"Critical": "crit", "High": "high", "Medium": "med", "Low": "low"}.get(comp["threat"], "low")
            
            card_html = f"""
            <div class="comp-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                    <strong style="color:var(--primary);font-size:1.05rem">{comp['name']}</strong>
                    <span class="comp-bad {threat_class}">{comp['threat']}</span>
                </div>
                <div class="comp-line">
                    <span>Threat Score:</span>
                    <strong style="color:var(--primary)">{comp['threat_score']}/100</strong>
                </div>
                <div class="comp-line">
                    <span>RSS Feed:</span>
                    <span>{'✓ Active' if comp.get('rss') else '✗ None'}</span>
                </div>
                <div class="comp-line">
                    <span>GitHub:</span>
                    <span>{'✓ Tracked' if comp.get('github') else '✗ None'}</span>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Selection interface
        st.markdown('<div class="section-title">✅ Select Competitors to Monitor</div>', unsafe_allow_html=True)
        selected_names = st.multiselect(
            "Choose competitors",
            options=[c["name"] for c in ss.competitors],
            default=[c["name"] for c in ss.competitors if c.get("selected", True)],
            key="comp_selector"
        )
        ss.selected_competitors = [c for c in ss.competitors if c["name"] in selected_names]
        
        # >>> REPLACED BLOCK: Fetch Intelligence button (with diagnostics & safe save)
        # >>> FETCH INTELLIGENCE (append + diagnostics)
# >>> REPLACE the existing "📡 Fetch Intelligence" button block with this
        # --- FETCH INTELLIGENCE (append + cooldown + persistent success) ---
        if "last_fetch_ts" not in ss:
            ss.last_fetch_ts = 0.0

        import time
        now_ts = time.time()

        clicked = st.button("📡 Fetch Intelligence", use_container_width=True, disabled=not ss.selected_competitors)
        if clicked:
            # cooldown 2s to avoid double-saves on quick re-clicks
            if now_ts - ss.last_fetch_ts < 2.0:
                st.info("Hold on — just fetched a moment ago.")
            else:
                ss.last_fetch_ts = now_ts
                with st.spinner("Gathering competitive intelligence..."):
                    try:
                        events = fetch_competitor_updates(company, industry, ss.selected_competitors, demo_mode)

                        from services.storage import get_events, set_events
                        existing = get_events() or []
                        combined = existing + events

                        # Stronger de-dupe (competitor + normalized title)
                        seen = set()
                        deduped = []
                        for e in combined:
                            key = (e.get("competitor","").strip().lower(),
                                   (e.get("title","") or "").strip().lower())
                            if key in seen:
                                continue
                            seen.add(key)
                            deduped.append(e)

                        set_events(deduped)
                        new_items = max(0, len(deduped) - len(existing))
                        st.success(f"✓ Saved {new_items} new intelligence item(s). Open the ⚡ Live Monitoring tab to view.")
                    except Exception as e:
                        show_error_box("Fetch intelligence", e)


# ------------------------------------------------------------------
# TAB 2: Intelligence Digest
# ------------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">📊 Intelligence Digest</div>', unsafe_allow_html=True)
    
    if st.button("🧠 Generate AI Digest", use_container_width=True):
        with st.spinner("AI analyzing competitive landscape..."):
            try:
                from services.storage import get_events
                from services.ai import generate_digest
                
                events = get_events() or []
                if not events:
                    st.warning("No intelligence data available. Fetch updates first.")
                else:
                    digest = generate_digest(company, industry, events, demo_mode)
                    ss.digest_data = digest
                    st.success("✓ Digest generated")
                    st.rerun()
            except Exception as e:
                show_error_box("Generate digest", e)
    
    if ss.digest_data:
        digest = ss.digest_data
        
        # Executive Summary
        if digest.get("summary"):
            render_glass_card(
                title="📋 Executive Summary",
                badge="Priority",
                badge_type="primary",
                content=digest["summary"]
            )
        
        # Key Threats
        if digest.get("threats"):
            st.markdown('<div class="section-title">⚠️ Key Threats</div>', unsafe_allow_html=True)
            for threat in digest["threats"][:3]:
                render_glass_card(
                    title=threat.get("title", "Competitive Threat"),
                    badge=threat.get("severity", "Medium"),
                    badge_type="danger" if threat.get("severity") == "High" else "warning",
                    meta_items=[threat.get("competitor", "Unknown"), threat.get("category", "General")],
                    content=threat.get("description", ""),
                    insight=threat.get("impact", "")
                )
        
        # Opportunities
        if digest.get("opportunities"):
            st.markdown('<div class="section-title">💡 Strategic Opportunities</div>', unsafe_allow_html=True)
            for opp in digest["opportunities"][:3]:
                render_glass_card(
                    title=opp.get("title", "Opportunity"),
                    badge="Action",
                    badge_type="success",
                    meta_items=[opp.get("timeframe", "Q1"), opp.get("effort", "Medium")],
                    content=opp.get("description", ""),
                    insight=opp.get("rationale", "")
                )
        
        # Recommended Actions
        if digest.get("actions"):
            st.markdown('<div class="section-title">🎯 Recommended Actions</div>', unsafe_allow_html=True)
            for idx, action in enumerate(digest["actions"][:5], 1):
                st.markdown(
                    f'<div class="glass-card"><strong style="color:var(--primary)">{idx}.</strong> {action}</div>',
                    unsafe_allow_html=True
                )
    else:
        st.info("👆 Generate an AI digest to see competitive insights")

# ------------------------------------------------------------------
# TAB 3: AI Chat
# ------------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">💬 AI Intelligence Assistant</div>', unsafe_allow_html=True)
    
    # Display chat messages
    for msg in ss.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about competitors, strategies, or insights..."):
        ss.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    from services.storage import get_events
                    from services.ai import chat_query
                    
                    events = get_events() or []
                    response = chat_query(prompt, company, industry, events, demo_mode)
                    st.write(response)
                    ss.chat_messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"⚠️ Error: {str(e)}"
                    st.error(error_msg)
                    ss.chat_messages.append({"role": "assistant", "content": error_msg})

# ------------------------------------------------------------------
# TAB 4: Live Monitoring
# ------------------------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">⚡ Live Intelligence Feed</div>', unsafe_allow_html=True)
    
    try:
        from services.storage import get_events
        events = get_events() or []
        
        if events:
            for event in sorted(events, key=lambda x: x.get("published_at", ""), reverse=True)[:10]:
                render_glass_card(
                    title=event.get("title", "Intelligence Update"),
                    badge=event.get("source_type", "unknown").upper(),
                    badge_type="primary",
                    meta_items=[
                        event.get("competitor", "Unknown"),
                        event.get("published_at", "")[:10] if event.get("published_at") else "Recent"
                    ],
                    content=event.get("raw", "")[:300] + ("..." if len(event.get("raw", "")) > 300 else ""),
                    link=event.get("source_url", "#")
                )
        else:
            st.info("No intelligence data yet. Head to Discovery tab to start monitoring.")
    except Exception as e:
        show_error_box("Live monitoring", e)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;padding:2rem 0 1rem;color:var(--muted);font-size:0.85rem">
        <strong style="color:var(--primary)">INTEL-AGENT</strong> — Powered by AI Intelligence • 
        <a href="https://github.com" style="color:var(--primary)">GitHub</a> • 
        Built for Hackathons 🚀
    </div>
    """,
    unsafe_allow_html=True
)
