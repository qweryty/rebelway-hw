import time
import json
import streamlit as st
import requests

st.title("Quotes")

st.write("ID")
id_chart = st.line_chart()
st.write("Length")
length_chart = st.line_chart()
text = st.text("quote")

session = requests.Session()
while True:
    response = session.get("https://animechan.io/api/v1/quotes/random")
    if not response.ok:
        print("Failed")
        print(response.content)
        time.sleep(10)
        continue

    data = json.loads(response.content.decode())
    if data.get("status") != "success":
        print("Failed")
        print(data)
        time.sleep(10)
        continue

    id_chart.add_rows([data["data"]["anime"]["id"]])
    text.text(data["data"]["content"])
    length_chart.add_rows([len(data["data"]["content"])])
    time.sleep(10)
