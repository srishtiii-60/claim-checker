TEST_TEXTS = [
    # 1. Simple fact
    "Tesla delivered 1.8 million vehicles in 2023.",

    # 2. Ek sentence mein do claims
    "Our startup has five million users and grew revenue by 80% last year.",

    # 3. Opinion (verify nahi hona chahiye)
    "I think this is the best phone ever made.",

    # 4. Prediction (verify nahi hona chahiye)
    "Electric cars will probably replace petrol cars by 2040.",

    # 5. Mixed: fact + opinion + prediction
    "India has over 1.4 billion people, which is amazing, and it will soon become the largest economy.",

    # 6. Hinglish / Hindi
    "भारत की जनसंख्या 140 करोड़ से ज़्यादा है, aur mujhe lagta hai ye bahut zyada hai.",
]

TEST_TEXTS = [
    # 1. Simple fact
    "Tesla delivered 1.8 million vehicles in 2023.",

    # 2. Ek sentence mein do claims
    "Our startup has five million users and grew revenue by 80% last year.",

    # 3. Opinion (verify nahi hona chahiye)
    "I think this is the best phone ever made.",

    # 4. Prediction (verify nahi hona chahiye)
    "Electric cars will probably replace petrol cars by 2040.",

    # 5. Mixed: fact + opinion + prediction
    "India has over 1.4 billion people, which is amazing, and it will soon become the largest economy.",

    # 6. Hinglish / Hindi
    "भारत की जनसंख्या 140 करोड़ से ज़्यादा है, aur mujhe lagta hai ye bahut zyada hai.",
]
EXPECTED = [
    # Text 1
    [("FACT", "Tesla delivered 1.8 million vehicles in 2023")],
    # Text 2
    [("FACT", "Startup has five million users"),
     ("FACT", "Startup grew revenue by 80% last year")],
    # Text 3
    [("OPINION", "This is the best phone ever made")],
    # Text 4
    [("PREDICTION", "Electric cars will replace petrol cars by 2040")],
    # Text 5
    [("FACT", "India has over 1.4 billion people"),
     ("OPINION", "This is amazing"),
     ("PREDICTION", "India will become the largest economy")],
    # Text 6
    [("FACT", "India's population is over 140 crore"),
     ("OPINION", "Population is too high")],
]