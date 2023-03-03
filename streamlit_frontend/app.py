import streamlit as st
import validators
import requests

# My ec2 instance
BASE_URL = "http://18.144.55.136"

def push_video(source_name, source_url):
    valid_url = validators.url(source_url)
    if not valid_url:
        st.write("make sure the url is a valid video url!")
    
    # make our post request
    data = {"source_name": source_name, "source_url": source_url}
    vid_id = requests.post(f"{BASE_URL}/push", json=data)
    print(f"post request: {vid_id}")

def get_query_data(id):
    return requests.get(f"{BASE_URL}/query/{id}").json()

def get_status(id):
    return requests.get(f"{BASE_URL}/status/{id}").json()

def main():
    st.write("# Push request")
    source_name = st.text_input('Enter video name', '')
    source_url = st.text_input('Enter video URL', '')
    valid_url = validators.url(source_url)
    if not valid_url:
        st.write("make sure the url is a valid video url!")

    st.button("submit", disabled=not valid_url, on_click=lambda: push_video(source_name, source_url))

    st.write("# Query data")
    query_vid_id = st.number_input("video id", step=1)
    query_vid_data = get_query_data(query_vid_id)
    query_vid_status = get_status(query_vid_id)

    # mad jank lol
    if "No video with" in query_vid_status:
        st.write(f"{query_vid_status}")
    else:
        st.write(f"Video has status: `{query_vid_status}`")
        st.write(query_vid_data)

    st.write("# List all data")
    refresh = st.button("refresh data")
    if refresh:
        all_data = requests.get(f"{BASE_URL}/list").json()
        # display in reverse chronological
        all_data.reverse()
        st.write(all_data)
    # st.table(data.json())


main()
