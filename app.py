"""AasPaas landing page (Streamlit).

Run locally:  streamlit run app.py
Deploy:       push this whole folder (including .streamlit/ and assets/) to GitHub,
              then create an app on share.streamlit.io with app.py as the main file.

Interest forms are delivered to CONTACT_EMAIL through FormSubmit (formsubmit.co).
The first submission triggers a one-time activation email to that address;
click the link in it, and every later submission arrives in the inbox.
"""

import base64
from pathlib import Path

import requests
import streamlit as st

CONTACT_EMAIL = "ahmedlodhi@uchicago.edu"
FORM_ENDPOINT = f"https://formsubmit.co/ajax/{CONTACT_EMAIL}"
ASSETS = Path(__file__).parent / "assets"

st.set_page_config(
    page_title="AasPaas | Your neighbourhood, connected",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def html(block: str) -> None:
    """Render raw HTML. Lines are stripped so Markdown never reads indentation as code."""
    lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


@st.cache_data
def img(name: str) -> str:
    data = (ASSETS / name).read_bytes()
    return "data:image/jpeg;base64," + base64.b64encode(data).decode()


def send_interest(subject: str, fields: dict) -> bool:
    payload = {"_subject": subject, "_template": "table", "_captcha": "false", **fields}
    try:
        r = requests.post(FORM_ENDPOINT, json=payload, headers={"Accept": "application/json"}, timeout=12)
        return r.status_code == 200
    except requests.RequestException:
        return False


# ---------------------------------------------------------------------------
# Styles: palette matches the pitch slides
# ---------------------------------------------------------------------------
html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Noto+Nastaliq+Urdu:wght@500&display=swap');

:root {
  --forest: #143F39;
  --shutter: #1E5B52;
  --gold: #E2A43A;
  --paper: #F4F7F3;
  --sage: #E3ECE6;
  --ink: #16231F;
  --muted: #4E5F59;
  --rule: #D3DED8;
}

#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stToolbar"] { display: none !important; }
.stApp { background: var(--paper); }
.block-container { padding-top: 1.5rem !important; padding-bottom: 3rem !important; max-width: 1100px !important; }
.stApp, .stApp p, .stApp li, .stApp a, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp th, .stApp td, .stApp label, .stApp input, .stApp textarea, .stApp button {
  font-family: 'Bricolage Grotesque', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
.stApp p, .stApp li, .stApp h1, .stApp h2, .stApp h3 { color: var(--ink); }

.ap-nav { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--rule); }
.ap-brand { display: flex; align-items: baseline; gap: .6rem; }
.ap-brand .latin { font-size: 1.5rem; font-weight: 800; letter-spacing: -.02em; color: var(--shutter); }
.ap-brand .urdu { font-family: 'Noto Nastaliq Urdu', serif; font-size: 1.15rem; color: var(--shutter); line-height: 2; }
.ap-status { font-size: .9rem; color: var(--forest); background: var(--sage); border-radius: 999px; padding: .35rem .9rem; }

.ap-hero { display: grid; grid-template-columns: 1.15fr 1fr; gap: 3rem; align-items: center; padding: 3.5rem 0 3rem; }
.ap-hero h1 { font-size: clamp(2.2rem, 4.6vw, 3.6rem); line-height: 1.05; font-weight: 800; letter-spacing: -.03em; margin: 0 0 1.25rem; }
.ap-hero .lede { font-size: 1.2rem; line-height: 1.55; color: var(--muted); max-width: 34rem; margin: 0 0 1.75rem; }
.ap-ctas { display: flex; gap: .75rem; flex-wrap: wrap; }
.ap-cta { display: inline-block; background: var(--shutter); color: #fff !important; text-decoration: none !important; font-weight: 600; padding: .85rem 1.3rem; border-radius: 10px; }
.ap-cta:hover { background: var(--forest); }
.ap-cta.alt { background: var(--gold); color: #2A1E05 !important; }
.ap-cta.alt:hover { background: #CF9228; }
.ap-cta:focus-visible { outline: 3px solid var(--gold); outline-offset: 3px; }

.ap-thread { background: var(--shutter); border-radius: 22px; padding: 1.4rem 1.2rem 1.1rem; box-shadow: 0 18px 40px -18px rgba(20, 63, 57, .55); }
.ap-thread .note { color: #CFE3DC; font-size: .82rem; margin: 0 0 .9rem .2rem; }
.msg { border-radius: 14px; padding: .75rem .95rem; margin-bottom: .6rem; max-width: 88%; line-height: 1.4; font-size: .98rem; }
.msg small { display: block; font-size: .78rem; margin-bottom: .2rem; opacity: .8; }
.msg.ask { background: var(--gold); color: #2A1E05; margin-left: auto; border-bottom-right-radius: 4px; }
.msg.reply { background: #FBFCFA; color: var(--ink); border-bottom-left-radius: 4px; }
.msg.reply.no { background: #D8E6E0; color: #3D4E48; }

.ap-section { padding: 2.75rem 0; border-top: 1px solid var(--rule); }
.ap-section h2 { font-size: 1.9rem; font-weight: 800; letter-spacing: -.02em; margin: 0 0 1rem; }
.ap-section > p, .ap-section .body { font-size: 1.08rem; line-height: 1.6; color: var(--muted); max-width: 42rem; }
.ap-kicker { font-size: 1rem; color: var(--muted); margin: -.4rem 0 1.5rem; }

.ap-photo { width: 100% !important; max-width: 100% !important; height: auto !important; display: block; border-radius: 18px; object-fit: cover; }
.ap-cap { font-size: .85rem; color: #6C7C76; margin-top: .5rem; }

.ap-why { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5rem; align-items: center; }
.ap-why .big { font-size: 4rem; font-weight: 800; letter-spacing: -.04em; color: var(--shutter); line-height: 1; margin-bottom: .6rem; }
.ap-why p { font-size: 1.08rem; line-height: 1.6; color: var(--muted); margin: 0 0 .9rem; }
.ap-source { font-size: .82rem !important; color: #6C7C76 !important; }
.ap-source a { color: #6C7C76; }
.ap-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-top: 2rem; }
.ap-pair .ap-photo { aspect-ratio: 16 / 9; }

.ap-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }
.ap-step .n { display: inline-flex; width: 2.2rem; height: 2.2rem; border-radius: 50%; align-items: center; justify-content: center; font-weight: 800; background: var(--sage); color: var(--shutter); margin-bottom: .8rem; }
.ap-step h3 { font-size: 1.2rem; font-weight: 600; margin: 0 0 .4rem; }
.ap-step p { font-size: 1rem; line-height: 1.55; color: var(--muted); margin: 0; }

.ap-audience { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
.ap-card { background: #FBFCFA; border: 1px solid var(--rule); border-radius: 18px; padding: 1.5rem; display: block; }
.ap-card > * + * { margin-top: 1rem !important; }
.ap-card h3 { font-size: 1.3rem; font-weight: 600; margin: 0; color: var(--forest); }
.ap-card .promise { font-size: 1.15rem; line-height: 1.45; color: var(--ink); margin: 0; font-weight: 600; }
.ap-card ul { padding-left: 1.1rem; margin: 0; }
.ap-card li { font-size: 1rem; line-height: 1.55; color: var(--muted); margin-bottom: .4rem; }
.ap-cardimg { width: 100%; aspect-ratio: 4 / 3; border-radius: 14px; background-size: cover; background-repeat: no-repeat; }

.ap-compare { width: 100%; border-collapse: collapse; font-size: 1rem; }
.ap-compare th, .ap-compare td { text-align: left; padding: .85rem 1rem; border-bottom: 1px solid var(--rule); vertical-align: top; line-height: 1.5; }
.ap-compare th { font-weight: 600; color: var(--forest); }
.ap-compare td:first-child { color: var(--muted); width: 28%; }
.ap-compare td.us { background: var(--sage); font-weight: 600; color: var(--ink); }
.ap-table-wrap { overflow-x: auto; }

.ap-impact { display: grid; grid-template-columns: 1.1fr 1fr; gap: 2.5rem; align-items: start; }
.ap-metric { padding: 1rem 0 1rem 1.1rem; border-left: 4px solid var(--gold); margin-bottom: 1rem; }
.ap-metric h3 { font-size: 1.15rem; font-weight: 600; margin: 0 0 .3rem; }
.ap-metric p { font-size: 1rem; line-height: 1.55; color: var(--muted); margin: 0; }

.ap-status-box { background: var(--forest); border-radius: 18px; padding: 2rem; display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center; }
.ap-status-box p { color: #E3ECE6 !important; font-size: 1.05rem; line-height: 1.6; margin: 0 0 .8rem; }
.ap-status-box h3 { color: var(--gold) !important; font-size: 1.3rem; margin: 0 0 .6rem; }
.ap-founder { display: flex; align-items: center; gap: 1rem; }
.ap-founder img { width: 96px; height: 96px; border-radius: 50%; object-fit: cover; background: #fff; }
.ap-founder p { margin: 0 !important; font-size: .95rem !important; }

.ap-forms-head h2 { font-size: 1.9rem; font-weight: 800; letter-spacing: -.02em; margin: 0 0 .4rem; }
div[data-testid="stForm"] { background: #FBFCFA; border: 1px solid var(--rule); border-radius: 18px; padding: 1.25rem 1.25rem .5rem; }
.stFormSubmitButton button { background: var(--shutter) !important; color: #fff !important; border: none !important; font-weight: 600 !important; }
.stFormSubmitButton button:hover { background: var(--forest) !important; }
.stFormSubmitButton button p { color: #FFFFFF !important; font-weight: 600; }
.stApp h4 { color: var(--forest) !important; font-weight: 600 !important; }

.ap-footer { padding-top: 2rem; margin-top: 2rem; border-top: 1px solid var(--rule); font-size: .9rem; color: #6C7C76; line-height: 1.6; }
.ap-footer a { color: var(--shutter); }

@media (max-width: 820px) {
  .ap-hero, .ap-why, .ap-pair, .ap-audience, .ap-impact, .ap-status-box { grid-template-columns: 1fr; gap: 1.75rem; }
  .ap-hero { padding-top: 2rem; }
  .ap-steps { grid-template-columns: 1fr; gap: 1.5rem; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
"""
)

# ---------------------------------------------------------------------------
# Nav
# ---------------------------------------------------------------------------
html(
    """
<nav class="ap-nav">
  <div class="ap-brand"><span class="latin">AasPaas</span><span class="urdu" lang="ur">آس پاس</span></div>
  <span class="ap-status">Pilot in development, Karachi</span>
</nav>
"""
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
html(
    """
<section class="ap-hero">
  <div>
    <h1>When your shop doesn't have it, the shop next door might.</h1>
    <p class="lede">AasPaas is a planned service that will send your request to the independent shops around you,
    so the ones that have the item can reply. Shopkeepers will answer on the phone they already use:
    no catalogue to upload, no software to learn.</p>
    <div class="ap-ctas">
      <a class="ap-cta" href="#join-shops">I run a shop</a>
      <a class="ap-cta alt" href="#join-customers">I'd like to try it</a>
    </div>
  </div>
  <div class="ap-thread" aria-label="Illustration of how a request is planned to work">
    <p class="note">Illustration of the planned service, not a live product</p>
    <div class="msg ask"><small>You</small>Does anyone nearby have wheat baby cereal, the 175g box?</div>
    <div class="msg reply no"><small>Your usual shop, 100 m</small>Not today, maybe next week.</div>
    <div class="msg reply"><small>Madina General Store, 350 m</small>Yes, two boxes. Can send it in 20 minutes.</div>
    <div class="msg reply"><small>Al-Noor Kiryana, 600 m</small>Yes, ready for pickup.</div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# Why neighbourhood shops (with photos)
# ---------------------------------------------------------------------------
html(
    f"""
<section class="ap-section">
  <h2>Why neighbourhood shops</h2>
  <div class="ap-why">
    <div>
      <div class="big">~90%</div>
      <p>Industry estimates suggest that nearly 90% of grocery shopping in Pakistan still happens at neighbourhood
      kiryana stores. They are where people buy on credit, send a child for bread, and know the shopkeeper by name.</p>
      <p class="ap-source">Industry estimate reported in
      <a href="https://tribune.com.pk/story/2578568/gen-z-digitisation-drive-q-commerce" target="_blank" rel="noopener">The Express Tribune</a>.</p>
    </div>
    <img class="ap-photo" style="aspect-ratio: 4 / 5;" src="{img('community.jpg')}" alt="Neighbours talking at the counter of a green-shuttered kiryana in Karachi">
  </div>
  <div class="ap-pair">
    <div>
      <img class="ap-photo" src="{img('supermarket.jpg')}" alt="A large new supermarket across the road from a small kiryana with no customers">
      <p class="ap-cap">Large supermarkets are opening across Karachi.</p>
    </div>
    <div>
      <img class="ap-photo" src="{img('delivery-app.jpg')}" alt="A kiryana with its shutter half down as a delivery rider passes">
      <p class="ap-cap">Many of the delivery apps growing in Pakistan sell from their own warehouses rather than from local shops.</p>
    </div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# How it will work
# ---------------------------------------------------------------------------
html(
    """
<section class="ap-section">
  <h2>How it will work</h2>
  <p class="ap-kicker">This is the proposed design. Our Karachi pilot will test each step before we build an app.</p>
  <div class="ap-steps">
    <div class="ap-step"><span class="n">1</span><h3>Ask once</h3>
      <p>You send one message saying what you need, as text or a voice note in Urdu.</p></div>
    <div class="ap-step"><span class="n">2</span><h3>Nearby shops answer</h3>
      <p>Independent shops within walking distance see the request and reply only if they have it.</p></div>
    <div class="ap-step"><span class="n">3</span><h3>Pick up or get it sent</h3>
      <p>You choose a shop, then collect the item or have the shop send it over.</p></div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# Who it's for
# ---------------------------------------------------------------------------
html(
    f"""
<section class="ap-section">
  <h2>Who it's for</h2>
  <div class="ap-audience">
    <div class="ap-card">
      <div class="ap-cardimg" role="img" aria-label="A mother with her toddler asking a shopkeeper for an item he does not have" style="background-image:url('{img('out-of-stock.jpg')}'); background-position: center 30%;"></div>
      <h3>Households</h3>
      <p class="promise">Find a product nearby when your regular shop doesn't have it.</p>
      <ul>
        <li>One message instead of walking from shop to shop.</li>
        <li>Keep buying from people in your own area.</li>
      </ul>
    </div>
    <div class="ap-card">
      <div class="ap-cardimg" role="img" aria-label="A smiling shopkeeper reading a message on his phone at his counter" style="background-image:url('{img('shopkeeper.jpg')}'); background-position: center 25%;"></div>
      <h3>Shopkeepers</h3>
      <p class="promise">Reach new customers without expensive software or inventory systems.</p>
      <ul>
        <li>Hear from nearby customers who would not otherwise have walked in.</li>
        <li>Reply only when you have the item. Nothing to list, no stock to update.</li>
      </ul>
    </div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# What makes it different
# ---------------------------------------------------------------------------
html(
    """
<section class="ap-section">
  <h2>What makes AasPaas different</h2>
  <p class="ap-kicker">AasPaas focuses on the moment your usual shop can't help, and sends that demand to other shops on your street.</p>
  <div class="ap-table-wrap">
    <table class="ap-compare">
      <tr><th></th><th>Typical delivery app</th><th>AasPaas (planned)</th></tr>
      <tr><td>Where the order goes</td><td>Often the app's own warehouse or a large retailer</td><td class="us">Independent shops in your neighbourhood</td></tr>
      <tr><td>What a shop needs</td><td>A product catalogue, an app and stock updates</td><td class="us">The phone it already uses</td></tr>
      <tr><td>Best for</td><td>A full grocery basket delivered fast</td><td class="us">The one item your regular shop is out of</td></tr>
    </table>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# Measuring impact
# ---------------------------------------------------------------------------
html(
    f"""
<section class="ap-section">
  <h2>How we'll measure impact</h2>
  <p class="ap-kicker">Our goal is measurable new business for small retailers and stronger neighbourhood economies. In the pilot we plan to track:</p>
  <div class="ap-impact">
    <div>
      <div class="ap-metric"><h3>Requests fulfilled</h3>
        <p>The share of household requests that a nearby independent shop is able to fill.</p></div>
      <div class="ap-metric"><h3>New customer connections</h3>
        <p>How many households buy from a participating shop for the first time through AasPaas.</p></div>
      <div class="ap-metric"><h3>Incremental sales</h3>
        <p>Sales that would not have happened otherwise. Shops will join in phases, so shops still waiting to join
        act as a comparison for shops already taking part.</p></div>
    </div>
    <div>
      <img class="ap-photo" style="aspect-ratio: 4 / 3;" src="{img('outcome.jpg')}" alt="A teenage boy from a local shop hands groceries to an elderly woman at her door">
      <p class="ap-cap">The outcome we're working toward: neighbourhood demand served by neighbourhood shops.</p>
    </div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# Where we are + founder
# ---------------------------------------------------------------------------
html(
    f"""
<section class="ap-section">
  <div class="ap-status-box">
    <div>
      <h3>Where we are</h3>
      <p>AasPaas is an early-stage venture. Our next step is to talk with shopkeepers and households in Karachi
      and run a small manual pilot with 10 to 15 shops in one neighbourhood, before building any app.</p>
      <div class="ap-founder">
        <img src="{img('ahmed.jpg')}" alt="Ahmed Raza Khan Lodhi">
        <p>Founded by <b>Ahmed Raza Khan Lodhi</b>, formerly seven years at the State Bank of Pakistan,
        now at the University of Chicago.</p>
      </div>
    </div>
  </div>
</section>
"""
)

# ---------------------------------------------------------------------------
# Interest forms
# ---------------------------------------------------------------------------
html(
    """
<div class="ap-section ap-forms-head">
  <h2>Join the Karachi pilot</h2>
  <p class="ap-kicker">We'll only use these details to contact you about the pilot.</p>
</div>
"""
)

col_shop, col_cust = st.columns(2, gap="large")

with col_shop:
    html('<span id="join-shops"></span>')
    st.markdown("#### For shopkeepers")
    with st.form("shopkeeper_form", clear_on_submit=True):
        shop_name = st.text_input("Shop name")
        owner = st.text_input("Your name")
        area = st.text_input("Area in Karachi", placeholder="e.g. Gulshan-e-Iqbal Block 13")
        phone = st.text_input("WhatsApp or phone number")
        willing = st.radio(
            "Would you reply to requests from nearby customers on WhatsApp?",
            ["Yes", "Maybe, I'd like to know more", "No"],
            index=1,
        )
        sent_shop = st.form_submit_button("Register my shop's interest")
    if sent_shop:
        if not (shop_name.strip() and area.strip() and phone.strip()):
            st.error("Add your shop name, area and a phone number so we can reach you.")
        elif send_interest(
            "AasPaas: shopkeeper interest",
            {"Shop name": shop_name, "Owner": owner, "Area": area, "Phone": phone, "Would reply on WhatsApp": willing},
        ):
            st.success("Thank you. We'll contact you about the pilot.")
        else:
            st.error(f"The form couldn't be sent. Please email {CONTACT_EMAIL} instead.")

with col_cust:
    html('<span id="join-customers"></span>')
    st.markdown("#### For households")
    with st.form("customer_form", clear_on_submit=True):
        name = st.text_input("Your name")
        c_area = st.text_input("Area in Karachi", placeholder="e.g. North Nazimabad Block H")
        contact = st.text_input("WhatsApp number or email")
        missing = st.text_area("What did you last struggle to find at your usual shop?", height=100)
        sent_cust = st.form_submit_button("Sign up to try AasPaas")
    if sent_cust:
        if not (name.strip() and c_area.strip() and contact.strip()):
            st.error("Add your name, area and a way to reach you.")
        elif send_interest(
            "AasPaas: household interest",
            {"Name": name, "Area": c_area, "Contact": contact, "Hard to find item": missing},
        ):
            st.success("Thank you. We'll be in touch when the pilot starts in your area.")
        else:
            st.error(f"The form couldn't be sent. Please email {CONTACT_EMAIL} instead.")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
html(
    f"""
<div class="ap-footer">
  Researchers, partners and anyone interested in neighbourhood retail can reach us at
  <a href="mailto:{CONTACT_EMAIL}?subject=AasPaas">{CONTACT_EMAIL}</a>.<br>
  Photographs on this page are AI-generated illustrations, not images of real shops or people.
</div>
"""
)
