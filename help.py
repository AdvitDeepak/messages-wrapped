import datetime, statistics

def ms_time(ms): 
    return datetime.datetime.fromtimestamp(ms/1000)

def num_days(date1, date2):
    return abs((date2-date1).days)




def pretty_print(stats, sender, receiver):

    print() 
    print("---------------------------- GENERAL  STATS ---------------------------")
    print(f"Showing history of: {sender} and {receiver}\n")
    print(f"Total messages sent: {stats['messages_total']}")
    print(f"   Sent by {sender}: {stats['total_metrics']['message_count_p1']}")
    print(f"   Sent by {receiver}: {stats['total_metrics']['message_count_p2']}\n")
    print(f"Days of talking: {num_days(ms_time(stats['first_n_last']['message_last_time']), ms_time(stats['first_n_last']['message_first_time']))}")

    print()
    print()

    print("---------------------------- FIRST AND LAST ---------------------------")
    print(f"First message sent by: {stats['first_n_last']['message_first_sender']}")
    print(f"First message content: {stats['first_n_last']['message_first_content']}")
    print(f"First message sent on: {ms_time(stats['first_n_last']['message_first_time'])}")

    print() 

    print(f"Last message sent by: {stats['first_n_last']['message_last_sender']}")
    print(f"Last message content: {stats['first_n_last']['message_last_content']}")
    print(f"Last message sent on: {ms_time(stats['first_n_last']['message_last_time'])}")

    print() 
    print() 

    print("---------------------------- TEXTING STATS ---------------------------")
    #print(stats['total_metrics']['message_len_p1'])
    num_messages_once_p1 = [] 
    len_messages_once_p1 = []

    for msg in stats['total_metrics']['message_len_p1']: 
        num_messages_once_p1.append(len(msg))
        len_messages_once_p1.append(sum(msg))

    num_messages_once_p2 = [] 
    len_messages_once_p2 = []

    for msg in stats['total_metrics']['message_len_p2']: 
        num_messages_once_p2.append(len(msg))
        len_messages_once_p2.append(sum(msg))

    print(f"Avg # msgs at once by {sender}: {statistics.mean(num_messages_once_p1)}")
    print(f"Avg # msgs at once by {receiver}: {statistics.mean(num_messages_once_p2)}\n")
    print(f"Avg # chars at once by {sender}: {statistics.mean(len_messages_once_p1)}")
    print(f"Avg # chars at once by {receiver}: {statistics.mean(len_messages_once_p2)}")

    print() 
    print() 

    print("---------------------------- REACTION STATS ---------------------------")
    print(f"Total reactions by {sender}: {stats['total_metrics']['reaction_count_p1']}")
    print(f"Total reactions by {receiver}: {stats['total_metrics']['reaction_count_p2']}")
    print(f"Most used reaction by {sender}: {max(stats['text_strings']['reactions_p1'])}")
    print(f"Most used reaction by {receiver}: {max(stats['text_strings']['reactions_p2'])}")

    print() 
    print() 

    print("---------------------------- TIME GAP STATS ---------------------------")
    print(f"Avg time to respond by {sender}: {abs(statistics.mean(stats['time_metrics']['time_gap_p1']) / 1000 / 60)} min")
    print(f"Avg time to respond by {receiver}: {abs(statistics.mean(stats['time_metrics']['time_gap_p2']) / 1000 / 60)} min")