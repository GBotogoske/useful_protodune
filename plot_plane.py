import ROOT as root
from waffles.np04_analysis.light_vs_hv.imports import *

#plane U V X ==> 012
#APA 1,2,3,4 ==> APA_P01SU , APA_P02SU, APA_P02NL , APA_P01NL
#cada deltat sao 32 unidades de timestamps

cont=0

range_APA = 5952
range_PDS = 4395

wire_number_1 = []
wire_number_2 = []
wire_number_3 = []
wire_number_4 = [[7680 , 8479], [8480,9279], [9280,10239]] #800,800,960 fios

wire_number=[wire_number_1,wire_number_2,wire_number_3,wire_number_4]


home_folder="/home/gabriel/Documents/protodune/data/HD/charge/28210/"
file_name="merge_output.root"

def get_timestamp_pds(file,ov):

    wfsets=None
    with open(file, 'rb') as attr:
        wfsets=pickle.load(attr)
    wfsets[ov][0].waveforms[0].timestamp
    timestamps_pds=[]
    for wf in wfsets[ov][0].waveforms:
        timestamps_pds.append(wf.timestamp)
    return timestamps_pds

def get_timestamp_apa(tree_in):

    timestamp = []

    N=tree_in.GetEntries()

    for i in range(N):
        tree_in.GetEntry(i)
        time_aux=tree_in.timestamp

        if time_aux not in timestamp:
            timestamp.append(time_aux)
    
    return sorted(timestamp)
     

def get_plane(time, tree_in):
   
    N = tree_in.GetEntries()

    for i in range(N):
        tree_in.GetEntry(i)
        time_aux = tree_in.timestamp
        if time == time_aux:
            wf_length = len((np.array(tree_in.wf, copy=True)))
            break
        
    adcs = [
    [np.zeros(wf_length) for _ in range(800)],   
    [np.zeros(wf_length) for _ in range(800)],   
    [np.zeros(wf_length) for _ in range(960)]    
    ]

    counts = [0,0,0]
    for i in range(N):
        tree_in.GetEntry(i)
        time_aux = tree_in.timestamp
        if time == time_aux:
            plane=int(tree_in.plane)

            apa = tree_in.crate_geo - 1
            ch  = tree_in.channel_offline - wire_number[apa][plane][0]
            
            adcs[plane][ch] = (np.array(tree_in.wf, copy=True))
            
            if counts[0] == 0 and counts[1] == 0 and counts[2] == 0:
                print(f"waveform length: {len(adcs[plane][ch])}")
            counts[plane] = counts[plane] + 1

            if counts[0] == 800 and counts[1] == 800 and counts[2] == 960:
                break
            
    return adcs
    
def filter_plane(adcs):
    wires = [
    [None for _ in range(800)],   
    [None for _ in range(800)],   
    [None for _ in range(960)]    
    ]

    kernel=np.ones(20)
    for plane_index in range(3):
        for ch in range(len(wires[plane_index])):   
            wires[plane_index][ch] = np.convolve(np.array(adcs[plane_index][ch] - np.mean(adcs[plane_index][ch])), kernel, "same")  
            wires[plane_index][ch] = np.where(wires[plane_index][ch] > 400, 1, 0)  

    return wires

def print_plane(wires,index):


    fig, axes = plt.subplots(3, 1, figsize=(15, 15))  

    title = ["INDUCTION PLANE U", "INDUCTION PLANE V", "COLLECTION PLANE X"]

    for i in range(3):
        print(len(wires),len(wires[i]))
        im = axes[i].imshow(wires[i], aspect='auto', cmap='viridis', origin='lower')
        axes[i].set_xlabel('Time [samples]')
        axes[i].set_ylabel('Wires')
        axes[i].set_title(f'APA 4 - {title[i]}')
        fig.colorbar(im, ax=axes[i], label='Intensidade do sinal')

        

    fig.tight_layout()  
    print(f" Saving /home/gabriel/Documents/protodune/data/HD/charge/28210/all_figures/candidate_{index}.png")
    fig.savefig(f"/home/gabriel/Documents/protodune/data/HD/charge/28210/all_figures/candidate_{index}.png")
    plt.close(fig)  # Fecha a figura para liberar memória e evitar que Jupyter renderize

def main():
    file = "/home/gabriel/Documents/protodune/data/HD/charge/28210/merge_output.root"
    file_in = root.TFile.Open(file, "READ")
    tree_in = file_in.Get("my_tree")  # Nome do TTree dentro do arquivo

  
    timestamp_apa = get_timestamp_apa(tree_in)
   

    for i,time in enumerate(timestamp_apa):
        adcs = get_plane(time,tree_in)
        adcs = filter_plane(adcs)
        print_plane(adcs,i)

if __name__=="__main__":
    main()
