#-------------------
# LAB : 5
# Contributors - Anubhab Chakraborty(Roll - 2106306)
# Contributors - Akhil Thirukonda Sivakumar (Roll - 2103106)
#-------------------



import random,copy
from queue import Queue 



def extractinfo(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read the entire file content
            lines = file.readlines()
            #print(lines)
            first_line = lines[0].strip().split(', ')
            var_list = first_line[1:]
            tot_var = len(var_list)
            #print("Variable List : ",var_list)
            var_dict = {}
            for i in range(1,tot_var+1):
                line = lines[i].strip().split(', ')
                var = line[0]
                values = [x for x in line[1:]]
                var_dict[var] = values

            # for var, values in var_dict.items():
            #     print(f"Variable: {var}, Possible Values: {values}")

            var_parents = {}
            is_variable = False
            for line in lines:
                line = line.strip()
                if '|' in line and ':' not in line and '?' not in line:
                    is_variable = True
                    l = line.split(' |')
                    current_var = l[0]
                    var_parents[current_var]=[]
                    var = l[1].strip().split(',')
                if is_variable and line and ':' not in line and '?' not in line and '|' not in line:
                    
                    var_parents[current_var] = [x for x in var]

            print(var_parents)
            # Topo sort -------------------
            indegree = {var:0 for var in var_parents}
            for var in var_parents:
                l = var_parents[var]
                if(l[0]!=''):
                    indegree[var] = len(l)

            print(indegree)
            topo_sorted_var_parents={}
            qu = []

            for i in indegree:
                if(indegree[i]==0):
                    
                    qu.append(i)
            print(qu)
            adj_list = {var:[] for var in var_parents}
            for i in var_parents:
                for j in var_parents[i]:
                    print("print",j)
                    if(j==''):
                        break
                    adj_list[j].append(i)

            print(adj_list)

            while qu:
                var = qu.pop(0)
                topo_sorted_var_parents[var] = var_parents[var]

                for child in adj_list[var]:
                    indegree[child] -= 1
                    if indegree[child] == 0:
                        qu.append(child)

            print("Topologically sorted variables with their parents:")
            for var in topo_sorted_var_parents:
                print(f"{var}: {topo_sorted_var_parents[var]}")
            




            

            

            
            # for var, parents in var_parents.items():
            #     print(f"Variable: {var}, Parents: {parents}")

            cpt_dict = {}
            current_var = None
            for line in lines:
                line = line.strip()
                if '|' in line and ':' not in line and '?' not in line:
                    current_var = line.split(' |')[0]
                    #print(current_var)
                    cpt_dict[current_var] = {}

                if current_var and ':' not in line and '?' not in line and '|' not in line and line:
                    data = line.split(', ')
                    #print(data)
                    event = tuple(data[:-1])
                    s=""
                    for i in event:
                        s+=i
                    prob = float(data[-1])
                    cpt_dict[current_var][s] = prob

            print(cpt_dict)
            ucv_dict = {}
            cv_dict = {}
            query = [line for line in lines if line.startswith("Query")][0]
            query = query.split("Query: ")[1].strip()
            actquery = query[2:-1].replace(' ', '')
            variables = actquery.split('|')
            ucv = variables[0].split(',')
            cv  = variables[1].split(',')
            for j,i in enumerate(ucv):
                sut = i.split('=')
                ucv[j]=(sut[0],sut[1])

            for j,i in enumerate(cv):
                sut = i.split('=')
                cv[j]=(sut[0],sut[1])
            
            for i,j in ucv:
                ucv_dict[i] = j 

            for i,j in cv:
                cv_dict[i] = j 
            
            print(ucv_dict)
            print(cv_dict)
        # Displaying the CPTs for each variable
        # for var, cpt in cpt_dict.items():
        #     print(f"Variable: {var}, CPT:")
        #     for event, probability in cpt.items():
        #         print(f"    Event: {event}, Probability: {probability}")

                        




        return tot_var,topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict

            #print(file_content)
    except FileNotFoundError:
        print("The file does not exist or the path is incorrect.")
    except Exception as e:
        print("An error occurred:", e)

def generate_samples(var_parents,cpt_dict,var_dict):
    sample = {}
    #print(var_parents)
    for i in var_parents:
        #print("Hello")
        if var_parents[i] == ['']:
            rand = random.random()
            #print(i)
            cumulative_prob = 0.0
            for key in cpt_dict[i]:
                cumulative_prob += cpt_dict[i][key]
                if rand < cumulative_prob:
                    sample[i] = key
                    #print(key)
                    break

        else:
            s = ""
            #print(i)
            for key in var_parents[i]:
                s+=sample[key]
            sample_list = []
            for possible_value in var_dict[i]:
                sample_list.append((s+possible_value,possible_value))

            rand = random.random()
            cumulative_prob = 0.0
            for key,sm in sample_list:
                cumulative_prob += cpt_dict[i][key]
                if rand < cumulative_prob:
                    sample[i] = sm
                    #print(sm)
                    break


    return sample

        
def prior_sampling(var_parents,cpt_dict,var_dict,ucv_d,cv_d,iterations):
    sample_ct=0.0
    ct=0.0
    for i in range(iterations):
        flag = False
        extract_sample = generate_samples(var_parents,cpt_dict,var_dict)
        print(f'Iteration number {i+1} : {extract_sample}')
        for i in cv_d:
            if(cv_d[i]==extract_sample[i]):
                flag = True
            else:
                flag = False
                break

        if(flag):
            sample_ct+=1
            for i in ucv_d:
                if(ucv_d[i]==extract_sample[i]):
                    flag = True
                else:
                    flag = False
                    break

            if(flag):
                ct+=1

    return float(ct/sample_ct)
    #print("Probability: ",float(ct/sample_ct))

def rejection_sampling(var_parents,cpt_dict,var_dict,ucv_d,cv_d,iterations):
    ct=0
    it_no=0
    match_ct=0
    while(ct<iterations):
        flag = False
        extract_sample = generate_samples(var_parents,cpt_dict,var_dict)
       
        for i in cv_d:
            if(cv_d[i]==extract_sample[i]):
                flag = True
            else:
                flag = False
                break

        if(flag):
            ct+=1
            for i in ucv_d:
                if(ucv_d[i]==extract_sample[i]):
                    flag = True
                else:
                    flag = False
                    break

            if(flag):
                match_ct+=1
                print(f'Iteration number {it_no+1} :\n')
                print(f'Selected Sample : {extract_sample}')
                print(ct)
            else:
                print(f'Iteration number {it_no+1} :\n')
                print(f'Selected Sample : {extract_sample}')
                print(ct)
        else:
            print(f'Iteration number {it_no+1} :\n')
            print(f'Rejected Sample : {extract_sample}')
            print(ct)

        it_no=it_no+1
    return float(match_ct/ct)
    #print("Probability: ",float(match_ct/ct))
    
def gen_weighted_sample(var_parents,cpt_dict,var_dict,cv_dict):
    sample = {}
    w = 1
    #print(var_parents)
    for i in var_parents:
        #print("Hello")
        if i in cv_dict:

            if var_parents[i] == ['']:
                sample[i] = cv_dict[i]
                w = w*cpt_dict[i][cv_dict[i]]

            else:
                s = ""
                #print(i)
                for key in var_parents[i]:
                    s+=sample[key]
                val_exp = cv_dict[i]
                s+=val_exp
                sample[i] = val_exp
                w=w* cpt_dict[i][s]
                

        else:
        
            #print(var_parents)
        
            #print("Hello")
            if var_parents[i] == ['']:
                rand = random.random()
                #print(i)
                cumulative_prob = 0.0
                for key in cpt_dict[i]:
                    cumulative_prob += cpt_dict[i][key]
                    if rand < cumulative_prob:
                        sample[i] = key
                        #print(key)
                        break

            else:
                s = ""
                #print(i)
                for key in var_parents[i]:
                    s+=sample[key]
                sample_list = []
                for possible_value in var_dict[i]:
                    sample_list.append((s+possible_value,possible_value))

                rand = random.random()
                cumulative_prob = 0.0
                for key,sm in sample_list:
                    cumulative_prob += cpt_dict[i][key]
                    if rand < cumulative_prob:
                        sample[i] = sm
                        #print(sm)
                        break


    return sample,w
def likelihood_weighting(var_parents,cpt_dict,var_dict,ucv_d,cv_d,iterations):
    wt=0
    tot_weight=0.0
    sample_weight = 0.0
    for i in range(iterations):
        flag = False
        ext_sample,weight = gen_weighted_sample(var_parents,cpt_dict,var_dict,cv_d)
        print(f'Generated Sample : {ext_sample} , weight : {weight}')
        for i in ucv_d:
            if ucv_d[i] == ext_sample[i]:
                flag = True
            else:
                flag = False
                break
        tot_weight = tot_weight+weight
        if(flag):
            sample_weight = sample_weight+weight
    return (sample_weight/tot_weight)
    #print(sample_weight/tot_weight)

def calculate_probability(sample_var,var_parents,var_dict,sample,cpt_dict):
    tot_prob =0.0
    cpts_to_compute=[]
    prob_list_total = []
    fin_dist = {}
    dist = {}
    for i in var_dict[sample_var]:
        sample[sample_var] = i
        p=1
        for cpt in cpt_dict:
            print("CPT:",cpt)
            if(cpt == sample_var):
                s=""
                if(var_parents[cpt]!=['']):
                    for var in var_parents[cpt]:
                        s+=sample[var]
                s+=i
                print("Sample as child :",s)
                dictionary = cpt_dict[cpt]
                for values in dictionary:
                    if(values == s):
                        p*=dictionary[values]

            elif (sample_var in var_parents[cpt]):
                s=""
                for var in var_parents[cpt]:
                    s+=sample[var]
                s+=sample[cpt]
                print("Sample as parent :",s)
                dictionary = cpt_dict[cpt]
                for values in dictionary:
                    if(values == s):
                        p*=dictionary[values]


        tot_prob+=p
        dist[i] = p

    for i in dist:
        fin_dist[i] = dist[i]/tot_prob

    return fin_dist

           
    # for i in var_dict:



def gibbs_sampling(var_parents,cpt_dict,var_dict,ucv_d,cv_d,iterations):
    sample = {var: random.choice(var_dict[var]) for var in var_parents}
    print(sample)
    for var in sample:
        if var in cv_d:
            sample[var] = cv_d[var]

    non_evidence = [var for var in var_parents if var not in cv_d]
    
    temp = copy.deepcopy(non_evidence)
    print("Temp: ",temp)
    sample_match =0
    for i in range(iterations):
        print(f'Iteration {i+1}: -------------------------')
        print(non_evidence)
        sample_var = random.choice(non_evidence)
        #sample_var = 'M'
        print(sample_var)
        print("Before:",sample)
        distribution = calculate_probability(sample_var,var_parents,var_dict,sample,cpt_dict)
        ran = random.random()
        cum_prob =0.0
        for val in distribution:
            cum_prob+=distribution[val]
            if(ran<cum_prob):
                sample[sample_var] = val
                break
        print(distribution)
        print("After:",sample)
        non_evidence = copy.deepcopy(temp)
        #print("Before Removing: ",non_evidence)
        non_evidence.remove(sample_var)
        #print("After Removing: ",non_evidence)
        print(f'Generated Sample : {sample}')
        flag = False
        for i in ucv_d:
            if(ucv_d[i]==sample[i]):
                flag = True
            else:
                flag = False
                break

        if(flag):
            sample_match+=1

        print("---------------------------------------")

    return sample_match/iterations
    #print("Probability :", sample_match/iterations)




        

def main():
    tot_var,topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict = extractinfo('example_bayesnet.txt')
    num_samples = 500  # Number of samples for all sampling methods
    # print(topo_sorted_var_parents)
    # print(cpt_dict)
    #print(var)
    #Prior Sampling
    # prior_samples = prior_sampling(topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict,num_samples)
    # print("Prior Sampling Result:", prior_samples)

    #Rejection Sampling
    result_rejection = rejection_sampling(topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict,num_samples)
    print("Rejection Sampling Result:", result_rejection)

    #Likelihood Weighting
    # result_likelihood = likelihood_weighting(topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict,num_samples)
    # print("Likelihood Weighting Result:", result_likelihood)

    #Gibbs Sampling
    # result_gibbs = gibbs_sampling(topo_sorted_var_parents,cpt_dict,var_dict,ucv_dict,cv_dict,num_samples)
    # print("Gibbs Sampling Result:", result_gibbs)


if __name__ == "__main__":
    main()







        

#print(cpt_dict)

# v,c,v_d,u,cv = extractinfo()
#gibbs_sampling(v,c,v_d,u,cv,1000)
#ext_sample = generate_samples(v,c,v_d)
#print(ext_sample)
#prior_sampling(v,c,v_d,u,cv,10000)
#rejection_sampling(v,c,v_d,u,cv,1000)

#likelihood_weighting(v,c,v_d,u,cv,5000)
#extractinfo()