import streamlit as st, requests, random
st.set_page_config(page_title="Zettabet", layout="centered")
st.title("🎯 Zettabet – Palpites Lotofácil 13-14 acertos")
qtd = st.slider("Quantos palpites?", 1, 25, 5)
if st.button("Gerar"):
    res = requests.post("http://localhost:8000/palpite", json={"qtd": qtd}).json()
    for p in res["palpites"]:
        st.write(" ".join(f"{n:02d}" for n in p))