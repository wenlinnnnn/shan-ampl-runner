import multiprocessing as mp
import os
import pathlib
import subprocess


def call_ampl(instance_folder_name, instance_name, time_limit, num_threads):
    template: str
    template_filename = "testwithIEEE.run_template"
    instance_complete_name = f"{instance_folder_name}/{instance_name}"
    output_dir = "ampl_outputs"
    log_dir = pathlib.Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir/(instance_name+".txt")
    
    with open(template_filename, "r", encoding="utf-8") as f:
        template = f.read()
    
    
    run_script = template.replace("@INSTANCE_NAME@", instance_complete_name)
    run_script = run_script.replace("@TIME_LIMIT@", str(time_limit))
    run_script = run_script.replace("@NUM_THREADS@", str(num_threads))
    run_script = run_script.replace("@OUTPUT_DIR@", output_dir)
    
    run_dir = pathlib.Path()/"runfiles"/instance_folder_name
    run_script_filename = f"{instance_name}.run"
    run_filepath = run_dir/run_script_filename
    with open(run_filepath.absolute(), "w+", encoding="utf-8") as f:
        f.write(run_script)
    
    cmd_args = ["ampl", run_filepath.absolute()]
    with open(log_path.absolute(), "w", encoding="utf-8") as logfile:
        subprocess.run(cmd_args, stdout=logfile, stderr=subprocess.STDOUT)
    if os.path.exists(run_filepath.absolute()):
        # os.remove(run_filepath.absolute())
        print(f"Solver is Done, File run file is saved in {run_filepath.absolute()}.")

if __name__ == "__main__":
    output_root_dir = pathlib.Path()/"ampl_outputs"
    run_root_dir = pathlib.Path()/"runfiles"
    instance_folder_names = [
        "data_10",
        "data_5",
        "data_15",
        "data_25"
    ]
    for instance_folder_name in instance_folder_names:    
        output_dir = output_root_dir/instance_folder_name
        output_dir.mkdir(parents=True, exist_ok=True)
        run_dir = run_root_dir/instance_folder_name
        run_dir.mkdir(parents=True, exist_ok=True)
    
    all_instances = [
        ("data_5","C101-5"),
        ("data_5","C103-5"),
        ("data_5","C206-5"),
        ("data_5","C208-5"),
        ("data_5","R104-5"),
        ("data_5","R105-5"),
        ("data_5","R202-5"),
        ("data_5","R203-5"),
        ("data_5","RC105-5"),
        ("data_5","RC108-5"),
        ("data_5","RC204-5"),
        ("data_5","RC208-5"),
        ("data_10","C101-10"),
        ("data_10","C104-10"),
        ("data_10","C202-10"),
        ("data_10","C205-10"),
        ("data_10","R102-10"),
        ("data_10","R103-10"),
        ("data_10","R201-10"),
        ("data_10","R203-10"),
        ("data_10","RC102-10"),
        ("data_10","RC108-10"),
        ("data_10","RC201-10"),
        ("data_10","RC205-10"),
        ("data_15","C103-15"),
        ("data_15","C106-15"),
        ("data_15","C202-15"),
        ("data_15","C208-15"),
        ("data_15","R102-15"),
        ("data_15","R105-15"),
        ("data_15","R202-15"),
        ("data_15","R209-15"),
        ("data_15","RC103-15"),
        ("data_15","RC108-15"),
        ("data_15","RC202-15"),
        ("data_15","RC204-15"),
        ("data_25","C101-25"),
        ("data_25","C102-25"),
        ("data_25","C103-25"),
        ("data_25","C104-25"),
        ("data_25","C105-25"),
        ("data_25","C106-25"),
        ("data_25","C107-25"),
        ("data_25","C108-25"),
        ("data_25","C109-25"),
        ("data_25","C201-25"),
        ("data_25","C202-25"),
        ("data_25","C203-25"),
        ("data_25","C204-25"),
        ("data_25","C205-25"),
        ("data_25","C206-25"),
        ("data_25","C207-25"),
        ("data_25","C208-25"),
        ("data_25","R101-25"),
        ("data_25","R102-25"),
        ("data_25","R103-25"),
        ("data_25","R104-25"),
        ("data_25","R105-25"),
        ("data_25","R106-25"),
        ("data_25","R107-25"),
        ("data_25","R108-25"),
        ("data_25","R109-25"),
        ("data_25","R110-25"),
        ("data_25","R111-25"),
        ("data_25","R112-25"),
        ("data_25","R201-25"),
        ("data_25","R202-25"),
        ("data_25","R203-25"),
        ("data_25","R204-25"),
        ("data_25","R205-25"),
        ("data_25","R206-25"),
        ("data_25","R207-25"),
        ("data_25","R208-25"),
        ("data_25","R209-25"),
        ("data_25","R210-25"),
        ("data_25","R211-25"),
        ("data_25","RC101-25"),
        ("data_25","RC102-25"),
        ("data_25","RC103-25"),
        ("data_25","RC104-25"),
        ("data_25","RC105-25"),
        ("data_25","RC106-25"),
        ("data_25","RC107-25"),
        ("data_25","RC108-25"),
        ("data_25","RC201-25"),
        ("data_25","RC202-25"),
        ("data_25","RC203-25"),
        ("data_25","RC204-25"),
        ("data_25","RC205-25"),
        ("data_25","RC206-25"),
        ("data_25","RC207-25"),
        ("data_25","RC208-25"),
        
    ]
    
    shan_pc_instances = []
    gemilang_pc_instances = []
    workstation_pc_instances = []

    for i, instance in enumerate(all_instances):
        if i%3==0:
            shan_pc_instances.append(instance)
        elif i%3==1:
            gemilang_pc_instances.append(instance)
        else:
            workstation_pc_instances.append(instance)

    PC = "GEMILANG"
    # PC = "SHAN"
    # PC = "WORKSTATION"

    chosen_instances = gemilang_pc_instances # change this depending whether you ar ein workstaion or els
    if PC == "SHAN":
        chosen_instances = shan_pc_instances
    elif PC == "WORKSTATION":
        chosen_instances = workstation_pc_instances
    time_limit = 28800
    num_threads = 2
    num_cpus = os.cpu_count()
    if num_cpus is None:
        num_cpus = 8
    num_workers = int(num_cpus/num_threads)
    print(f"Number of instances to be run: {len(chosen_instances)}")
    print(f"Running {num_workers} instances in parallel")
    print(f"Estimated running for {(int(len(chosen_instances)/num_workers) + 1)*time_limit/3600} Hours")
    # for ist in chosen_instances:
    #     print(ist)
    
    # args_list = [(instance_folder_name, instance_name, time_limit, num_threads) for (instance_folder_name, instance_name) in chosen_instances]
    # with mp.Pool(num_workers) as pool:
    #     pool.starmap(call_ampl, args_list)


    # for args in args_list:
    #     call_ampl(*args)
    #     exit()