import streamlit as st
from groq import Groq
from groq import APIError, AuthenticationError, RateLimitError


st.set_page_config(
    page_title="Text Rewriter",
    page_icon="🩷️️️️️️",
    layout="centered",
)


st.markdown(
    """
    <style>
    :root {
        --pink: #f7c8d8;
        --pink-dark: #b85f83;
        --pink-light: #fff0f5;
        --yellow: #fff2bd;
        --green: #dcefdc;
        --ink: #51424a;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 5%, #ffe8f0 0, transparent 28%),
            radial-gradient(circle at 92% 18%, #fff4c9 0, transparent 25%),
            linear-gradient(145deg, #fff9fb 0%, #fffdf4 55%, #f5fbf3 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label, .stMarkdown {
        color: var(--ink);
    }

    .hero {
        padding: 1.5rem 1.7rem;
        border: 1px solid #f3d5df;
        border-radius: 24px;
        background: linear-gradient(120deg, #fff0f5 0%, #fff8df 58%, #eff8ed 100%);
        box-shadow: 0 8px 28px rgba(184, 95, 131, 0.08);
        margin-bottom: 1.3rem;
    }

    .hero h1 {
        margin: 0;
        color: #98506f;
        font-size: 2.35rem;
    }

    .hero p {
        margin: .55rem 0 0 0;
        color: #725d67;
        font-size: 1.03rem;
    }

    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,.88);
        border: 1px solid #eacbd7;
        border-radius: 14px;
        color: #51424a;
    }

    div[data-testid="stTextArea"] textarea:focus,
    div[data-testid="stTextInput"] input:focus {
        border-color: #d98eac;
        box-shadow: 0 0 0 1px #d98eac;
    }

    div.stButton > button {
        width: 100%;
        min-height: 3rem;
        border: 0;
        border-radius: 14px;
        color: #613e50;
        font-weight: 700;
        background: linear-gradient(90deg, #f6c7d8, #ffe9a8);
        transition: .2s ease;
    }

    div.stButton > button:hover {
        border: 0;
        color: #513546;
        background: linear-gradient(90deg, #f2b4cb, #ffe18a);
        transform: translateY(-1px);
    }

    .result-heading {
        padding: .75rem 1rem;
        margin-top: 1.2rem;
        border-radius: 14px;
        background: #eaf5e7;
        color: #527653;
        font-weight: 700;
    }

    .stAlert {
        border-radius: 14px;
    }

    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>🩷️️️️️️ Mellow Words </h1>
        <p>Перетворюй офіційні та складні тексти на просту,
        природну й невимушену розмовну мову.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Як це працює?"):
    st.write(
        "Встав текст, додай свій Groq API-ключ і натисни кнопку. "
        "Мовна модель перепише текст у розмовному стилі, збереже "
        "його основний зміст і поверне лише готовий результат."
    )

api_key = st.text_input(
    "Groq API-ключ",
    type="password",
    placeholder="Встав свій API-ключ",
    help="Ключ використовується лише для цього запуску й не записується в код.",
)

source_text = st.text_area(
    "Текст для перетворення",
    placeholder="Наприклад: Відповідно до чинного законодавства, громадяни мають право...",
    height=220,
)

rewrite_button = st.button("Переписати розмовною мовою ✨", type="primary")

if rewrite_button:
    if not api_key.strip():
        st.warning("Спочатку введи Groq API-ключ.")
    elif not source_text.strip():
        st.warning("Додай текст, який потрібно переписати.")
    else:
        try:
            client = Groq(api_key=api_key.strip())

            with st.spinner("Підбираю природніші формулювання..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Ти — редактор українських текстів. "
                                "Перепиши текст природною розмовною українською мовою: "
                                "використовуй прості слова, коротші й невимушені речення, "
                                "дружній тон. Збережи початковий зміст, факти, імена, "
                                "дати, числа та важливі деталі. Не вигадуй інформацію "
                                "і не змінюй сенс. Якщо текст уже розмовний, зроби його "
                                "трохи природнішим, не змінюючи зміст. "
                                "У відповіді подай тільки переписаний текст — "
                                "без вступу, пояснень, лапок чи коментарів."
                            ),
                        },
                        {"role": "user", "content": source_text.strip()},
                    ],
                    temperature=0.7,
                )

            rewritten_text = response.choices[0].message.content or ""
            rewritten_text = rewritten_text.strip()

            if rewritten_text:
                st.markdown(
                    '<div class="result-heading">🩷️ Готовий результат</div>',
                    unsafe_allow_html=True,
                )
                st.text_area(
                    "Текст розмовною мовою",
                    value=rewritten_text,
                    height=230,
                )
                st.download_button(
                    "Завантажити результат у TXT",
                    data=rewritten_text,
                    file_name="rewritten_text.txt",
                    mime="text/plain",
                )
            else:
                st.error("Модель повернула порожню відповідь. Спробуй ще раз.")

        except AuthenticationError:
            st.error("Не вдалося авторизуватися. Перевір правильність API-ключа.")
        except RateLimitError:
            st.error("Перевищено ліміт запитів Groq. Зачекай трохи й повтори спробу.")
        except APIError as error:
            st.error(f"Помилка Groq API: {error}")
        except Exception as error:
            st.error(f"Не вдалося обробити текст: {error}")

st.markdown("---")

