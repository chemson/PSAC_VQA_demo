import pickle
data = pickle.load(open('Action_label2ans.pkl','rb'))
print(type(data))
print(len(data))
print(data)