#Wikicivi Crawler Client SDK
import os
import time
import datetime
import os,sys
import json
import re
import traceback
import threading

#创建thread_count个线程,均匀分担thread_jobs里的负载.
def domt(thread_func,max_threads,thread_jobs,thread_param=None):
    thread_results = []
    THREAD_N = max_threads
    if max_threads > len(thread_jobs):
        THREAD_N = len(thread_jobs)
    try:
        time0 = int(time.time())
        thread_load_list = []
        for k in range(THREAD_N):
            thread_load_list.append({"tid":k%THREAD_N+1000,"jobs":[]})

        cur_K= 0
        for job in thread_jobs:
            thread_load_list[cur_K%THREAD_N]["jobs"].append(job)
            cur_K +=1

        threads = []
        for thread_load in thread_load_list:
            if len(thread_load["jobs"]) == 0:
                continue
            thread = threading.Thread(target=thread_func,args=(thread_load["tid"],thread_load["jobs"],thread_param,thread_results))    
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()           #主线程等待 ta线程结束才继续执行
       
        time1 = int(time.time())
        return thread_results
    except Exception as err:
        print(traceback.format_exc())
        print(err)
        return []


def demo_thread_main(thread_id,thread_jobs,thread_param,thread_results):
    for job in thread_jobs:
        print("t"+str(thread_id)+"  "+job["name"])
        thread_results.append(job["name"])


def main():
    com_list = [
        {'name':'测试1_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试2_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试3_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试4_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试5_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试6_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试7_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试8_北京科技有限公司','tags':["tag1","tag2"]}
    ]
    thread_results = domt(demo_thread_main,4,com_list)
    print(thread_results)


if __name__ == '__main__':
    main()
