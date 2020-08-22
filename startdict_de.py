from pathlib import Path

from pystardict import Dictionary

dir_path = Path(r"data\stardict-dict-de\stardict-fundset_KDIC_decn-2.4.2")

dir_path = Path(r"data\stardict-dict-de\stardict-fundset_german2cs-2.4.2")


# dict_de = Dictionary(dir_path / "xindehan")
# dict_de = Dictionary(dir_path / "fundset_KDIC_decn")
dict_de = Dictionary(dir_path / "fundset_german2cs")

# dict_de.dict["machen"]  #
dict_de.dict["tun"]  #

# In [232]: dict_de.dict["los"]
# Out[232]: 'adj. 宽松的。不牢固的。自由的。松散的。不连贯的。<BR>adv. 离开海底。轻率地。松弛地。疏忽地。懒散地。<BR>interj. 加油。前进！哟嗬！'