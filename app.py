import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

from helper import most_common_words, daily_timeline

st.sidebar.title("WhatsApp chat analyzer")
st.sidebar.image("Whatsapp.png")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    # preprocess
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("show analysis wrt ", user_list)

    # total_msg, total_words, total_media, total_links

    if st.sidebar.button("Show Analysis"):

        st.title("Top Statistics")
        total_msg, total_words, total_media, total_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Message')
            st.title(total_msg)
        with col2:
            st.header('Total Words')
            st.title(total_words)
        with col3:
            st.header('Total Media')
            st.title(total_media)
        with col4:
            st.header('Total Links')
            st.title(total_links)

        #monthly timline
        st.title("Monthly Timeline")
        time_line = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time_line['time'], time_line['message'], color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.weekly_active_day(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.monthly_active(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity heatmap
        st.title("Activity Heatmap (in hour)")
        htmap = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots()
        sns.heatmap(htmap, ax=ax)
        plt.yticks(rotation="horizontal")
        # plt.xticks(rotation='horizontal')
        st.pyplot(fig)


        #MOst busy users graph and percent
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.fetch_most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words used
        st.header(f"Most Common Words used by {selected_user}")
        new_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(new_df[0], new_df[1])
        st.pyplot(fig)

        #emoji_analysis
        st.header("Most used emojis")
        emoji_df = helper.emoji_analysis(selected_user, df)

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[0], autopct="%0.2f")
            st.pyplot(fig)
