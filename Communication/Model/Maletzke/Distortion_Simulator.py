import dataclasses as dcs
from datetime import datetime, UTC
import uuid 
import numpy as np

def create_message(text, truth=1.0, emotion=0.2, complexity=0.8):
    
    return {
        "id":str(uuid.uuid4()),
        "text":text,
        "truth":max(0.0, min(truth, 1.0)),
        "emotion":max(0.0, min(emotion, 1.0)),
        "complexity":max(0.0, min(complexity, 1.0)),
        "timestamp":datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S"),
        "history":[
            {
                "stage":"created",
                "truth":truth,
                "emotion":emotion,
                "complexity": complexity,
                "text": text
            }
        ]
    }

def sender_pressure(msg, fear=0.6, ideology=0.7, role_expectation=0.5):
    
    # Apply fear: reduce truth, increase emotion
    fear_emotion_boost = fear * np.random.uniform(0.15, 0.35)
    fear_truth_penalty = fear * np.random.uniform(0.1, 0.25)
    msg['emotion'] = min(1.0, msg["emotion"] + fear_emotion_boost)
    msg['truth'] = max(0.0, msg["truth"] - fear_truth_penalty)

    # Apply ideology bias: change text framing
    ideology_emotion_boost = ideology * np.random.uniform(0.1, 0.3)
    ideology_truth_penalty = ideology * np.random.uniform(0.05, 0.15)
    msg["emotion"] = min(1.0, msg["emotion"] + ideology_emotion_boost)
    msg["truth"] = max(0.0, msg["truth"] - ideology_truth_penalty)

    if ideology > 0.3:
        if "inflation" in msg['text'].lower():
            msg["text"] = f"Experts warn: Rising inflation is hitting households hard today"
        else:
            msg["text"] = f"Breaking: {msg['text']} could favor certain groups"

    # Apply role expectation: simplify or exaggerate
    complexity_penalty = role_expectation * np.random.uniform(0.1, 0.4)
    msg["complexity"] = max(0.0, msg["complexity"] - complexity_penalty)
    
    if role_expectation > 0.5:
        msg["text"] += ", Hurting families everywhere!"

    # Track history
    msg["history"].append({
        "stage": "sender_pressure",
        "truth": msg["truth"],
        "emotion": msg["emotion"],
        "complexity": msg["complexity"],
        "text": msg["text"]
    })
 
    return msg

def self_censorship(msg, fear=0.5, peer_pressure=0.6, legal_risk=0.3):
    # Applies realistic self-censorship effects on message.
    censorship_factor = np.random.uniform(0.1, 0.3)  
    total_pressure = fear * 0.4 + peer_pressure * 0.35 + legal_risk * 0.25

    msg["truth"] = max(0.0, msg["truth"] - total_pressure * censorship_factor)
    msg["complexity"] = max(0.0, msg["complexity"] - total_pressure * censorship_factor * 1.2)

    if total_pressure > 0.5:
        msg["text"] = f"Partial report: {msg['text'].split(':')[-1].strip()} – certain details removed due to sensitivity"
    
    msg["history"].append({
        "stage": "self_censorship",
        "truth": msg["truth"],
        "emotion": msg["emotion"],
        "complexity": msg["complexity"],
        "text": msg["text"]
      })

    return msg

def framing_bias(msg, ideology=0.3, sensationalism=0.4, narrative_focus=0.4):
    # Applies realistic framing bias effects.
    
    #  Boost emotion for sensationalism
    msg["emotion"] = min(1.0, msg["emotion"] + sensationalism * np.random.uniform(0.1, 0.4))

    # Slight truth penalty for framing bias
    msg["truth"] = max(0.0, msg["truth"] - (ideology * 0.15 + narrative_focus * 0.1))

    # Reduce complexity for simplified narrative
    msg["complexity"] = max(0.0, msg["complexity"] - narrative_focus * np.random.uniform(0.05, 0.2))

    if sensationalism >= 0.5:
        msg["sensationalism"] = f"Breaking News: {msg['text']}"
    if ideology >= 0.3:
         msg["text"] = f"Government policy blamed, {msg['text']}"
    if narrative_focus >= 0.5:
        msg["text"] += " – key points emphasized for impact"
    
    msg["history"].append({
        "stage": "framing_bias",
        "truth": msg["truth"],
        "emotion": msg["emotion"],
        "complexity": msg["complexity"],
        "text": msg["text"]
      })

    return msg

def run_simulator(text):
    
    msg = create_message(text)
    pressure = sender_pressure(msg)
    censorship = self_censorship(msg)
    framing = framing_bias(msg)

    return msg

text = "Inflation increased by 3%"
run_simulator(text)
