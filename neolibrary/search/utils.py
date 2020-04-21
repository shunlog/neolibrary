def str_to_regexp(str):

        regexp = str.replace('a', '[aâă]').replace('A', '[AÂĂ]').replace('t', '[tț]').replace('T', '[TȚ]').replace('s', '[sș]').replace('S', '[SȘ]').replace('i', '[iȋ]').replace('I', '[IȊ]')
        regexp = "(?i).*" + regexp + ".*"
        return regexp
