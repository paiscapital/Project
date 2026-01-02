'''
Logic Algo
Network = audience mapping (who receives the message).
Source = sender node (creates original message).
Channel = medium of distribution (mass or selective).
E2 or next receivers = secondary propagation (how message spreads further).
Noise = misinterpretation, distortion, or failure to decode. if random < noise_level = distort else get message
'''
import networkx as nx
import random as rd

eml = {
    'Receiver1':['TV', 0.2],
    'Receiver2':['Radio', 0.4],
    'Receiver3':['Newspaper', 0.6],
    'Receiver4': ['News', 0.3],
    'Receiver5': ['Social Media', 0.02],
    'Receiver6': ['Thirdparty', 0.7],
    'Receiver7': ['Others', 0.9],
}

def nodes(E, EML):
    G = nx.DiGraph()
    G.add_node(E)
    for ER, value in EML.items():
        G.add_edge(E, ER, channel=value[0], noise=value[1])
    return G

E = str('Sender')
gnodes = nodes(E, eml)
M = 'propaganda to shape our society, dont trust that emotion shaping they give!'

def send_mess(gnodes, E, M):
    for rcv in gnodes.successors(E):
        edge = gnodes[E][rcv]
        noise = edge.get('noise', 0)

        if rd.random() < noise:
            dlvr_mess = f"Corrupted message {chr(rd.randint(33, 126))}"

        else:
            dlvr_mess = M

        print(f"{rcv} get message via channel {edge.get('channel')} : {dlvr_mess}")

print(f'{"="*10}Gerbner General Model{"="*10}\n')
send_mess(gnodes, E, M)
