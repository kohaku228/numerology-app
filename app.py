
import streamlit as st

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

# Streamlitアプリ本体
st.title("🔢 数秘術診断アプリ")
st.markdown("あなたの生年月日と名前から、4つの基本的な数秘術の数を導き出します。")

name = st.text_input("名前（ローマ字で入力してください 例：TARO YAMADA）")
birthdate = st.date_input("生年月日を選んでください")

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
