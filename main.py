import streamlit as st
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
from streamlit_extras.stoggle import stoggle
from streamlit_extras.let_it_rain import rain
from streamlit_extras.colored_header import colored_header

# ✅ Cấu hình page
st.set_page_config(page_title="Customer shopping trends ", page_icon="🧡", layout="wide")

st.title("🧭 Customer shopping trends ")
st.markdown("Welcome to the **combined dashboard** of introduction and Shopping Analysis!")

# ✅ Tabs chia từng mục
tab1, tab2, tab3, tab4 = st.tabs([
    "📘 Group introduction",
    "🛍️Shopping Trends - Introduction",
    "📅 Purchase frequency",
    "🛒Purchased items"
])

# ========== TAB 1 ==========
with tab1:
    st.title("💡 Python 2- Business IT 2")
    st.write("We are a group of business students interested in customer shopping trends. Therefore, we decided to analyze a data set about products and purchase frequencies for different age groups.")
    
    stoggle("Group information ", """
    \n 1. Ho Huynh Gia Phuc - 10622045
    \n 2. Nguyen Thanh Thuy - 10622023
    \n 3. Nguyen Ho Huy Thong - 10622014
    \n 4. Vu thien Tuan - 10622088
    \n 5. Pham Thi Tuyet Mai - 10622073
    """)
    
    rain(emoji="🎓", font_size=42, falling_speed=5, animation_length="3")

    colored_header("Thành viên nhóm", "Thông tin chi tiết", color_name="blue-green-70")
    
    members = [
        ("1.jpg", "Ho Huynh Gia Phuc (Leader)", "10622045", "10622045@student.vgu.edu.vn", "BBA", "077 6209215"),
        ("2.jpg", "Nguyen Thanh Thuy", "10622023", "10622023@student.vgu.edu.vn", "BFA", "090 8784370"),
        ("3.jpg", "Nguyen Ho Huy Thong", "10622014", "10622014@student.vgu.edu.vn", "BBA", "039 2230636"),
        ("4.jpg", "Vu Thien Tuan", "10622088", "10622088@student.vgu.edu.vn", "BBA", "096 1234567"),
        ("5.jpg", "Pham Thi Tuyet Mai", "10622073", "10622073@student.vgu.edu.vn", "BFA", "093 7654321"),
    ]

    for i in range(0, len(members), 2):
        col1, col2 = st.columns(2)
        for col, (img, name, sid, email, major, phone) in zip([col1, col2], members[i:i+2]):
            with col:
                st.image(Image.open(img), width=250)
                st.subheader(name)
                st.markdown(f"**ID:** {sid}  \n**Email:** {email}  \n**Major:** {major}  \n**Phone:** {phone}")

    st.markdown("---")
    st.subheader("💬 Góp ý cho nhóm")
    contactform = """<form action="https://formsubmit.co/10622045@student.vgu.edu.vn" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Name" required>
         <input type="email" name="email" placeholder="Email " required>
         <textarea name="message" placeholder="Nhắn gì đó nhé~"></textarea>
         <button type="submit">Gửi</button>
    </form>"""
    st.markdown(contactform, unsafe_allow_html=True)

# ========== TAB 2 ==========
with tab2:
    st.title("🛍️ About Shopping Data")
    st.markdown("""
    Welcome to exploring customer shopping trends!
    
    - Consumer behavior analysis
    - Find out shopping frequency
    - Most purchased items
    """)

st.write("[Accessing our dataset >](https://docs.google.com/spreadsheets/d/1fIlFhKB7DCpfObmOpn2KVlsaEYW6Tdn9g5mkgzhGpDE/edit?gid=244936750#gid=244936750)")


# ========== TAB 3 ==========
with tab3:
    st.title("📅Purchase Frequency Analysis ")

    @st.cache_data
    def load_data():
        df = pd.read_excel("shopping_trends.xlsx", sheet_name="shopping_trends")
        return df

    df = load_data()

    freq = st.selectbox("Select frequency group:", df["Frequency of Purchases"].unique())
    df_freq = df[df["Frequency of Purchases"] == freq]

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Number of customers", df_freq.shape[0])
    col2.metric("💵 Total expenditure", f"${df_freq['Purchase Amount (USD)'].sum():,.2f}")
    col3.metric("📈 Average number of previous purchases", f"{df_freq['Previous Purchases'].mean():.2f}")

    fig, ax = plt.subplots()
    sns.histplot(df_freq["Age"], bins=10, kde=True, ax=ax, color='orange')
    ax.set_title("Average number of previous purchases")
    st.pyplot(fig)

# ========== TAB 4 ==========
with tab4:
    st.title("🛒Purchased Items Analysis")

    gender = st.multiselect("Select gender", df["Gender"].unique(), default=df["Gender"].unique())
    age_range = st.slider("Select age", int(df["Age"].min()), int(df["Age"].max()), (18, 60))

    df_filtered = df[
        (df["Gender"].isin(gender)) &
        (df["Age"] >= age_range[0]) &
        (df["Age"] <= age_range[1])
    ]

    item_counts = df_filtered["Item Purchased"].value_counts().reset_index()
    item_counts.columns = ["Item", "Count"]

    st.subheader("🔝 Top 10 products purchased")
    fig1 = px.bar(item_counts.head(10), x="Count", y="Item", orientation='h', color="Count", color_continuous_scale="teal")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📊 Item Rate")
    fig2 = px.pie(item_counts, names="Item", values="Count", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)
