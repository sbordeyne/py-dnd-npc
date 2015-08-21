# py-dnd-npc

NPC generator for Dungeons and Dragons.

Just call generate_npc(alignment, gender, race, class_, level, stats) to have a string being the generated NPC.

alignment : Any, Any Lawful/Neutral/Chaotic, Lawful Good/Neutral/Evil etc
gender : Male or Female
Race : Elf, Human, Dwarf, Any, Halfelin
class_ : Warrior, Wizard, Thief, Cleric, Any
level : integer
stats : Best 3 of 5d6, Low, Average, High

It generates beliefs, class, race, name, belongings, AC, motivations, recent past, characteristics, laguages and alignment

Beliefs are determined according to alignment : 'or' or 'on' in god name = lawful, 'sh' 'k' 'y', 'x' in god name = chaotic, anything else = neutral


AC rules are the ones of OD&D, you'll need to adapt if you want 3.5+ characters. (no big deal actually)
