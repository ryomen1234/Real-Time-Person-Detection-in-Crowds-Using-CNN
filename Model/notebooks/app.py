import streamlit as st
import requests

API_URL = "http://localhost:8000"  # FastAPI backend URL

st.title("Student Management System")

menu = ["Register Student", "View All Students"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register Student":
    st.subheader("Register a New Student")

    prn = st.text_input("PRN")
    name = st.text_input("Name")
    source = st.selectbox("Source", ["camera", "file"])
    img_file = st.file_uploader("Upload Student Image", type=["jpg", "png", "jpeg"])

    if st.button("Register"):
        if prn and name and img_file:
            files = {"img": (img_file.name, img_file, "image/jpeg")}
            data = {"id": prn, "name": name, "source": source}
            response = requests.post(f"{API_URL}/resister", data=data, files=files)
            if response.status_code == 200:
                st.success(f"Student {name} registered successfully!")
            else:
                st.error("Failed to register student.")
        else:
            st.warning("Please fill all fields and upload an image.")

elif choice == "View All Students":
    st.subheader("All Registered Students")
    response = requests.get(f"{API_URL}/all_students/")
    if response.status_code == 200:
        students = response.json().get("students", [])
        for student in students:
            st.write(f"**PRN:** {student['payload'].get('PRN')}")
            st.write(f"**Name:** {student['payload'].get('name')}")
            st.write(f"**Source:** {student['payload'].get('source')}")
            st.write("---")
    else:
        st.error("Failed to fetch students.")
