from nim1 import train, play

ai = train(10000)
print(ai.q[(1,2,0,0),(1,2)])
print(ai.q[(0,1,2,0),(2,2)])
print(ai.q[(0,0,1,2),(3,2)])

print(ai.q[(1,2,0,0),(0,1)])
print(ai.q[(0,1,2,0),(1,1)])
print(ai.q[(0,0,1,2),(2,1)])

print(ai.q[(1,3,5,7),(0,1)])
print(ai.q[(1,3,5,7),(3,1)])

# print(ai.q)

# print(len(ai.q))

play(ai)
