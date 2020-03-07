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
    
    center_drugs=pd.DataFrame()
    center = stem_data[stem_data['stem'].str.contains("^\-(.*)\-$",regex=True)]
    center['stem']= center['stem'].str.replace("-","",regex=True)
    for i in range(len(center)):
        center_terms = "[^ ]+("+ str(center.iloc[i]['stem'])+")[^ ]+"
        df = data[data['term'].str.contains(center_terms,regex=True,na=False)] 
        df['stem']=center.iloc[i]['stem']
        center_drugs = center_drugs.append(df)
    center_drugs['stem']=center_drugs['stem'].apply(lambda x: '-'+str(x)+'-')
    
    return center_drugs

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

    center_drugs=pd.DataFrame()
    center = stem_data[stem_data['stem'].str.contains("^\-(.*)\-$",regex=True)]
    center['stem']= center['stem'].str.replace("-","",regex=True)
    for i in range(len(center)):
        center_terms = ".+("+ str(center.iloc[i]['stem'])+").+"
        df = data[data['term'].str.contains(center_terms,regex=True,na=False)] 
        df['stem']=center.iloc[i]['stem']
        center_drugs = center_drugs.append(df)
    center_drugs['stem']=center_drugs['stem'].apply(lambda x: '-'+str(x)+'-')
    
    return center_drugs

def starts(stem_data,data):
    """
    stem: ran-
    
    identifies the following,
        random word
        randomint
    does not identify the following,
        second random
    
    """
        
    
    begin_drugs = pd.DataFrame()
    begin = stem_data[stem_data['stem'].str.contains("^[a-z]+\-$",regex=True)]
    begin['stem'] = begin['stem'].str.replace("-","",regex=True)

    for i in range(len(begin)):
        begin_terms = "^"+str(begin.iloc[i]['stem'])
        df = data[data['term'].str.contains(begin_terms,regex=True,na=False)] 
        df['stem']=begin.iloc[i]['stem']
        begin_drugs = begin_drugs.append(df)
    begin_drugs['stem']=begin_drugs['stem'].apply(lambda x: str(x)+'-')

    return begin_drugs

def ends(stem_data,data):
    """
    stem: -end
    identifies the following,
        blend
        second blend
        
    does not identify,
        blend random
    """
    
    
    end_drugs = pd.DataFrame()
    end = stem_data[stem_data['stem'].str.contains(r'^\-[a-z]+',regex=True)]
    end = end[end['stem'].str[-1]!='-']
    end['stem'] = end['stem'].str.replace("-","",regex=True)
    
    for i in range(len(end)):
        end_terms = ".+("+str(end.iloc[i]['stem'])+")$"
        df = data[data['term'].str.contains(end_terms,regex=True,na=False)] 
        df['stem']=end.iloc[i]['stem']
        end_drugs = end_drugs.append(df)
    end_drugs['stem']=end_drugs['stem'].apply(lambda x: '-'+str(x))
    
    return end_drugs

def stemming(stem_data,data):
    
    start=starts(stem_data,data)
    middle=only_middle(stem_data,data)
    end=ends(stem_data,data)
    
    output=pd.concat([start,middle,end])
    
    return start,middle,end,output
    
data = pd.read_csv("df_roots.csv")
data=data.drop_duplicates()
stem_data = pd.read_csv("usan_stems.csv")
s,m,e,out=stemming(stem_data,data)

test=starts(stem_data,data)

output_file_name = "drugs_missing_usan_stems"
    
    
    