import streamlit as st
from gemini_api import get_fixed_code
from utils import create_fixed_zip

st.set_page_config(page_title="Gemini Code Fixer", layout="wide")
st.title("🧠 Gemini-Powered Code Fixer & Explainer")

# Sidebar options
st.sidebar.title("⚙️ Settings")
mode = st.sidebar.radio("Choose Mode:", ["Fix Only", "Fix + Explain"])
explain = mode == "Fix + Explain"

# Upload individual files
uploaded_files = st.file_uploader("📄 Upload multiple code files", type=["py", "js", "ts", "jsx", "txt" , "tsx"], accept_multiple_files=True)

if uploaded_files:
    fixed_files = {}

    for file in uploaded_files:
        file_name = file.name
        file_code = file.read().decode("utf-8", errors="ignore")

        with st.spinner(f"Fixing {file_name}..."):
            try:
                fixed_code = get_fixed_code(file_code, explain)
                fixed_files[file_name] = fixed_code

                with st.expander(f"✅ {file_name} (Fixed)"):
                    st.code(fixed_code, language="python" if file_name.endswith(".py") else "javascript")

            except Exception as e:
                st.error(f"❌ Error fixing {file_name}: {e}")

    if fixed_files:
        zip_buffer = create_fixed_zip(fixed_files)
        st.download_button("📥 Download All Fixed Files (ZIP)", zip_buffer, file_name="fixed_code_files.zip")