headWind = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

for i in range (4, len(headWind), 10):
    x = i + 10
    s = sum(headWind[i:x])
    print (s)