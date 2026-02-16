class Sortirovka:
    name_combo_spell = {
        ('Q',None,None,None,None) : ['stone',10,1],
        ('W', None, None, None, None): ['heal', 10, 1],
        ('E', None, None, None, None): ['shield', 10, 1],
    }

    @classmethod
    def check(cls,str_combo_list):
        if any(str_combo_list):
            if a := cls.name_combo_spell.get(str_combo_list):
                match a[0]:
                    case 'stone':
                        ...
                    case 'shield':
                        ...
                    case 'heal':
                        ...