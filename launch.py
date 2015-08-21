# -*- coding: utf-8 -*-
import random as rd

def generate_npc(alignment, gender, race, class_, level, stats):
    characteristics = {"str":0,"int":0,"wis":0,"dex":0,"con":0,"cha":0}
    npc_dict = read_config("npc-gen")
    if "Any" in alignment:
        try:
            assert alignment != "Any"
            alignment = alignment.split(" ")[1] + " " + rd.choice(["Good", "Neutral", "Evil"])
        except AssertionError:
            alignment = rd.choice(["Lawful", "Neutral", "Chaotic"]) + " " + rd.choice(["Good", "Neutral", "Evil"])
    if gender == "Any":
        gender = rd.choice(["Male", "Female"])
    if race == "Any":
        race = rd.choice(["Human", "Elf", "Dwarf", "Halfelin"])
    if class_ == "Any":
        class_ = rd.choice(["Warrior", "Wizard", "Thief", "Cleric"])
    if stats == "Best 3 of 5d6":
        for stat, stat_value in characteristics.items():
            dice_rolls=[]
            for i in range(5):
                dice_rolls.append(rd.randint(1,6))
            characteristics[stat] = sum(sorted(dice_rolls)[2:])
    elif stats == "Low":
        for stat, stat_value in characteristics.items():
            dice_rolls=[]
            dice_rolls.append(rd.randint(1,6))
            dice_rolls.append(rd.randint(1,6))
            characteristics[stat] = sum(dice_rolls)
    elif stats == "Average":
        for stat, stat_value in characteristics.items():
            characteristics[stat] = 6 + rd.randint(1,8)
    else:
        for stat, stat_value in characteristics.items():
            characteristics[stat] = 12 + rd.randint(1,6)

    name = get_npc_name(npc_dict, race, gender)
    languages = get_npc_languages(npc_dict, characteristics["int"], race, alignment)
    beliefs = get_npc_beliefs(npc_dict, alignment)
    recent_past, motivation = get_npc_motivation(npc_dict)
    npc_ac, belongings = get_npc_belongings(npc_dict, level, class_)
    life = dice_roll("{}d6+2".format(level))

    string_to_return = \
    """
    {}, {} {} {}, level {}, {} HP, {} AC\n
    Alignment : {}, believes in : {}\n
    Stats : 
    \tSTR : {}\n
    \tINT : {}\n
    \tWIS : {}\n
    \tDEX : {}\n
    \tCON : {}\n
    \tCHA : {}\n

    Language(s) spoken : {}

    Belongings : {}

    {}

    Recent Past : {}
    """.format(name.capitalize(), gender, class_, race, level, life, npc_ac, alignment, beliefs,\
    characteristics["str"], characteristics["int"], characteristics["wis"],\
    characteristics["dex"], characteristics["con"], characteristics["cha"],\
    languages, belongings, motivation, recent_past)
    return string_to_return

def get_npc_name(npc_dict, race, gender):
    race = race.lower()
    gender = gender.lower()
    names = npc_dict["{}_names".format(race)]
    preffixes = []
    intermediate = []
    suffixes = []
    if gender is "male" or gender is "m":
        gender = "m"
    else:
        gender = "f"
    for value_lists in names:
        if value_lists[0] == "{}pre".format(gender):
            preffixes.append(value_lists[1])
        else:
            preffixes.append(value_lists[1])
        if "{}suf".format(gender) == value_lists[0]:
            suffixes.append(value_lists[1])
        else:
            suffixes.append(value_lists[1])
        if "{}in".format(gender) == value_lists[0]:
            intermediate.append(value_lists[1])
        else:
            intermediate.append("")
    return rd.choice(preffixes) + rd.choice(intermediate) + rd.choice(suffixes)

def get_npc_languages(npc_dict, intelligence, race, alignment):
    languages = "Common, {}".format(alignment.capitalize())
    available_languages = npc_dict["languages"]
    nbr = 0
    if intelligence >= 17:
        nbr += 2
    elif 17 > intelligence >= 14:
        nbr += 1
    elif 9 > intelligence >= 6:
        return "Common spoken with difficulties"
    elif 6 > intelligence >= 3:
        return "Can't read common, speaks with a lot of trouble"
    if race.lower() is not "human":
        languages += ", {}".format(race.capitalize())
        available_languages.remove(race.lower())
    for i in range(nbr):
        lang = rd.choice(available_languages)
        available_languages.remove(lang)
        languages += ", {}".format(lang.capitalize())
    return languages

def get_npc_beliefs(npc_dict, alignment):
    gods = npc_dict["churches"]
    law_gods = []
    neu_gods = []
    cha_gods = []
    for god in gods:
        if "on" in god or "or" in god:
            law_gods.append(god)
        elif "k" in god or "sh" in god or "x" in god or "y" in god:
            cha_gods.append(god)
        else:
            neu_gods.append(god)
    if "Lawful" in alignment:
        return rd.choice(law_gods)
    elif "Chaotic" in alignment:
        return rd.choice(cha_gods)
    else:
        return rd.choice(neu_gods)

