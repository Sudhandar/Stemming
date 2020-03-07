import pandas as pd

def only_middle(stem_data,data):
    
    """
    stem: -bol-
    
    does not identify the following,
        sample boloterm
        sambol random
    identifies the foloowing,
        ganbolo random
        random ganbolo
   
    """
    
    center_hits=pd.DataFrame()
    center = stem_data[stem_data['stem'].str.contains("^\-(.*)\-$",regex=True)]
    center['stem']= center['stem'].str.replace("-","",regex=True)
    for i in range(len(center)):
        center_terms = "[^ ]+("+ str(center.iloc[i]['stem'])+")[^ ]+"
        df = data[data['term'].str.contains(center_terms,regex=True,na=False)] 
        df['stem']=center.iloc[i]['stem']
        center_hits = center_hits.append(df)
    center_hits['stem']=center_hits['stem'].apply(lambda x: '-'+str(x)+'-')
    
    return center_hits

def middle(stem_data,data):
    
    """
    stem: -bol-
    identifies the following,
        ganbolo random
        random ganbolo
        sample boloterm
        sambol random
        ranbolterm
    """

    center_hits=pd.DataFrame()
    center = stem_data[stem_data['stem'].str.contains("^\-(.*)\-$",regex=True)]
    center['stem']= center['stem'].str.replace("-","",regex=True)
    for i in range(len(center)):
        center_terms = ".+("+ str(center.iloc[i]['stem'])+").+"
        df = data[data['term'].str.contains(center_terms,regex=True,na=False)] 
        df['stem']=center.iloc[i]['stem']
        center_hits = center_hits.append(df)
    center_hits['stem']=center_hits['stem'].apply(lambda x: '-'+str(x)+'-')
    
    return center_hits

def starts(stem_data,data):
    """
    stem: ran-
    
    identifies the following,
        random word
        randomint
    does not identify the following,
        second random
    
    """
        
    
    begin_hits = pd.DataFrame()
    begin = stem_data[stem_data['stem'].str.contains("^[a-z]+\-$",regex=True)]
    begin['stem'] = begin['stem'].str.replace("-","",regex=True)

    for i in range(len(begin)):
        begin_terms = "^"+str(begin.iloc[i]['stem'])
        df = data[data['term'].str.contains(begin_terms,regex=True,na=False)] 
        df['stem']=begin.iloc[i]['stem']
        begin_hits = begin_hits.append(df)
    begin_hits['stem']=begin_hits['stem'].apply(lambda x: str(x)+'-')

    return begin_hits

def ends(stem_data,data):
    """
    stem: -end
    identifies the following,
        blend
        second blend
        
    does not identify,
        blend random
    """
    
    
    end_hits = pd.DataFrame()
    end = stem_data[stem_data['stem'].str.contains(r'^\-[a-z]+',regex=True)]
    end = end[end['stem'].str[-1]!='-']
    end['stem'] = end['stem'].str.replace("-","",regex=True)
    
    for i in range(len(end)):
        end_terms = ".+("+str(end.iloc[i]['stem'])+")$"
        df = data[data['term'].str.contains(end_terms,regex=True,na=False)] 
        df['stem']=end.iloc[i]['stem']
        end_hits = end_hits.append(df)
    end_hits['stem']=end_hits['stem'].apply(lambda x: '-'+str(x))
    
    return end_hits

def stemming(stem_data,data):
    
    start=starts(stem_data,data)
    middle=only_middle(stem_data,data)
    end=ends(stem_data,data)
    
    output=pd.concat([start,middle,end])
    
    return start,middle,end,output
    
data = pd.read_csv("df_roots.csv")
data=data.drop_duplicates()
stem_data = pd.read_csv("usan_stems.csv")
starting,middle_hits,ending,output=stemming(stem_data,data)

test=starts(stem_data,data)

output.to_csv("hits_output.csv",index=False)
    
    
    