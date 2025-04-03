import streamlit as st
import datetime
import locale

# 日本語ロケールに設定（日本語の月・曜日表記用）
try:
    locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
except:
    pass

# ピタゴラス数値変換表

def char_to_num(c):
    mapping = {
        'A':1, 'J':1, 'S':1,
        'B':2, 'K':2, 'T':2,
        'C':3, 'L':3, 'U':3,
        'D':4, 'M':4, 'V':4,
        'E':5, 'N':5, 'W':5,
        'F':6, 'O':6, 'X':6,
        'G':7, 'P':7, 'Y':7,
        'H':8, 'Q':8, 'Z':8,
        'I':9, 'R':9
    }
    return mapping.get(c.upper(), 0)

# 数値を1桁まで還元（マスターナンバーは除く）
def reduce_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# 生年月日から運命数
@st.cache_data
def calculate_life_path_number(birthdate):
    digits = [int(d) for d in birthdate.replace('-', '') if d.isdigit()]
    return reduce_number(sum(digits))

# 誕生日から誕生数
@st.cache_data
def calculate_birth_day_number(day):
    return reduce_number(day)

# 名前から表現数
@st.cache_data
def calculate_expression_number(name):
    return reduce_number(sum(char_to_num(c) for c in name if c.isalpha()))

# 名前から魂の欲求数（母音のみ）
def calculate_soul_urge_number(name):
    vowels = "AEIOU"
    return reduce_number(sum(char_to_num(c) for c in name if c.upper() in vowels))

# 2人の運命数の関係性評価
def evaluate_compatibility(n1, n2):
    distance = abs(n1 - n2)
    if n1 == n2:
        return "似すぎて衝突も／深い理解"
    elif distance == 1:
        return "バランスが良い／補い合える関係"
    elif distance in [2, 3]:
        return "やや違いがあり刺激的な関係"
    else:
        return "理解に時間がかかるが学びが大きい"

def get_relationship_theme(n):
    themes = {
        1: "自立とチャレンジの関係",
        2: "共感と寄り添いの関係",
        3: "楽しさと遊び心の関係",
        4: "安定と現実的なパートナーシップ",
        5: "変化と刺激を求める関係",
        6: "愛と家庭的な関係",
        7: "精神性と心の距離感を学ぶ関係",
        8: "成功と目標達成の協働関係",
        9: "奉仕・学び・運命的な縁",
        11: "霊的な成長・インスピレーションの関係",
        22: "理想実現と共同創造の関係",
        33: "無条件の愛を学び合う魂のパートナー"
    }
    return themes.get(n, "未知の関係")

# Streamlitアプリ本体
st.title("🔢 数秘術診断アプリ")
st.markdown("あなたの生年月日と名前から、4つの基本的な数秘術の数を導き出します。また、相性診断もお試しいただけます。")

# タブ表示
basic_tab, compatibility_tab = st.tabs(["🧑‍💼 自分を診断", "💑 相性診断"])

with basic_tab:
    name = st.text_input("名前（ローマ字で入力してください 例：TARO YAMADA）")
    birthdate = st.date_input(
        "生年月日を選んでください",
        min_value=datetime.date(1925, 1, 1),
        max_value=datetime.date(2025, 12, 31),
        value=datetime.date(1980, 1, 1)
    )

    if st.button("診断する"):
        if name:
            life_path = calculate_life_path_number(birthdate.strftime('%Y-%m-%d'))
            birth_day = calculate_birth_day_number(birthdate.day)
            expression = calculate_expression_number(name)
            soul = calculate_soul_urge_number(name)

            st.subheader("🔮 診断結果")
            st.write(f"**運命数（Life Path Number）：** {life_path}")
            st.write(f"**誕生数（Birth Day Number）：** {birth_day}")
            st.write(f"**表現数（Expression Number）：** {expression}")
            st.write(f"**魂の欲求数（Soul Urge Number）：** {soul}")
        else:
            st.warning("名前をローマ字で入力してください。")

with compatibility_tab:
    col1, col2 = st.columns(2)
    with col1:
        your_name = st.text_input("あなたの名前（ローマ字）", key="your_name")
        your_birthdate = st.date_input(
            "あなたの生年月日",
            min_value=datetime.date(1925, 1, 1),
            max_value=datetime.date(2025, 12, 31),
            value=datetime.date(1980, 1, 1),
            key="your_birthdate")
    with col2:
        partner_name = st.text_input("相手の名前（ローマ字）", key="partner_name")
        partner_birthdate = st.date_input(
            "相手の生年月日",
            min_value=datetime.date(1925, 1, 1),
            max_value=datetime.date(2025, 12, 31),
            value=datetime.date(1985, 1, 1),
            key="partner_birthdate")

    if st.button("相性を診断"):
        you = calculate_life_path_number(your_birthdate.strftime('%Y-%m-%d'))
        partner = calculate_life_path_number(partner_birthdate.strftime('%Y-%m-%d'))
        total = reduce_number(you + partner)
        relation = evaluate_compatibility(you, partner)
        theme = get_relationship_theme(total)

        st.subheader("🔗 相性診断結果")
        st.write(f"あなたの運命数：{you}")
        st.write(f"相手の運命数：{partner}")
        st.write(f"相性タイプ：{relation}")
        st.write(f"ふたりの関係性テーマ（合計数 {total}）：{theme}")
