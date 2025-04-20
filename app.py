import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import emoji

# Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="MessageMetrics",
    page_icon="💬",
    layout="wide"
)

# Add custom CSS styling
st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding: 2rem;
    }
    
    /* Header styling */
    .st-emotion-cache-18ni7ap {
        background-color: #2c3e50;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling */
    .st-emotion-cache-1r6slb0 {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
    }
    
    /* Table styling */
    table {
        border: 2px solid #2c3e50 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    th {
        background-color: #2c3e50 !important;
        color: white !important;
        padding: 12px !important;
        font-weight: 600 !important;
    }
    
    td {
        padding: 10px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2c3e50 !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 0.5rem 1rem !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background-color: #34495e !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metric containers */
    div[data-testid="stMetricValue"] {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
    }
    
    /* File uploader */
    .st-emotion-cache-1erivf3 {
        border: 2px dashed #2c3e50 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 💬 MessageMetrics")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")     #conversion of the bytes_data into readable text
    df = preprocessor.preprocess(data)

    # Display the dataframe only once
    st.dataframe(df, hide_index=True)
    
    # fetch unique users
    user_list = df['user'].unique().tolist()     
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis w.r.t", user_list)
    
    if st.sidebar.button("Show analysis"):
        num_messages, words, num_media_messages, links, num_emojis, num_stickers = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 📱 Total Messages")
            st.title(num_messages)
        with col2:
            st.markdown("### 📝 Total Words")
            st.title(words)
        with col3:
            st.markdown("### 🖼️ Total Media")
            st.title(num_media_messages)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.markdown("### 🔗 Total Links")
            st.title(links)
        with col5:
            st.markdown("### 😊 Total Emojis")
            st.title(num_emojis)
        with col6:
            st.markdown("### 🎯 Total Stickers")
            st.title(num_stickers)

        # Chat age and first message
        if selected_user == 'Overall':
            chat_info = helper.get_chat_age(df)
        else:
            chat_info = helper.get_user_first_message(selected_user, df)
            
        st.title("📝 Chat Information")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"First Message Date: **{chat_info['first_message_date']}**")
        with col2:
            if selected_user == 'Overall':
                st.info(f"Chat Age: **{chat_info['chat_age']}**")

        st.title("💬 First Message")
        st.markdown(
            f"""
            <div style='padding: 1.5rem; border-radius: 8px; background-color: #ffffff; border-left: 5px solid #2c3e50; margin: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='color: #1f1f1f; font-weight: bold; margin-bottom: 8px; font-size: 1.2em;'>{chat_info['first_message_user']}</p>
                <p style='color: #2c3e50; margin: 0; font-size: 1.3em; background-color: #f8f9fa; padding: 1rem; border-radius: 5px;'>{chat_info['first_message']}</p>
                <p style='color: #666; font-size: 1em; margin-top: 12px;'>{chat_info['first_message_date']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Voice Message Analysis
        st.title("🎤 Voice Message Analysis")
        voice_counts = helper.voice_message_analysis(selected_user, df)
        
        if not voice_counts.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(voice_counts)
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                width = 0.4 if selected_user != 'Overall' else 0.8
                ax.bar(voice_counts['User'], voice_counts['Voice Message Count'], 
                      width=width, color='#008080') #teal
                ax.set_xlabel("User", fontsize=12)
                ax.set_ylabel("Number of Voice Messages", fontsize=12)
                plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
                st.pyplot(fig)
        else:
            st.write("No voice messages found in the chat.")

        # Most Active Users
        if selected_user == 'Overall':
            st.title("👥 Most Active Users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='#008080', width=0.8) #teal
                plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        
         # Call Analysis
        st.title("📞 Call Analysis") 
        call_data, call_message = helper.call_analysis(selected_user, df)
        if call_message:
            st.write(call_message)
        else:
            st.dataframe(call_data)
            fig, ax = plt.subplots()
            width = 0.4 if selected_user != 'Overall' else 0.8
            ax.bar(call_data['Call Type'], call_data['Count'], color=['#39FF14', '#2a3439'], width=width)
            ax.set_xlabel("Call Type", fontsize=12)
            ax.set_ylabel("Count", fontsize=12)
            ax.set_title("Number of Voice and Video Calls", fontsize=14)
            st.pyplot(fig)
        
        # wordcloud
        st.title("☁️ Wordcloud")   
        wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)
        
        # emoji analysis
        st.title("😀 Emoji Analysis")   
        emoji_df = helper.emoji_helper(selected_user, df)   
        col1, col2 = st.columns(2)
        if emoji_df.empty:
            st.write("No emojis found in the messages.")
        else:
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig, ax = plt.subplots()
                ax.pie(emoji_df['Count'], labels=emoji_df['Emoji'], autopct='%1.1f%%')
                st.pyplot(fig)

        # monthly timeline
        st.title("📅 Monthly Timeline")   
        monthly_timeline = helper.monthly_timeline(selected_user, df)    
        fig, ax = plt.subplots()
        ax.plot(monthly_timeline['month'], monthly_timeline['message'], color='#9955bb') #purple
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        if daily_timeline is not None and not daily_timeline.empty:
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#00416A') #dark blue
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.write("No data available for the daily timeline.")
        
        # activity charts
        st.title("📈 Activity Charts")
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#00416A') #blueberry
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#65000B') # rosewood
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # heatmap
        st.title("📊 Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)

        # response time analysis
        st.title("⚡ Response Time Analysis")      
        response_times, fastest_responder = helper.response_time_analysis(selected_user, df)

        if not response_times.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.header("Average Response Time")
                st.dataframe(response_times)
            with col2:
                if fastest_responder is not None:
                    st.header("Fastest Responder")
                    st.write(f"User: {fastest_responder['user']}")
                    st.write(f"Average Response Time: {fastest_responder['avg_response_time']:.2f} seconds")
                else:
                    st.header("Response Time Analysis")
                    st.write("No fastest responder data available.")
        else:
            st.write("No response time data available for analysis.")
        
        # first message of the day
        st.title("🌅 First Message of the Day")  
        first_message_counts = helper.first_message_of_day(selected_user, df)

        if selected_user == 'Overall' and not first_message_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(first_message_counts['user'], first_message_counts['first_message_count'], width=0.8, color='#008080') #teal
            ax.set_xlabel("User", fontsize=12)
            ax.set_ylabel("First Message Count", fontsize=12)
            plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
            st.pyplot(fig)
        elif not first_message_counts.empty:
            st.dataframe(first_message_counts)
        else:
            st.write("No data available for first message analysis.")
        
        # late night activity
        st.title("🌙 Late Night Activity (12 AM - 3 AM)")   
        late_night_counts = helper.late_night_activity(selected_user, df)

        if selected_user == 'Overall' and not late_night_counts.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(late_night_counts['user'], late_night_counts['late_night_message_count'], width=0.8, color='#008080') #teal
            ax.set_xlabel("User", fontsize=12)
            ax.set_ylabel("No. of Messages", fontsize=12)
            plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
            st.pyplot(fig)
        elif not late_night_counts.empty:
            st.dataframe(late_night_counts)
        else:
            st.write("No late-night activity detected.")
        
        # Longest Streaks Analysis
        st.title("🔥 Top 10 Days with Continuous Chat Activity")      
        top_days = helper.longest_streaks(selected_user,df)

        if not top_days.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Create the bar chart
            ax.bar(top_days['only_date'].astype(str), top_days['message_count'], color='#00416A') #dark blue
                            
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Number of Messages", fontsize=12)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        else:
            st.write("No data available for longest streaks analysis.")
        
        # Text Length Analysis
        st.title("📏 Text Length Analysis")
        text_length_df = helper.text_length_analysis(selected_user, df)
        
        if not text_length_df.empty:
            if selected_user == 'Overall':
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(text_length_df['User'], text_length_df['Average Message Length'], width=0.8, color='#008080') #teal
                ax.set_xlabel("User")
                ax.set_ylabel("Average Message Length (characters)")
                plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
                st.pyplot(fig)
            else:
                # For individual user, show a metric display instead of bar chart
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label="Average Message Length",
                        value=f"{text_length_df['Average Message Length'].iloc[0]:.1f} characters",
                        help="Average number of characters per message"
                    )
                with col2:
                    st.dataframe(text_length_df)
        else:
            st.write("No text length data available for analysis.")

        # Message Deletion Analysis
        st.title("🗑️ Message Deletion Analysis")
        deletion_stats = helper.analyze_deleted_messages(selected_user, df)
        
        if not deletion_stats.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(deletion_stats)
            with col2:
                fig, ax = plt.subplots(figsize=(10, 6))
                width = 0.4 if selected_user != 'Overall' else 0.8
                ax.bar(deletion_stats['User'], deletion_stats['Deleted Messages'], 
                      width=width, color='#008080') #teal
                ax.set_xlabel("User", fontsize=12)
                ax.set_ylabel("Number of Deleted Messages", fontsize=12)
                plt.xticks(rotation='vertical' if len(user_list) > 3 else 'horizontal')
                
                # Add percentage labels on top of bars
                for i, v in enumerate(deletion_stats['Deleted Messages']):
                    percentage = deletion_stats['Deletion Rate (%)'].iloc[i]
                    ax.text(i, v, f'{percentage}%', 
                           ha='center', va='bottom')
                st.pyplot(fig)
        else:
            st.write("No deleted messages found in the chat.")

        # Group Dynamics Analysis
        st.title("💭 Group Dynamics Analysis")
        mentions_summary, reply_summary, group_message = helper.analyze_group_dynamics(selected_user, df)
        
        if group_message:
            st.write(group_message)
        else:
            # Mentions Analysis
            st.header("Mentions Analysis")
            if not mentions_summary.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(mentions_summary)
                with col2:
                    fig, ax = plt.subplots(figsize=(10, 6))
                    width = 0.4 if selected_user != 'Overall' else 0.8
                    ax.bar(mentions_summary['Mentioned_by'], mentions_summary['Mention_count'], 
                          color='#4B0082', width=width)  # indigo
                    plt.xticks(rotation='vertical')
                    ax.set_xlabel("User")
                    ax.set_ylabel("Number of Mentions Made")
                    st.pyplot(fig)
            else:
                st.write("No mentions found in the chat")

            # Reply Patterns Analysis
            st.header("Reply Patterns")
            if not reply_summary.empty:
                col1, col2 = st.columns(2)
                with col1:
                    st.dataframe(reply_summary)
                with col2:
                    # Create a heatmap of reply patterns
                    reply_matrix = reply_summary.pivot_table(
                        index='From', columns='To', values='Reply_count', fill_value=0
                    )
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(reply_matrix, annot=True, cmap='YlOrRd', fmt='g')
                    plt.title("Reply Patterns Heatmap")
                    st.pyplot(fig)
            else:
                st.write("No reply patterns found in the chat")
      
      