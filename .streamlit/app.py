import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load your pickled data
popular_df = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.zip')
similarity_scores = np.load('similarity_scores',allow_pickle=True)

# Streamlit app layout
def main():
    st.title('Book Recommendation System')

    # Sidebar for user input
    st.sidebar.title('User Input')
    user_input = st.sidebar.selectbox('Select a book:', list(pt.index))

    if st.sidebar.button('Recommend'):
        recommend(user_input)

def recommend(user_input):
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError:
        st.error('Book not found in database. Please select another book.')
        return

    # Get top similar items
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    st.subheader('Recommended Books')

    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        if not temp_df.empty:
            st.write(f"**Title:** {temp_df['Book-Title'].values[0]}")
            st.write(f"**Author:** {temp_df['Book-Author'].values[0]}")
            st.image(temp_df['Image-URL-M'].values[0])

if __name__ == '__main__':
    main()
