import re
import csv
import glob
import numpy as np
from statistics import geometric_mean as gm



rx_dict = {
    'IPC': re.compile(r'CPU\s*0\s*cumulative\s*IPC\D*(?P<IPC>\S*)'),
    'load_miss': re.compile(r'L1I.*LOAD.*MISS\D*(?P<load_miss>\S*)'),
    'miss_latency': re.compile(r'L1I.*LATENCY\D*(?P<miss_latency>\S*)'),
    'useful': re.compile(r'L1I.*USEFUL\D*(?P<useful>\S*)'),
    'useless': re.compile(r'L1I.*USELESS\D*(?P<useless>\S*)'),
    'prftch_rec':re.compile(r'L1I.*REQUESTED\D*(?P<prftch_rec>\S*)'),
}

#model_list = ['no', 'D_JOLT', 'pips', 'EIP']
#model_list=['no', 'D_JOLT_5_4', 'D_JOLT_9_4', 'D_JOLT_11_4', 'D_JOLT', 'D_JOLT_a_0p5', 'D_JOLT_a_2', 'D_JOLT_l_2', 'D_JOLT_d_20_6', 'D_JOLT_d_10_2']
#model_list=['no', 'pips_ns_6', 'pips_ns_8', 'pips_t_2', 'pips_t_5']
model_list=['no', 'pips_ns_2', 'pips_t_9', 'pips_hm', 'pips_hm_l']


all_result_dict = {}

for model in model_list:
    #file_list = glob.glob(f"fin_results/*{model}-next*")
    file_list = glob.glob(f"results_50M/*{model}-next*")

    for filepath in file_list:
        result_dict = {}
        trace_tag = re.match(r'.*/(\S*).champ.*',filepath).group(1)
        
        with open(filepath,'r') as file:
            line = file.readline()
            while line:
                line = file.readline()

                for key,rx in rx_dict.items():
                    match = rx.match(line)
                    if match: 
                        result_dict[key] = float(match.group(key))
        if  trace_tag not in all_result_dict.keys(): all_result_dict[trace_tag] = {}
        all_result_dict[trace_tag][model] = result_dict

trace_list = []
for trace in all_result_dict.keys():
    trace_list.append(trace)

np_trace_list = np.array(trace_list)
#print(np_trace_list.shape)

np_trace_list = np.transpose(np_trace_list)
np_trace_list = np_trace_list.reshape((50,1))
#print(np_trace_list.shape)

IPC_SPEED   =  np.zeros((50,10))
L1_useful   =  np.zeros((50,10))
L1_useless  =  np.zeros((50,10))
L1_pft_rec  =  np.zeros((50,10))
miss_ltcy   =  np.zeros((50,10))


for i in range(1,len(model_list)):
        model = model_list[i]

        for index, trace in enumerate(all_result_dict.keys()):
            print(trace, model, all_result_dict[trace][model]['IPC'])    
            IPC_SPEED[index][i-1]   = (all_result_dict[trace][model]['IPC']/all_result_dict[trace][model_list[0]]['IPC'])
            L1_useful[index][i-1]   = int(all_result_dict[trace][model]['useful'])
            L1_useless[index][i-1]  = int(all_result_dict[trace][model]['useless'])
            L1_pft_rec[index][i-1]  = int(all_result_dict[trace][model]['prftch_rec'])
            miss_ltcy[index][i-1]   = all_result_dict[trace][model]['miss_latency']


IPC_SPEED_w_trace   = np.concatenate((np_trace_list, IPC_SPEED), axis=1)
L1_pft_rec_w_trace  = np.concatenate((np_trace_list, L1_pft_rec), axis=1)
L1_useless_w_trace  = np.concatenate((np_trace_list, L1_useless), axis=1)
L1_useful_w_trace   = np.concatenate((np_trace_list, L1_useful), axis=1)
miss_ltcy_w_trace   = np.concatenate((np_trace_list, miss_ltcy), axis=1)

filename = "bl_data_dump_pip_IPC.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(IPC_SPEED_w_trace)

filename = "bl_data_dump_pip_pft_rec.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(L1_pft_rec_w_trace)

filename = "bl_data_dump_pip_pft_useless.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(L1_useless_w_trace)

filename = "bl_data_dump_pip_pft_useful.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(L1_useful_w_trace)


filename = "bl_data_dump_pip_miss_ltcy.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
    # writing the fields 
    csvwriter.writerow(model_list) 
        
    # writing the data rows 
    csvwriter.writerows(miss_ltcy_w_trace)