
from numpy import NaN
import streamlit as st
from pandasql import sqldf
from sklearn import datasets
import pickle
import pandas as pd
import requests
import ast
import sqlite3
import streamlit.components.v1 as components
import time
from streamlit_option_menu import option_menu
import numpy
from PIL import Image

st.set_page_config(page_title="Movie Recommender", layout='wide')
# st.title('Welcome to PopCorn')
# st.markdown("[![Foo]()](http://google.com.au/)")
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=73efae0ed93a5601ac51cc320de316b1&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:11]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster  

st.sidebar.title('PopCorn')
# with st.sidebar:
#     with st.echo():
#         "This code will be printed to the sidebar."
#     with st.spinner("Loading..."):
#         time.sleep(5)
#     st.success("Done!")
with st.sidebar:
       rad = option_menu(
           menu_title=None,
           options=["Home", "What's Hot", "Bucket_List", "Ratin-O-Meter", "About Us"],
        )
if rad=="Home":
        st.markdown('<h1 style="font-family: cursive; font-size:600%; color:#D10B0B;"><b>Welcome To PopCorn</b></h1>', unsafe_allow_html=True)
        movies_dict= pickle.load(open('movies_dict.pkl','rb'))
        movies = pd.DataFrame(movies_dict)
        orig_list = pd.read_csv('movieList.csv')
        orig_list = orig_list[['genres', 'id', 'title', 'vote_average', 'genres1']]
        # orig_list.iloc[0].genres
        orig_list['genres'] = orig_list['genres'].apply(convert)
        pysqldf = lambda q: sqldf(q, globals())
        orig_list = orig_list.sort_values(
                by="vote_average",
                ascending = False
        )
        genres = pd.DataFrame(orig_list['genres1'].value_counts()).head(6)
        # st.write(genres.head())
        mov_id = pd.DataFrame(orig_list['id'].value_counts()).head(10)
        # st.write(mov_id.index[0])
        # selected_genre = st.sidebar.selectbox('Select Genre', orig_list['genres1'].values)
        orig_list['genres'] = orig_list['genres'].apply(lambda x:" ".join(x))
        # st.write(orig_list.head())
        # st.write(orig_list.where(orig_list['genres']==selected_genre))
        # st.write(selected_genre)
        year_list = pd.read_csv('movieList.csv')
        pysqldf = lambda q: sqldf(q, globals())
        query = "SELECT * FROM orig_list where genres='Thriller' LIMIT 5"
        Thriller = pysqldf(query)
        query2 = "SELECT * FROM orig_list where genres='Romance' LIMIT 5"
        Romantic = pysqldf(query2)
        # st.write(Romantic)
        years = st.sidebar.slider('Top Movies By Year:', min_value=1980, max_value=2017, value=2000, step=1)
        # query7 = "Select * FROM year_list WHERE YEAR==@years LIMIT 5"
        # Years = pysqldf(query7)
        # st.write(Years)
        new_df = year_list.query("YEAR==@years")
        # st.write(new_df)
        similarity  = pickle.load(open('similarity.pkl','rb'))
        first_col, second_col, third_col = st.columns(3)
        # first_col.subheader('Enjoy your Movies')
        first_col.markdown('<h2 style="color:#F56B3B;">Enjoy your Movies</h2>', unsafe_allow_html=True)
        third_col.markdown('<br>',  unsafe_allow_html=True)
        with third_col.expander("LOG IN/ SIGN UP"):
            st.write("Hello User : Please Enter your details")
            Login = st.selectbox("Select", ["Login", "Register"])
            if Login=="Login":
                input_user = st.text_input('UserName', ' ')
                input_password = st.text_input('Password', ' ')
                if input_user!=' ':
                    if input_password!=' ':
                        with st.spinner("Loading..."):
                            time.sleep(5)
                        st.success("Logged In Successfully!")
            if Login=="Register":
                    input_user1 = st.text_input('UserName', ' ')
                    input_password1 = st.text_input('Password', ' ') 
                    st.write("Add a DP to your Profile")
                    picture = st.camera_input("Take a picture") 
                    if st.button('Submit'):
                        to_add = {"UserName":[input_user1], "PassWord":[input_password1], "Image":[picture]}
                        to_add = pd.DataFrame(to_add)
                        open('Data_User.csv', 'w').write(to_add.to_csv())
                        st.success("Profile Created")       
        selected_movie_name = st.selectbox(
        'For Recommendations, Select Movie and Click Recommend',
        movies['title'].values)

        if st.button('Recommend'):
            st.header('Recommended movies')
            names,posters = recommend(selected_movie_name)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(names[0])
                st.image(posters[0])
            with col2:
                st.text(names[1])
                st.image(posters[1])
            with col3:
                st.text(names[2])
                st.image(posters[2])
            with col4:
                st.text(names[3])
                st.image(posters[3])
            with col5:
                st.text(names[4])
                st.image(posters[4])
                
            col6, col7, col8, col9, col10 = st.columns(5)
            with col6:
                st.text(names[5])
                st.image(posters[5])
            with col7:
                st.text(names[6])
                st.image(posters[6])
            with col8:
                st.text(names[7])
                st.image(posters[7])
            with col9:
                st.text(names[8])
                st.image(posters[8])
            with col10:
                st.text(names[9])
                st.image(posters[9])
        st.subheader("Top rated of the year")
        st.write(years)
        yearss = st.container()
        with yearss:
            col30, col31, col32, col33, col34 = st.columns(5)
            with col30:
                st.text(new_df.iloc[0].title)
                st.image(fetch_poster(new_df.iloc[0].id))
            with col31:
                st.text(new_df.iloc[1].title)
                st.image(fetch_poster(new_df.iloc[1].id))
            with col32:
                st.text(new_df.iloc[2].title)
                st.image(fetch_poster(new_df.iloc[2].id))
            with col33:
                st.text(new_df.iloc[3].title)
                st.image(fetch_poster(new_df.iloc[3].id))
            with col34:
                st.text(new_df.iloc[4].title)
                st.image(fetch_poster(new_df.iloc[4].id))
        top_on = st.container()       
        with top_on:
            st.subheader('Trending on PopCorn')
            col12, col13, col14, col15, col16 = st.columns(5)
            with col12:
                st.image(fetch_poster(mov_id.index[7]))
            with col13:
                st.image(fetch_poster(mov_id.index[2]))
            with col14:
                st.image(fetch_poster(mov_id.index[3]))
            with col15:
                st.image(fetch_poster(mov_id.index[4]))
            with col16:
                st.image(fetch_poster(mov_id.index[5]))
        # components.iframe("https://docs.streamlit.io/en/latest")  
        video_file = open('fifty_shades.mp4', 'rb')  
        video_bytes = video_file.read()
        Bucket = pd.DataFrame([["0", "Fifty Shades of Grey", "fifty_shades.mp4", "97.9"], ["1", "maze runner", "maze.mp4", "96.6"]],
                 columns=["id", "Movie_name", "clip", "popularity"])
        Bucket = Bucket.sort_values(
            by="popularity",
            ascending = False
        )        
        st.subheader("**Latest Voted Movie Clip**")
        video_fil1 = open("maze.mp4", 'rb')
        if Bucket.iloc[0].clip=="fifty_shades.mp4":
            st.video(video_file)
        else:
               st.video(video_fil1) 
        container = st.container()   
        container.subheader('Thriller on PopCorn')
        Thrill = st.container() 
        with Thrill:
            col20, col21, col22, col23, col24 = st.columns(5)
            with col20:
                st.text(Thriller.iloc[0].title)
                st.image(fetch_poster(Thriller.iloc[0].id))
            with col21:
                st.text(Thriller.iloc[1].title)
                st.image(fetch_poster(Thriller.iloc[1].id))
            with col22:
                st.text(Thriller.iloc[2].title)
                st.image(fetch_poster(Thriller.iloc[2].id))
            with col23:
                st.text(Thriller.iloc[3].title)
                st.image(fetch_poster(Thriller.iloc[3].id))
            with col24:
                st.text(Thriller.iloc[4].title)
                st.image(fetch_poster(Thriller.iloc[4].id))
        st.subheader("Romantic On PopCorn")        
        Romance = st.container()
        with Romance:
            col30, col31, col32, col33, col34 = st.columns(5)
            with col30:
                st.text(Romantic.iloc[0].title)
                st.image(fetch_poster(Romantic.iloc[0].id))
            with col31:
                st.text(Romantic.iloc[1].title)
                st.image(fetch_poster(Romantic.iloc[1].id))
            with col32:
                st.text(Romantic.iloc[2].title)
                st.image(fetch_poster(Romantic.iloc[2].id))
            with col33:
                st.text(Romantic.iloc[3].title)
                st.image(fetch_poster(Romantic.iloc[3].id))
            with col34:
                st.text(Romantic.iloc[4].title)
                st.image(fetch_poster(Romantic.iloc[4].id)) 

        query3 = "SELECT * FROM orig_list where genres='Action' LIMIT 5"
        Action = pysqldf(query3)
        st.subheader("Action On PopCorn")   
        Actin = st.container()
        with Actin:
            col30, col31, col32, col33, col34 = st.columns(5)
            with col30:
                st.text(Action.iloc[0].title)
                st.image(fetch_poster(Action.iloc[0].id))
            with col31:
                st.text(Action.iloc[1].title)
                st.image(fetch_poster(Action.iloc[1].id))
            with col32:
                st.text(Action.iloc[2].title)
                st.image(fetch_poster(Action.iloc[2].id))
            with col33:
                st.text(Action.iloc[3].title)
                st.image(fetch_poster(Action.iloc[3].id))
            with col34:
                st.text(Action.iloc[4].title)
                st.image(fetch_poster(Action.iloc[4].id))

        query5 = "SELECT * FROM orig_list where genres='Drama' LIMIT 5"
        Drama = pysqldf(query5)
        st.subheader("Drama On PopCorn")   
        Dram = st.container()
        with Dram:
            col30, col31, col32, col33, col34 = st.columns(5)
            with col30:
                st.text(Drama.iloc[0].title)
                st.image(fetch_poster(Drama.iloc[0].id))
            with col31:
                st.text(Drama.iloc[1].title)
                st.image(fetch_poster(Drama.iloc[1].id))
            with col32:
                st.text(Drama.iloc[2].title)
                st.image(fetch_poster(Drama.iloc[2].id))
            with col33:
                st.text(Drama.iloc[3].title)
                st.image(fetch_poster(Drama.iloc[3].id))
            with col34:
                st.text(Drama.iloc[4].title)
                st.image(fetch_poster(Drama.iloc[4].id))
        query4 = "SELECT * FROM orig_list where genres='Comedy' LIMIT 5"
        Comedy = pysqldf(query4)
        st.subheader("Comedy On PopCorn")   
        Comey = st.container()
        with Comey:
            col30, col31, col32, col33, col34 = st.columns(5)
            with col30:
                st.text(Comedy.iloc[0].title)
                st.image(fetch_poster(Comedy.iloc[0].id))
            with col31:
                st.text(Comedy.iloc[1].title)
                st.image(fetch_poster(Comedy.iloc[1].id))
            with col32:
                st.text(Comedy.iloc[2].title)
                st.image(fetch_poster(Comedy.iloc[2].id))
            with col33:
                st.text(Comedy.iloc[3].title)
                st.image(fetch_poster(Comedy.iloc[3].id))
            with col34:
                st.text(Comedy.iloc[4].title)
                st.image(fetch_poster(Comedy.iloc[4].id))
        st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray"><h4 style="text-align:center;">Reach us Out At<br><br></h4>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([5, 5, 5, 1])
        # st.markdown("[![Foo](insta.jpg)](http://google.com.au/)")
        col1.image("insta.jpg", width=80)
        col2.image("facebook.png", width=80)
        col3.image("gmail.png", width=110)
        col4.image("phone.png", width=60)      
        st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
