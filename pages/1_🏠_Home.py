import streamlit as st
from pages.stream_app.utils import setup_page

setup_page("Archimedes", sidebar_state="collapsed")

# Welcome section
st.title("Welcome to Archimedes")
st.markdown("---")

# Create two rows of cards using columns
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Notebooks Card
with row1_col1:
    if st.button("📒 Courses", key="notebooks_btn", use_container_width=True):
        st.switch_page("pages/2_📒_Courses.py")

# Courses Card
with row1_col2:
    if st.button("📝_Ask_a_Tutor", key="courses_btn", use_container_width=True):
        st.switch_page("pages/3_📝_Ask_a_Tutor.py")

# Ask a Tutor Card
with row2_col1:
    if st.button("🧪 Quizzes", key="tutor_btn", use_container_width=True):
        st.switch_page("pages/4_🧪_Quizzes.py")

# Quizzes Card
with row2_col2:
    if st.button("🤖_Models", key="quiz_btn", use_container_width=True):
        st.switch_page("pages/7_🤖_Models.py")

# Add quick stats or recent activity
st.markdown("---")
st.subheader("📊 Quick Stats")

# Create three columns for stats
stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.metric(label="Total Notebooks", value="5")
with stat2:
    st.metric(label="Active Courses", value="3")
with stat3:
    st.metric(label="Recent Notes", value="12")

# Recent Activity Section
st.markdown("---")
st.subheader("🔄 Recent Activity")
st.info("Your latest notebook was updated 2 hours ago")