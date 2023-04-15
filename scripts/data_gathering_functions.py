import sqlite3
import pandas as pd
import numpy as np

#conn = sqlite3.connect(con_string)
con_string = 'db.sqlite3'


def get_subscriber_change(channel_name, start_time):
    """
    Query sql table and get the change in subscribers for selected stream
    input: channel_name, start_time
    output: subcriber change (int)
    """
    
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    new_subscriber_query =  '''
                    with starting_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {} 
                        order by date asc
                        limit 1)

                    ,ending_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        order by date desc
                        limit 1
                        )

                    select * from starting_subscribers
                    UNION ALL select * from ending_subscribers

                    '''.format(channel_name, start_time, channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(new_subscriber_query)
    subscriber_count = cursor_obj.fetchall()
    subscriber_change = subscriber_count[1][0] - subscriber_count[0][0]
    conn.commit()
    conn.close()
    
    return subscriber_change

def get_pct_subscriber_change(channel_name, start_time):
    """
    Query sql table and get the average number of chatters for selected stream
    input: channel_name, start_time
    output: average_chatters (float)
    """
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    new_subscriber_query =  '''
                    with starting_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {} 
                        order by date asc
                        limit 1)

                    ,ending_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        order by date desc
                        limit 1
                        )

                    select * from starting_subscribers
                    UNION ALL select * from ending_subscribers

                    '''.format(channel_name, start_time, channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(new_subscriber_query)
    subscriber_count = cursor_obj.fetchall()
    subscriber_change_pct = round((100 * (subscriber_count[1][0] - subscriber_count[0][0]) / subscriber_count[0][0]))
    conn.commit()
    conn.close()
    
    return subscriber_change_pct

def get_follower_change(channel_name, start_time):
    """
    Query sql table and get the change in followers for selected stream
    input: channel_name, start_time
    output: follower_change (int)
    """
     # set streamer name and datetime for now
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    new_followers_query =  '''
                    with starting_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {} 
                        order by date asc
                        limit 1)

                    ,ending_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        order by date desc
                        limit 1
                        )

                    select * from starting_followers
                    UNION ALL select * from ending_followers

                    '''.format(channel_name, start_time, channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(new_followers_query)
    follower_count = cursor_obj.fetchall()
    follower_change = follower_count[1][0] - follower_count[0][0]
    conn.commit()
    conn.close()  
    
    return follower_change

def get_pct_follower_change(channel_name, start_time):
    """
    Query sql table and get the change in followers for selected stream
    input: channel_name, start_time
    output: follower_change (int)
    """
     # set streamer name and datetime for now
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    new_followers_query =  '''
                    with starting_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {} 
                        order by date asc
                        limit 1)

                    ,ending_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        order by date desc
                        limit 1
                        )

                    select * from starting_followers
                    UNION ALL select * from ending_followers

                    '''.format(channel_name, start_time, channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(new_followers_query)
    follower_count = cursor_obj.fetchall()
    follower_count_pct = round((100 * (follower_count[0][0] - follower_count[1][0]) / follower_count[1][0]))
    conn.commit()
    conn.close()
    
    return follower_count_pct

def get_average_view_count(channel_name, start_time):
    """
    Query sql table and get the average number of viewers for selected stream
    input: channel_name, start_time
    output: view_count (int)
    """
    
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    average_views_query = '''
                        select round(avg(viewer_count)) as avg_viewers
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        '''.format(channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(average_views_query)
    view_count = cursor_obj.fetchall()
    conn.commit()
    conn.close()  

    return view_count[0][0] 

def get_message_count(channel_name, start_time):
    """
    Query sql table and get the total number of chats for selected stream
    input: channel_name, start_time
    output: message_count (int)
    """
    
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    total_messages_query = '''
                        select count(*) as total_messages
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        '''.format(channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(total_messages_query)
    message_count = cursor_obj.fetchall()
    conn.commit()
    conn.close()  


    return message_count[0][0]

def get_average_sentiment(channel_name, start_time):
    """
    Query sql table and get the average sentiment for selected stream
    input: channel_name, start_time
    output: average_sentiment (float)
    """
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    average_sentiment_query = '''
                        select avg(message_sentiment) as total_messages
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        '''.format(channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(average_sentiment_query)
    average_sentiment = cursor_obj.fetchall()
    conn.commit()
    conn.close()  


    return average_sentiment[0][0] 

def get_pct_positive_negative(channel_name, start_time):
    """
    Query sql table and get the percentage of positive, negative, and neutral chats
    for selected stream
    input: channel_name, start_time
    output: pct_positive, negative, neutral
    """
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    sentiment_pct_query = '''
                        with positive_chats as (select count(*) as chat_count
                                                from chats_table_demo
                                                where channel_name = {} 
                                                and stream_date = {} 
                                                and message_sentiment > 0)
                            ,negative_chats as (select count(*) as chat_count
                                                from chats_table_demo
                                                where channel_name = {} 
                                                and stream_date = {} 
                                                and message_sentiment < 0)
                            ,neutral_chats as (select count(*) as chat_count
                                                from chats_table_demo
                                                where channel_name = {} 
                                                and stream_date = {} 
                                                and message_sentiment = 0)
                            select * from positive_chats
                            UNION ALL select * from negative_chats
                            UNION ALL select * from neutral_chats       
                        '''.format(channel_name, start_time,channel_name, start_time,channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(sentiment_pct_query)
    sentiment_counts = cursor_obj.fetchall()
    total_chats = sentiment_counts[0][0] + sentiment_counts[1][0] + sentiment_counts[2][0]
    positive_chats = round( 100 * (sentiment_counts[0][0] / total_chats))
    negative_chats = round(100* (sentiment_counts[1][0] / total_chats))
    neutral_chats = round(100 * (sentiment_counts[2][0] / total_chats))
    chat_percentages = """Positive Chats: {}% 
                        Negative Chats: {}%
                        Neutral Chats: {}%""".format(positive_chats, negative_chats, neutral_chats)
    conn.commit()
    conn.close()  


    return chat_percentages 

def get_average_chatters(channel_name, start_time):
    """
    Query sql table and get the average number of chatters for selected stream
    input: channel_name, start_time
    output: average_chatters (float)
    """
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    
    conn = sqlite3.connect(con_string)
    
    average_chatters_query = '''
                        select avg(chatter_count) as average_chatters
                        from chats_table_demo
                        where channel_name = {} and stream_date = {}
                        '''.format(channel_name, start_time)
    
    cursor_obj = conn.cursor()
    cursor_obj.execute(average_chatters_query)
    average_chatters = cursor_obj.fetchall()
    conn.commit()
    conn.close()  


    return average_chatters[0][0] 

def recommendation(row,sorted_choices):
    '''
    Basic recommendation engine. Each normalized category divided by the seconds spent times the weight. 

    Current weight configuration: 
    35% Sentiment Value
    30% Subs Gained
    25% Followers Gained
    10% Views
    '''
    value = ((0.10 * (row['avg_viewers'])/row['time']) 
            + (0.25 * (row['followers_change'])/row['time']) 
            + (0.30 * (row['subscriber_change'])/row['time']) 
            + (0.35 * (row['average_sentiment'])/row['time']))
    return value


def recommender_engine(channel_name, start_time, sorted_choices):
    """ Queries sql table to get new followers, new subscribers, average viewers,
        average sentiment, and time by category. Runs the recommendation engine and
        outputs results.
        intput: channel_name, start_time
        output: recommendation_dict
    """
    channel_name = '\'' + channel_name + '\''
    start_time = '\'' + start_time + '\''
    conn = sqlite3.connect(con_string)


    distinct_topics_query = '''
                        select distinct stream_topic 
                        from chats_table_demo
                        where channel_name = {} 
                        and stream_date = {}
                    '''.format(channel_name, start_time)

    cursor_obj = conn.cursor()
    cursor_obj.execute(distinct_topics_query)
    topics = cursor_obj.fetchall()
    print(topics)
    followers_list = []
    subscriber_list = []
    for topic in topics:
        query_topic = '\'' + topic[0] + '\''
        new_followers_query =  '''
                    with starting_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {} 
                        and stream_date = {} 
                        and stream_topic = {} 
                        order by date asc
                        limit 1)

                    ,ending_followers as (
                        select follower_count
                        from chats_table_demo
                        where channel_name = {}
                        and stream_date = {}
                        and stream_topic = {} 
                        order by date desc
                        limit 1
                        )

                    select * from starting_followers
                    UNION ALL select * from ending_followers
                    '''.format(channel_name, start_time, query_topic, channel_name, start_time, query_topic)
        cursor_obj = conn.cursor()
        cursor_obj.execute(new_followers_query)
        follower_count = cursor_obj.fetchall()
        follower_change = follower_count[1][0] - follower_count[0][0]
        followers_list.append(follower_change)

        new_subscriber_query =  '''
                    with starting_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {} 
                        and stream_date = {} 
                        and stream_topic = {} 
                        order by date asc
                        limit 1)

                    ,ending_subscribers as (
                        select subscriber_count
                        from chats_table_demo
                        where channel_name = {}
                        and stream_date = {}
                        and stream_topic = {} 
                        order by date desc
                        limit 1
                        )

                    select * from starting_subscribers
                    UNION ALL select * from ending_subscribers

                    '''.format(channel_name, start_time, query_topic, channel_name, start_time, query_topic)
        cursor_obj = conn.cursor()
        cursor_obj.execute(new_subscriber_query)
        subscriber_count = cursor_obj.fetchall()
        subscriber_change = subscriber_count[1][0] - subscriber_count[0][0]
        subscriber_list.append(subscriber_change)
        
    grouped_stream_query = '''with grouped_stream as (
                select channel_name, 
                stream_topic, 
                avg(viewer_count) as avg_viewers, 
                max(stream_length) as max_minutes,
                min(stream_length) as min_minutes,
                round(avg(message_sentiment),2) as average_sentiment
                from chats_table_demo
                where channel_name = {}
                and stream_date = {}
                group by channel_name, stream_topic
                )
                select channel_name,
                stream_topic,
                round(avg_viewers) as avg_viewers, 
                average_sentiment,
                (max_minutes - min_minutes) as time
                from grouped_stream
                
                '''.format(channel_name, start_time)
    
    df = pd.read_sql_query(grouped_stream_query, conn)
    df['subscriber_change'] = np.array(subscriber_list)

    df['followers_change'] = np.array(followers_list)

    # df = df.append(pd.DataFrame({'channel_name':['random', 'random', 'random', 'random'], 'stream_topic':['VALORANT', 'POLITICS', 'MINECRAFT', 'MULTIVERSUS'] , \
    #                             'avg_viewers':[1000, 1040, 1100, 2000], 'average_sentiment':[0.4, 0.14, 0.87, 0.54], 'time':[8, 3, 5, 6], 'subscriber_change':[500, 799, -200, 1230], 'followers_change':[25, 94, 12, 73]}))

    df.loc[:,'Topic'] = df['stream_topic']
    df.loc[:,'Avg viewers'] = df['avg_viewers']
    df.loc[:,'Avg sentiment'] = df['average_sentiment']
    df.loc[:,'Subscriber Δ'] = df['subscriber_change']
    df.loc[:,'Followers Δ'] = df['followers_change']

    # df = df.sample(4)
    # topics = [1, 2, 3, 5, 5]
    
    if len(topics) > 1:
        for col in ['avg_viewers','average_sentiment','subscriber_change','followers_change']:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        # df['Score'] = df.apply(recommendation, args=(sorted_choices), axis = 1, ) --> this was hard to use because of multiple **kwargs
        df = df.fillna(0)
        scores = sorted_choices.split(',')
        # print(scores)
        df.loc[:, 'Score %'] = [(i*.35 + i*.30 + k*.25 + l*.10)/time for i, j, k, l, time in zip(df[scores[0]], df[scores[1]], df[scores[2]], df[scores[3]], df['time'])]
    else:
        df['Score %'] = 100
     
    df['Score %'] = ((df['Score %']/df['Score %'].sum())*100).round(decimals=1)
    conn.commit()
    conn.close()

    pd.set_option('colheader_justify', 'left')
    # df['Score'] =  '<b>' + df['Score'].astype(str) + '%</b>'

    return df[['Topic','Avg viewers','Avg sentiment','Subscriber Δ','Followers Δ', 'Score %']].\
        sort_values(by=['Score %'], ascending=False).\
                to_html(classes='table table-stripped', index=False)

