import random

class Agent:
    def __init__(self, name, mood):
        self.mood = mood
        self.name =  name

    def encoder(self, message):
        
        if self.mood == "happy":
            return message + ":)"
        elif self.mood == "angry":
            return message.upper() + "!!! >:("
        else:
            return message

    def decoder(self, message):

        if '!' in message:
            return 'Feels angry'
        elif ':)' in message:
            return 'Feels happy'
        else:
            return 'Neutral'

def chatloop(agent1, agent2, messages):
    for msg in messages:
        sent_msg = agent1.encoder(msg)
        print(f"{agent1.name} says: {sent_msg}")
        interpretation = agent2.decoder(sent_msg)
        print(f"{agent2.name} interprets: {interpretation}\n")

        # Swap Role
        agent1, agent2 = agent2, agent1

zul = Agent("Zul", "happy")
pais = Agent("Pais", "angry")
messages = ["Can you finish the report today?", "I think we need a break", "Let's meet tomorrow"]

chatloop(zul, pais, messages)

    
