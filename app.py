import streamlit as st
import pandas as pd
import preproccessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df =preproccessor.preprocess(df, region_df)
user_menu = st.sidebar.radio(

    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.header('Medal Tally')
    country, years = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select country', country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Medal Distribution')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title('Overall Medal of ' + selected_country + 'in Olympics')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Overall medal in'+str(selected_year))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title('Overall medals of'+selected_country+'in'+str(selected_country))

    st.dataframe(medal_tally)

if user_menu=='Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    Atheletes_names = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    events = df['Event'].unique().shape[0]

    st.title('Top Statics')
    col1,col2,col3,col4= st.columns(4)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    with col4:
        st.header('Nations')
        st.title(nations)

    col5, col6 = st.columns(2)
    with col5:
        st.header('Events')
        st.title(events)
    with col6:
        st.header('Atheletes')
        st.title(Atheletes_names)



    nations_over_time =helper.particioating_nations_over_time(df)
    st.title('Number of Nations Participating over the years ')
    fig = px.line(nations_over_time, x='Edition',y='Number of Countries')
    st.plotly_chart(fig)

    events_over_time = helper.Event_over_time(df)
    st.title('Number of Events Organize over the years')
    fig = px.line(events_over_time, x='Edition', y='Number of Events')
    st.plotly_chart(fig)


    Atheletes_over_time = helper.athletes_over_time(df)
    st.title('Number of Athletes participate over the years')
    fig = px.line(Atheletes_over_time, x='Edition', y='Number of Athletes')
    st.plotly_chart(fig)

    st.title('No. of events over time (every sport)')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Atheletes')
    st.header('and 24535 atheletes are more')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    st.subheader('Top 10 Atheletes in {}'.format(selected_sport))
    x = helper.mostsuccessful(df, selected_sport)
    st.table(x)

if user_menu == "Country-Wise Analysis":

    st.title('Country Wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country =st.selectbox('Select a country', country_list)

    country_df = helper.year_wisemealtally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + 'Medal tally over the Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' Excels in the following Sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 Atheletes of all time')
    top10_df = helper.most_successful_atheletes(df, selected_country)
    st.table(top10_df)


if user_menu=='Athlete wise Analysis':
    athelete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df[athelete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athelete_df[athelete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athelete_df[athelete_df['Medal'] == 'Bronze']['Age'].dropna()


    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)




