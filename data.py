import json
from help import pretty_print
from nlph import * 

def parse_dms(sender, receiver): 
    PATH = "./sample/" + receiver 

    with open(PATH) as json_data:
        data = json.load(json_data)

    participants = [list(elem.values())[0] for elem in data['participants']]
    receiver = participants[0]; sender = participants[1] #p1 = sender, p2 = receiver

    """

    Parse through file, extract all relevant information from messages

    """

    stats = {
        "first_n_last" : { 
                            "message_first_content" : None, 
                            "message_first_sender" : None, 
                            "message_first_time" : None, 
                            "message_last_content" : None, 
                            "message_last_sender" : None,
                            "message_last_time" : None, 
                        }, 
        
        "total_metrics" : { 
                            "message_count_p1" : 0, 
                            "message_count_p2" : 0,  
                            "message_len_p1" : [], 
                            "message_len_p2" : [], 
                            "reaction_count_p1" : 0, 
                            "reaction_count_p2" : 0, 
                        }, 
        
        "time_metrics" : { 
                            "time_gap_p1" : [], 
                            "time_gap_p2" : [], 
                        }, 
        
        "text_strings" : { 
                            "reactions_p1" : [], 
                            "reactions_p2" : [], 
                            "raw_text_p1" : [], 
                            "raw_text_p2" : []
                        }, 
        "messages_total" : 0
    }


    prev_sender = None 
    prev_time = None 
    raw_texts = [] 

    for message in data['messages']: 

        try: 
            content = message["content"]
        except: 
            stats["messages_total"] += 1
            continue # Means no content in message (image, post, vid, etc)

        try: 
            link = message["share"]
            stats["messages_total"] += 1
            continue 
        except: 
            pass 

        if not prev_sender: prev_sender = message["sender_name"]

        if "to your message" in message["content"] or message["type"] != "Generic": 
            stats["messages_total"] += 1
            continue # Means no content in message (image, post, vid, etc)

        # Store first message sent 

        if stats["messages_total"] + 5 >= len(data["messages"]):
            stats["first_n_last"]["message_first_content"] = message["content"]
            stats["first_n_last"]["message_first_sender"] = message["sender_name"]
            stats["first_n_last"]["message_first_time"] = message["timestamp_ms"]


        # Update count of number of messages each person sent

        if sender in message["sender_name"]: 
            stats["total_metrics"]["message_count_p1"] += 1

        if receiver in message["sender_name"]: 
            stats["total_metrics"]["message_count_p2"] += 1


        # Update reactions, type of reaction, if any (can be empty)

        try: 
            for reaction in message["reactions"]: 
                if sender in reaction["actor"]: 
                    stats["total_metrics"]["reaction_count_p1"] += 1
                    stats["text_strings"]["reactions_p1"].append(reaction["reaction"])
                
                if receiver in reaction["actor"]: 
                    stats["total_metrics"]["reaction_count_p2"] += 1
                    stats["text_strings"]["reactions_p2"].append(reaction["reaction"])
        
        except: 
            pass # Means no reactions were present in the message


        # Store each person's text in string (so can parse later) 

        if sender in message["sender_name"]: 
            stats["text_strings"]["raw_text_p1"].append(message["content"])

        if receiver in message["sender_name"]: 
            stats["text_strings"]["raw_text_p2"].append(message["content"])


        # Update length of messages sent at a time (if sender changed)

        if prev_sender != message["sender_name"]: 
            if sender in message["sender_name"]: 
                raw_stats = [len(msg) for msg in raw_texts]
                stats["total_metrics"]["message_len_p1"].append(raw_stats)
                raw_texts = []
            if receiver in message["sender_name"]: 
                raw_stats = [len(msg) for msg in raw_texts]
                stats["total_metrics"]["message_len_p2"].append(raw_stats)
                raw_texts = []
        else: 
            raw_texts.append(message["content"])
            

        # Compute time between responses (if sender changed, gap time)

        if prev_sender != message["sender_name"]: 
            if sender in message["sender_name"]: 
                stats["time_metrics"]["time_gap_p1"].append(message["timestamp_ms"] - prev_time)
            if receiver in message["sender_name"]: 
                stats["time_metrics"]["time_gap_p2"].append(message["timestamp_ms"] - prev_time)


        # Store last message sent 

        if stats["messages_total"] == 0: 
            stats["first_n_last"]["message_last_content"] = message["content"]
            stats["first_n_last"]["message_last_sender"] = message["sender_name"]
            stats["first_n_last"]["message_last_time"] = message["timestamp_ms"]

        prev_sender = message["sender_name"]
        prev_time = message["timestamp_ms"]

        stats["messages_total"] += 1


    """

    After parsing through file, we can dump var to stats.txt for backup

    """

    with open('stats.txt', 'w') as convert_file:
        convert_file.write(json.dumps(stats))

    #pretty_print(stats, sender, receiver)
    return stats 


"""

After parsing through file, use sentiment analysis/NLP text processing

"""

def gen_wordCloud(stats): 
    nlp_analyzer = NLPAnalysis(stats["text_strings"]["raw_text_p1"], stats["text_strings"]["raw_text_p2"])
    

def process_stats(stats, sender, receiver): 



    # Print out Word Cloud

    nlp_analyzer = NLPAnalysis(stats["text_strings"]["raw_text_p1"], stats["text_strings"]["raw_text_p2"])

    #nlp_analyzer.generateCloud("sender")
    #nlp_analyzer.generateCloud("receiver")
    nlp_analyzer.generateCloud("all")

    #nlp_analyzer.basicAnalysis("sender")
    #nlp_analyzer.basicAnalysis("receiver")
    nlp_analyzer.basicAnalysis("all")