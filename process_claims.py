
# coding: utf-8

# In[1]:


# pipeline to process "fact_checks_20180502.txt" to file
# the file is a python pickle containing the claims with its keywords and vectors


# In[2]:


from nlp_functions import *
import json


# In[3]:


fc_path = "fact_checks_20180502.txt"

with open(fc_path) as f:
    fc_raw = f.readlines()
    
print("No. of Claims:", len(fc_raw))


# In[4]:


claims_list = []

for fc in fc_raw[:300]:
    fc = fc.strip("\n")
    fc = fc.replace("</script>", "").replace('<script type="application/ld+json">', "")
    fc = json.loads(fc)
    claim = fc["claimReviewed"]
    claims_list.append(claim)


# In[5]:


print(claims_list[:10])


# In[6]:


import time

start_time = time.time()
processed_claims = process_claim_list(claims_list, debug=True)
print(time.time() - start_time)


# In[8]:


import pickle

with open('processed_claims.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(processed_claims, f, pickle.HIGHEST_PROTOCOL)


# In[ ]:


# # to load
# with open('processed_claims.pickle', 'rb') as f:
#     # The protocol version used is detected automatically, so we do not
#     # have to specify it.
#     processed_claims = pickle.load(f)