def get_npc_motivation(npc_dict):
    recent_past = replace_bracket_words(rd.choice(npc_dict["recent_past"]), npc_dict)
    motivation = replace_bracket_words(rd.choice(npc_dict["motivations"]), npc_dict)
    return recent_past, motivation

def replace_bracket_words(sentence, npc_dict):
    word = ""
    if "[" in sentence:
        word = sentence[sentence.index("[")+1:sentence.index("]")]
        sentence = sentence.replace("[{}]".format(word), rd.choice(npc_dict[word]), 1)
        return replace_bracket_words(sentence, npc_dict)
    else:
        return sentence

def read_config(file_name):
    """Function that reads the config of given filename, returns dict"""
    return_dict = dict()
    temp_list = list()
    with open("{}.cfg".format(file_name), "r") as config_file:
        for line in config_file:
            if "{" in line:
                name = line.split("{")[0]
            elif "}" in line:
                return_dict[name] = temp_list
                temp_list = []
            else:
                if ";" in line:
                    line = line.split("\n")[0]
                    to_append = line.split(";")
                else:
                    to_append = line.split("\n")[0]
                temp_list.append(to_append)
                del to_append
    return return_dict

def dice_roll(xdypz):
    """returns the result of a roll of dices in the form of a string "xdy+z" or "xdy-z" or "xdy" """
    number_of_dices = int(xdypz.split("d")[0])
    if "+" in xdypz:
        sides_of_dice = int(xdypz.split("d")[1].split("+")[0])
        modifier_of_dice = int(xdypz.split("d")[1].split("+")[1])
    elif "-" in xdypz:
        sides_of_dice = int(xdypz.split("d")[1].split("-")[0])
        modifier_of_dice = int(xdypz.split("d")[1].split("-")[1]) *(-1)
    else:
        sides_of_dice = int(xdypz.split("d")[1])
        modifier_of_dice = 0
    temp=[]
    for i in range(number_of_dices):
        temp.append(rd.randint(1,sides_of_dice))
    return sum(temp)+modifier_of_dice

def get_npc_belongings(npc_dict, level, npc_class):
    level = int(level)
    npc_belongings_value = int(level) * 100 * rd.gauss(1,0.5)
    weapons = []
    armors = []
    belongings = ""

    try:
        assert npc_belongings_value >= 0
        for i in range(int(level / 5) + 1):
            choose_weapon = rd.choice(npc_dict["weapon"])
            choose_armor = rd.choice(npc_dict["armor"])
            weapons.append(choose_weapon[0])
            armors.append(choose_armor[0])
            npc_belongings_value -= (int(choose_weapon[1]) + int(choose_armor[1]))
    except AssertionError:
        for armor in armors:
            belongings += armor + ", "
        belongings = belongings[:-2] + "\n"
        for weapon in weapons:
            belongings += weapon + ", "
        return belongings

    for armor in armors:
        belongings += armor + ", "
    belongings = belongings[:-2] + "\n"
    for weapon in weapons:
        belongings += weapon + ", "
    belongings = belongings[:-2] + "\n"
    while npc_belongings_value > 0:
        chosen_item = rd.choice(npc_dict["other"])
        belongings += chosen_item[0] + ", "
        npc_belongings_value -= int(chosen_item[1])
    belongings = belongings[:-2] + "\n"
    return get_npc_ac(armors, npc_class), belongings

def get_npc_ac(armors, npc_class):
    possible_ac = []
    owned_allowed_armors = []
    if "wizard" in npc_class.lower():
        allowed_armors = ["robe"]
    elif "warrior" in npc_class.lower():
        allowed_armors = ["robe", "leather armor", "chainmail armor", "plate armor"]
    elif  "thief" in npc_class.lower():
        allowed_armors = ["robe", "leather armor"]
    elif "cleric" in npc_class.lower():
        allowed_armors = ["robe", "leather armor", "chainmail armor"]
    else:
        return 9
    for allowed_armor in allowed_armors:
        for owned_armor in armors:
            if allowed_armor in owned_armor:
                owned_allowed_armors.append(owned_armor)
    for armor in owned_allowed_armors:
        try:
            bonus = int(armor.strip(" abcdefghijklmnopqrstuvwxyz+-*/."))
        except ValueError:
            bonus = 0
        if "robe" in armor:
            base_ac = 9
        elif "leather" in armor:
            base_ac = 7
        elif "chainmail" in armor:
            base_ac = 5
        elif "plate" in armor:
            base_ac = 3
        else:
            base_ac = 9
        possible_ac.append(base_ac - bonus)
    return min(possible_ac)