if rad=="About Us":
    st.subheader("You will be going to know more about our Product")
    st.write("Popcorn is a recommendation engine project for microsoft engage")
    # col1, col2, col3, col4 = st.columns(4)
    # image = Image.open('download.png')
    # col1.image(image, width=40)
    # col2.subheader("Microsoft Project")
    col1, mid, col2 = st.columns([1,1,20])
    with col1:
        st.image('download.png', width=60)
    with col2:
        st.subheader('Microsoft Project')
    col3, col4 = st.columns(2)
    col3.image("engage.png")
    col4.markdown('<h4 style="font-family: cursive; font-size:200%; color:#F53BEC;"><b>About the Developer</b></h4>', unsafe_allow_html=True)
    col4.text("Hi, My name is Ishika Bhola. I am really overwhelmed to be a ")
    col4.text("part of Microsoft Engage.")
    col4.text("This Project is one of my dream Projects. I have learnt a")
    col4.text("lot while making this project including more about Streamlit")
    col4.text("and Recommendation Engines.")
    st.markdown('<br><br><h4 style="text-align:center; border:2px solid Tomato; font-gamily:cursive;">Made by Ishika Bhola</h4>', unsafe_allow_html=True)
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray"><h4 style="text-align:center;">Reach us Out At<br><br></h4>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 1])
    col1.image("insta.jpg", width=80)
    col2.image("facebook.png", width=80)
    col3.image("gmail.png", width=110)
    col4.image("phone.png", width=60)      
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
if rad=="Bucket_List":
    st.markdown('<h2 style="font-family: cursive; font-size:400%; color:#F5953B"><b>Welcome To Bucket-List!</b></h2>', unsafe_allow_html=True)
    st.subheader("Add your favorite Movies to watch them in future")
    pysqldf = lambda q: sqldf(q, globals())
    movies = pd.read_csv('Movie_combined.csv')
    # st.text("Contribute to our Bucket List")
    # bucket = st.text_input('Contribute to our Bucket List', 'Add Movie')
    st.subheader("Top movies from Users Bucket List - ")
    Bucket = pd.DataFrame([["0", "Inception", "Inception.jpg"], ["1", "Fifty Shades Freed", "freed.jpg"], ["1", "Avengers:Infinity War", "avengers.jpg"], ["4", "the Godfather", "god.jpg"],  ["5", "The vampire diaries", "vampire.jpg"]],
                 columns=["id", "Movie_name", "Image"])       
    # Bucket = pd.read_csv("bucket_list.csv")
    # st.image(x.iloc[0].Department)
    col30, col31, col32, col33, col34 = st.columns(5)
    with col30:
        st.text(Bucket.iloc[0].Movie_name)
        st.image(Bucket.iloc[0].Image)
    with col31:
        st.text(Bucket.iloc[1].Movie_name)
        st.image(Bucket.iloc[1].Image)
    with col32:
        st.text(Bucket.iloc[2].Movie_name)
        st.image(Bucket.iloc[2].Image)
    with col33:
        st.text(Bucket.iloc[3].Movie_name)
        st.image(Bucket.iloc[3].Image)
    with col34:
        st.text(Bucket.iloc[4].Movie_name)
        st.image(Bucket.iloc[4].Image)
    st.subheader("Search Movies to watch later:")    
    movie = st.selectbox(
    '',
    movies['Title'].values)        
    if st.button("Submit"):
        movie_id = movies[movies['Title']==movie].index[0]
        new_df1 = movies.query("Genre==@movies.iloc[@movie_id].Genre")
        st.image(movies.iloc[movie_id].Poster, width=500)
        to_add = {"Movie_name":[movie], "Image":[], "Image":[movies.iloc[movie_id].Poster]}
        to_add = pd.DataFrame(to_add)
        open('Bucket.csv', 'w').write(to_add.to_csv())
        st.success("Submitted. Thank You")
        st.subheader("Movies you might also like:")
        col40, col41, col42, col43, col44 = st.columns(5)
        with col40:
            st.text(new_df1.iloc[0].Title)
            st.image(new_df1.iloc[0].Poster)
        with col41:
            st.text(new_df1.iloc[1].Title)
            st.image(new_df1.iloc[1].Poster)
        with col42:
            st.text(new_df1.iloc[2].Title)
            st.image(new_df1.iloc[2].Poster)
        with col43:
            st.text(new_df1.iloc[4].Title)
            st.image(new_df1.iloc[4].Poster)
        with col44:
            st.text(new_df1.iloc[3].Title)
            st.image(new_df1.iloc[3].Poster)

    # st.text("Fifty Shades Of Grey")
    # st.text("Fifty Shades darker")
    # st.text("Fifty shades Freed")
    # st.text("Nymphomaniac")
    # st.text("365 Days")
    # if bucket!="Add Movie":
    #     st.write(bucket)
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray"><h4 style="text-align:center;">Reach us Out At<br><br></h4>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 1])
    col1.image("insta.jpg", width=80)
    col2.image("facebook.png", width=80)
    col3.image("gmail.png", width=110)
    col4.image("phone.png", width=60)      
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)
if rad=="What's Hot":
    orig_list = pd.read_csv('movieList.csv')
    orig_list = orig_list[['genres', 'id', 'title', 'vote_average', 'genres1', 'YEAR']]
    orig_list['genres'] = orig_list['genres'].apply(convert)
    pysqldf = lambda q: sqldf(q, globals())
    orig_list = orig_list.sort_values(
            by="YEAR",
            ascending = False
    )
    # query = "SELECT * FROM orig_list LIMIT 5"
    # Top = pysqldf(query)
    st.markdown('<h1 style="font-family: cursive; font-size:450%; color:yellow;"><b>Latest on PopCorn</b></h1>', unsafe_allow_html=True)
    # st.subheader("Latest On PopCorn")   
    Comey = st.container()
    with Comey:
        col30, col31, col32, col33, col34 = st.columns(5)
        with col30:
            st.text(orig_list.iloc[0].title)
            st.image(fetch_poster(orig_list.iloc[0].id))
        with col31:
            st.text(orig_list.iloc[1].title)
            st.image(fetch_poster(orig_list.iloc[1].id))
        with col32:
            st.text(orig_list.iloc[2].title)
            st.image(fetch_poster(orig_list.iloc[2].id))
        with col33:
            st.text(orig_list.iloc[3].title)
            st.image(fetch_poster(orig_list.iloc[3].id))
        with col34:
            st.text(orig_list.iloc[4].title)
            st.image(fetch_poster(orig_list.iloc[4].id))
        col30, col31, col32, col33, col34 = st.columns(5)
        with col30:
            st.text(orig_list.iloc[5].title)
            st.image(fetch_poster(orig_list.iloc[5].id))
        with col31:
            st.text(orig_list.iloc[6].title)
            st.image(fetch_poster(orig_list.iloc[6].id))
        with col32:
            st.text(orig_list.iloc[7].title)
            st.image(fetch_poster(orig_list.iloc[7].id))
        with col33:
            st.text(orig_list.iloc[8].title)
            st.image(fetch_poster(orig_list.iloc[8].id))
        with col34:
            st.text(orig_list.iloc[9].title)
            st.image(fetch_poster(orig_list.iloc[9].id))
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray"><h4 style="text-align:center;">Reach us Out At<br><br></h4>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 1])
    col1.image("insta.jpg", width=80)
    col2.image("facebook.png", width=80)
    col3.image("gmail.png", width=110)
    col4.image("phone.png", width=60)      
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)          

