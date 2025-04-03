import click, pickle, inquirer

from waffles.utils.utils import print_colored
import waffles.input_output.raw_hdf5_reader as reader
import re

@click.command(help=f"\033[34mSave the WaveformSet object in a pickle file for easier loading.\n\033[0m")
@click.option("--run",   default = None, help="Run number to process", type=str)
@click.option("--dataflow",   default = None, help="Run number to process", type=str)
@click.option("--debug", default = True, help="Debug flag")
def main(run, dataflow, debug):
    '''
    Script to process peak/pedestal variables and save the WaveformSet object + unidimensional variables in a pickle file.

    Args:
        - run (int): Run number to be analysed. I can also be a list of runs separated by commas.
    Example: python 01Process.py --run 123456 or --run 123456,123457
    '''
    if run is None: 
        q = [ inquirer.Text("run", message="Please provide the run(s) number(s) to be analysed, separated by commas:)")]
        run_list = inquirer.prompt(q)["run"].split(",")
    else:
        run_list = run.split(",")
    
    for r in run_list:
        rucio_filepath = f"/eos/experiment/neutplatform/protodune/experiments/ProtoDUNE-II/PDS_Commissioning/waffles/1_rucio_paths/{str(r).zfill(6)}.txt"
        rucio_filepath="0"+ r + ".txt"
        
        if debug: 
            print_colored(f"Processing {str(r).zfill(6)}...", color="DEBUG")
        
        filepaths = reader.get_filepaths_from_rucio(rucio_filepath)
        if len(filepaths) > 5:
            print_colored(f"This run has {len(filepaths)} hdf5 files. \n {filepaths[:5]}", color="WARNING")
        else: 
            file_lim = len(filepaths)
        
        n_files = len(filepaths)
        last_digit = re.search(r'_(\d{4})_', filepaths[n_files-1])
        last_digit=int(last_digit.group(1))
        
        if dataflow is None:
            q2 = [ inquirer.Text("dataflow", message="Please provide the dataflow number to be analysed:)")]
            search_digit = int(inquirer.prompt(q2)["dataflow"].split(",")[0])
        else:
            search_digit=dataflow.split(",")[0]
        
        i=search_digit
        if i == search_digit:
            print(search_digit)
            find_str="_00"+f"{int(i):02}"+"_"
            print(find_str)
            filtered_files = [path for path in filepaths if re.search(find_str, path)]

            for j in range(len(filtered_files)):
                print(filtered_files[j])
            
            wfset = reader.WaveformSet_from_hdf5_files( filtered_files, read_full_streaming_data = False , truncate_wfs_to_minimum=False )                      
            # TODO: subsample the data reading (read each 2 entries)

            path_work="/afs/cern.ch/work/g/gbotogos/data/"

            if debug: 
                print_colored("Saving the WaveformSet object in a pickle file...", color="DEBUG")
            with open(f"{path_work}{str(r).zfill(6)}{find_str}full_wfset_raw.pkl", "wb") as f:
                pickle.dump(wfset, f)
            
            print_colored(f"\nDone! WaveformSet saved in {str(r).zfill(6)}_{find_str}+_full_wfset_raw.pkl\n", color="SUCCESS")
            

if __name__ == "__main__":
    main()