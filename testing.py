import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors
indices = pickle.load(open('book.pkl','rb'))
model= pickle.load(open('model.pkl','rb'))
book=pickle.load(open('category.pkl','rb'))

def rcmd(book_name):
    book_id = np.where(indices.index==book_name)[0][0]
    distances,suggestions=model.kneighbors(indices.iloc[book_id,:].values.reshape(1,-1),n_neighbors = 11)
    books=[]
    for i in range(len(suggestions)):
        if i==0:
            print("The suggestions for ",book_name,"are : ")
        if not i:
            books = indices.index[suggestions[i]]
    for i in range(1,len(books)):
            print(str(i) + ": " + books[i] )

    return books

def build_chart(genre):
    df = book[book['Category'] == genre]
    qualified = df[(df['votecount'] <= 100) & (df['votecount'].notnull()) & 
                   (df['vote average'].notnull())][['Title', 'votecount', 'vote average', 
                                                'Copies', 
                                                'Authorname','RackNo']]
    qualified['votecount'] = qualified['votecount'].astype('int')
    qualified['RackNo'] = qualified['RackNo'].astype('int')
    qualified.sort_values([ 'votecount'], 
                        axis=0,
                        ascending=[True], 
                        inplace=True)                                          
    result={}
    authors=[]
    titles =[]
    Rack=[]
    vc=[]
    result = qualified.head(10).reset_index()
    for i in range(len(result)): 
        authors.append(result.Authorname[i])
        titles.append(result.Title[i])
        Rack.append(result.RackNo[i])
        vc.append(result.votecount[i])
    return authors,titles,Rack,vc

