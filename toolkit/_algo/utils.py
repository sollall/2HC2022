class Graph_Manager():
    #隣接関係、持ってるジョブのidが分かればよい
    def __init__(self,Nv):
        self.job=[[] for _ in range(Nv)]   
    
    def register_job(self,job_id,v):
        self.job[v].append(job_id)


def input_data(path):
    
    
    with open(path) as f:
        type=f.readline()

        T_MAX=int(f.readline()) #返す

        Nv,Ne=map(int,f.readline().split())

        #init
        GM=Graph_Manager(Nv)

        loc={} #返す
        for _ in range(Nv):
            n,x,y=map(float,f.readline().split(" "))
            loc[n-1]=(x,y)

        edges=[{} for i in range(Ne)] #返す
        for _ in range(Ne):
            u,v,d=map(int,f.readline().split(" "))
            edges[u-1][v-1]=d
            edges[v-1][u-1]=d

        N_work=int(f.readline())
        workers=[{} for i in range(N_work)] #返す
        for i in range(N_work):
            work_status=list(map(int,f.readline().split()))
            workers[i]["v"]=work_status[0]
            workers[i]["task_max"]=work_status[1]
            workers[i]["job_type"]=work_status[3:][:]


        N_job=int(f.readline())
        jobs=[{} for i in range(N_job)]

        for _ in range(N_job):

            id,task_type,N_task,v,P,d,flag=map(float,f.readline().split())
            id,task_type,N_task,v,P,flag=int(id),int(task_type),int(N_task),int(v),int(P),int(flag)
            id-=1
            v-=1
            jobs[id]["task_type"]=task_type
            jobs[id]["N_task"]=N_task
            jobs[id]["v"]=v
            jobs[id]["P"]=P
            jobs[id]["d"]=d
            jobs[id]["flag"]=flag

            GM.register_job(id,v)

            jobs_reward=list(map(int,f.readline().split())) #N,(t,r)*N
            
            reward_sche=[[],[]] #返す tでのリワードを二分探索と線形補完で教えてくれる関数をつくる
            for i in range(jobs_reward[0]):
                reward_sche[0].append(jobs_reward[2*i+1])
                reward_sche[1].append(jobs_reward[2*i+2])
            jobs[id]["reward_sche"]=reward_sche[:]

            jobs_depend=list(map(int,f.readline().split()))[1:] #返す 依存関係をグラフにしたい
            jobs[id]["depend"]=jobs_depend[:]
        
        if type[0]=="A":
            return T_MAX,loc,edges,workers,jobs,GM
        elif type[0]=="B":
            N_weather,T_weather,_=map(int,f.readline().split()) #T_weather
            weather_automatton={}
            for n in range(N_weather):
                weather_automatton[n]=list(map(float,f.readline().split()))
            c=list(map(int,f.readline().split()))

            Pm,Rm,alpha=map(float,f.readline().split())#返す
            calibration=[Pm,Rm,alpha]

            return T_MAX,loc,edges,workers,jobs,T_weather,weather_automatton,c,calibration,GM


