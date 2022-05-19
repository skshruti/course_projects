import numpy as np
import matplotlib.pyplot as plt
 
d = {1: 84.571, 2: 11.244, 3: 33.782, 4: 12.689, 5: 16.003, 6: 33.701, 7: 101.672, 8: 23.587, 9: 15.581, 10: 29.015, 11: 28.904, 12: 19.154, 13: 39.59, 14: 19.951, 15: 30.209, 16: 23.391, 17: 38.722, 18: 80.421, 19: 24.21, 20: 76.125}
k = list(d.keys())
k = [str(v) for v in k]
v = list(d.values())
print(k,v)
fig = plt.figure(figsize = (10, 5))
 
plt.bar(k, v, color ='#69C9D0', width = 0.4)
 
plt.xlabel("Query number")
plt.ylabel("Time taken (in ms)")
plt.show()