if rad=="Ratin-O-Meter":
    st.markdown('<h1 style="font-family: cursive; font-size:400%; color:#3BF5AC;"><b>Give Ratings To movies</b></h1>', unsafe_allow_html=True)
    # st.subheader("")
    pysqldf = lambda q: sqldf(q, globals())
    movies = pd.read_csv('Movie_combined.csv')
    movie = st.selectbox(
    '',
    movies['Title'].values)
    movie_id = movies[movies['Title'] == movie].index[0]
    # for i in range(len(movies.id)):
    #     if movies['Title']==movie:
    #         indx=i
    col1, col2 = st.columns(2)
    col1.image(movies.iloc[movie_id].Poster)
    Rating = col2.text_input('Give Rating(out of 100)', ' ')
    text = col2.text_area("Review")
    moviess = pd.read_csv('movies_metadata.csv')
    st.subheader("Can watch the ratings of movies here")
    moviee = st.selectbox(
    '',
    moviess['title'].values)
    moviee_id = moviess[moviess['title'] == moviee].index[0]
    moviess.iloc[moviee_id].popularity
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray"><h4 style="text-align:center;">Reach us Out At<br><br></h4>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([5, 5, 5, 1])
    col1.image("insta.jpg", width=80)
    col2.image("facebook.png", width=80)
    col3.image("gmail.png", width=110)
    col4.image("phone.png", width=60)      
    st.markdown('<br><hr style="height:2px;border-width:0;color:gray;background-color:gray">', unsafe_allow_html=True)


