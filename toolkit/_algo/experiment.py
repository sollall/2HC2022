import bisect
import heapq as hq
from utils import input_data


def reward_at_t(id,t):
    index=bisect.bisect(jobs[id]["reward_sche"][0],t)
    reward=None
    if index==0 or index==len(jobs[id]["reward_sche"][0]):
        reward=0
    else:
        t1,r1=jobs[id]["reward_sche"][0][index-1],jobs[id]["reward_sche"][1][index-1]
        t2,r2=jobs[id]["reward_sche"][0][index],jobs[id]["reward_sche"][1][index]

        reward=(r2-r1)/(t2-t1)*t2+r1
        
    return reward

def bfs(now,goal=None):
    #nowの隣接を先に入れる
    visited=[0]*len(edges)
    visited[now]=1
    queue=[[edges[now][nxt],nxt] for nxt in edges[now].keys()]
    hq.heapify(queue)
    while queue:
        cost,pos=hq.heappop(queue)
        if visited[pos]==0:
            visited[pos]=1
            for nxt,n_cost in edges[pos].items():
                hq.heappush(queue,[cost+n_cost,nxt])
            if goal:
                if pos==goal:
                    yield cost
            else:
                yield pos

"""
たぶんいらない関数あつめ
def depend_tree():
    #有効グラフ　実行待ちに入れるのに必要なjobを記録しておいて、オールグリーンなら実行待ちに入れたい
    depend_tree=[[] for i in range(len(jobs))]
    for id in range(len(jobs)):
"""

#input
T_MAX,loc,edges,workers,jobs,GM=input_data("testcase_A.txt")

#init
w_status=[[workers[id]["v"],"stay",0] for id in range(len(workers))] #今の位置、命令、行動終了の待ち時間
j_finished=[[0,jobs[id]["N_task"]] for id in range(len(jobs))]
j_available={}
for id in range(len(jobs)):
    
    for depend in jobs[id]["depend"]:
        judge=True
        flag_finished=(j_finished[depend-1][0]/j_finished[depend-1][1])//1
        if j_finished[depend-1]:
            pass
        else:
            judge=False
        if judge:
            j_available[depend]=1



for t in range(T_MAX):
    #worker,jobのstate

    #action
    #workerの現在地から周辺をみてコストが最大になるのを選ぶ
    #とかしたいけど時間かかるから最寄りのノードからできる仕事があるところに動いて仕事する
    #仕事がここであるなら仕事する　ないならほかにうつる
    
    for w_id in range(len(workers)):
        candidates_generator=bfs(workers[w_id]["v"])
        next_work=(None,None)#v,j_id

        while next_work==(None,None):
            next_v=next(candidates_generator)
            for j_id in GM.job[next_v]:
                task_type=jobs[j_id]["task_type"]
                if task_type in workers[w_id]["job_type"] and (j_finished[j_id][0]/j_finished[j_id][1])//1==0:
                    next_work=(next_v,j_id)
        #w_status=今の位置、命令、行動終了の待ち時間
        if w_status[w_id][2]==0:
            if w_status[w_id][0]!=next_work[0]:#仕事がなくて移動する場合
                cost=next(bfs(w_status[w_id][0],goal=next_work[0]))
                w_status[w_id]=[next_work[0],f"move {next_work[0]}",cost]

            else:#仕事が残っている場合
                for j_id in GM.job[w_status[w_id][0]]:
                    if (j_finished[j_id][0]/j_finished[j_id][1])//1==0:
                        a=min(workers[w_id]['task_max'],j_finished[j_id][1]-j_finished[j_id][0])                   
                        w_status[w_id][1]=f"execute {next_work[1]} {a}"
                        j_finished[j_id][0]+=a

        else:#移動中
            w_status[w_id][2]-=1
        
        print(w_status[w_id][1])


