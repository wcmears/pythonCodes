def dmsToDD(inp):
    colon = 0
    degrees = ''
    minutes = ''
    seconds = ''
    for i in range(0,len(inp)):
        if colon == 0 and inp[i] != ':':
            degrees = degrees + inp[i]
        elif colon == 0 and inp[i] == ':':
            colon += 1
        elif colon == 1 and inp[i] != ':':
            minutes = minutes + inp[i]
        elif colon == 1 and inp[i] == ':':
            colon += 1    
        else:
            seconds = seconds + inp[i]
    degrees = float(degrees)
    degrees = degrees + (float(minutes)/60)
    degrees = degrees + (float(seconds)/3600)
    return degrees
    
print(dmsToDD('80:7:1'))