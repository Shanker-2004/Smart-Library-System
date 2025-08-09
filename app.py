import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import get_connection

st.set_page_config(page_title="📚 Local Library", layout="wide")

engine = get_connection()

st.title("📚 Smart Library System (Local)")

tab1, tab2 = st.tabs(["🔍 Books", "👤 Users"])

# --- Books Tab ---
with tab1:
    st.header("Books")
    search_term = st.text_input("Enter book title or author:")

    if st.button("Search Books"):
        if search_term.strip():
            query = f"""
                SELECT * FROM books
                WHERE title ILIKE '%%{search_term}%%' 
                OR author ILIKE '%%{search_term}%%'
            """
            df = pd.read_sql(text(query), engine)
            if df.empty:
                st.warning("No books found.")
            else:
                df.insert(0, "No.", range(1, len(df) + 1))  # Add numbering
                st.dataframe(df)
        else:
            st.warning("Please enter a search term.")

# --- Users Tab ---
with tab2:
    st.header("Users")
    user_name = st.text_input("Enter user name:")

    if st.button("Search Users"):
        if user_name.strip():
            query = f"SELECT * FROM users WHERE name ILIKE '%%{user_name}%%'"
            df_users = pd.read_sql(text(query), engine)

            if df_users.empty:
                st.warning("No users found.")
            else:
                df_users.insert(0, "No.", range(1, len(df_users) + 1))  # Add numbering
                st.dataframe(df_users)

                # Detect correct ID column
                if "id" in df_users.columns:
                    user_id = df_users.iloc[0]["id"]
                elif "user_id" in df_users.columns:
                    user_id = df_users.iloc[0]["user_id"]
                else:
                    st.error("❌ Could not find a column for user ID.")
                    st.stop()

                borrowed = 0  # default value

                # Try borrowed_books table first
                try:
                    count_query = f"""
                        SELECT COUNT(*) AS books_borrowed
                        FROM borrowed_books
                        WHERE user_id = {user_id}
                    """
                    df_count = pd.read_sql(text(count_query), engine)
                    borrowed = df_count.iloc[0]["books_borrowed"]
                except Exception:
                    # Check if books table has borrowed_by column before using it
                    books_cols = pd.read_sql(
                        text("SELECT * FROM books LIMIT 0"), engine
                    ).columns.tolist()

                    if "borrowed_by" in books_cols:
                        count_query = f"""
                            SELECT COUNT(*) AS books_borrowed
                            FROM books
                            WHERE borrowed_by = {user_id}
                        """
                        df_count = pd.read_sql(text(count_query), engine)
                        borrowed = df_count.iloc[0]["books_borrowed"]
                    else:
                        st.info("ℹ️ No borrowed book tracking found in books table.")

                st.success(f"📚 This user has borrowed **{borrowed}** books.")
        else:
            st.warning("Please enter a user name.")
