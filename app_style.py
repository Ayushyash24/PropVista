import streamlit as st


GITHUB_USERNAME = "Ayushyash24"
DEVELOPER_NAME = "Ayush Yash Dwivedi"


def apply_app_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            --brand: #176b87;
            --brand-dark: #0f4f63;
            --accent: #f4a261;
            --ink: #172026;
            --muted: #5d6b76;
            --panel: #ffffff;
            --line: #d9e3ea;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(23, 107, 135, 0.10), transparent 32rem),
                linear-gradient(180deg, #f7fbfd 0%, #edf4f7 100%);
            color: var(--ink);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f4f63 0%, #176b87 100%);
        }

        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] *,
        section[data-testid="stSidebar"] div[data-baseweb="input"] *,
        section[data-testid="stSidebar"] input,
        div[data-baseweb="popover"] *,
        div[role="listbox"] * {
            color: var(--ink) !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-baseweb="input"] > div {
            background: #ffffff !important;
            border-color: rgba(255, 255, 255, 0.45) !important;
        }

        section[data-testid="stSidebar"] svg {
            fill: var(--ink) !important;
            color: var(--ink) !important;
        }

        div[data-testid="stVerticalBlock"] > div:has(.feature-card) {
            gap: 1rem;
        }

        .hero {
            padding: 2rem 2.25rem;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: linear-gradient(135deg, #ffffff 0%, #eef8fb 100%);
            box-shadow: 0 18px 45px rgba(15, 79, 99, 0.10);
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin: 0;
            font-size: 3rem;
            line-height: 1.05;
            letter-spacing: 0;
            color: var(--brand-dark);
        }

        .hero p {
            color: var(--muted);
            font-size: 1.05rem;
            max-width: 760px;
            margin: 0.8rem 0 0;
        }

        .eyebrow {
            color: var(--brand);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.78rem;
            margin-bottom: 0.65rem;
        }

        .feature-card {
            min-height: 185px;
            padding: 1.25rem;
            border: 1px solid var(--line);
            border-radius: 12px;
            background: var(--panel);
            box-shadow: 0 12px 28px rgba(23, 107, 135, 0.08);
        }

        .feature-card h3 {
            margin: 0 0 0.6rem;
            color: var(--brand-dark);
            font-size: 1.15rem;
        }

        .feature-card p {
            color: var(--muted);
            margin: 0;
            line-height: 1.55;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 10px 24px rgba(23, 107, 135, 0.07);
        }

        .stButton > button {
            border: 0;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-dark) 100%);
            color: #ffffff;
            font-weight: 700;
            padding: 0.65rem 1.15rem;
            box-shadow: 0 10px 22px rgba(23, 107, 135, 0.22);
        }

        .stButton > button:hover {
            color: #ffffff;
            border: 0;
            transform: translateY(-1px);
        }

        h1, h2, h3 {
            color: var(--brand-dark);
            letter-spacing: 0;
        }

        hr {
            border-color: var(--line);
        }

        .stAlert {
            border-radius: 12px;
        }

        .developer-footer {
            margin: 3rem 0 0;
            padding: 1.25rem 0 0;
            border-top: 1px solid var(--line);
        }

        .developer-footer__inner {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.85rem;
            color: var(--muted);
            text-align: left;
        }

        .developer-footer__avatar {
            width: 54px;
            height: 54px;
            border-radius: 50%;
            border: 3px solid #ffffff;
            box-shadow: 0 8px 20px rgba(15, 79, 99, 0.18);
            object-fit: cover;
            background: #ffffff;
        }

        .developer-footer__label {
            margin: 0;
            font-size: 0.86rem;
            line-height: 1.25;
        }

        .developer-footer__name {
            margin: 0.15rem 0 0;
            color: var(--brand-dark);
            font-size: 1rem;
            font-weight: 800;
            line-height: 1.25;
        }

        @media (max-width: 640px) {
            .developer-footer__inner {
                text-align: center;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_hero(title: str, subtitle: str, eyebrow: str = "PropVista") -> None:
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="feature-card">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def app_footer() -> None:
    avatar_url = f"https://github.com/{GITHUB_USERNAME}.png"
    profile_url = f"https://github.com/{GITHUB_USERNAME}"

    st.markdown(
        f"""
        <footer class="developer-footer">
            <a class="developer-footer__inner" href="{profile_url}" target="_blank" rel="noopener noreferrer">
                <img
                    class="developer-footer__avatar"
                    src="{avatar_url}"
                    alt="{DEVELOPER_NAME} GitHub profile picture"
                />
                <div>
                    <p class="developer-footer__label">Developed by</p>
                    <p class="developer-footer__name">{DEVELOPER_NAME}</p>
                </div>
            </a>
        </footer>
        """,
        unsafe_allow_html=True,
    )
