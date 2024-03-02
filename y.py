import configparser
from scalesim.scale_sim import scalesim
cp = configparser.ConfigParser()
from multiprocessing import Process
import os
gemm = False
topo_files = ['alexnet.csv', 'FasterRCNN.csv', 'Googlenet.csv', 'Resnet18.csv', 'mobilenet.csv', 'yolo_tiny.csv']
# topo_files = [ 'mobilenet.csv', 'yolo_tiny.csv']

def google():
    cfg  = open('scale-sim-v2/configs/google.cfg')
    cp.read_file(cfg)
    
    procs = []
    
    for topo in topo_files:
        net = topo.split('.')[0]
        path = f'Part1/google/{net}'
        if os.path.exists(path):
            continue
        s = scalesim(
            save_disk_space=True, verbose=True,
            config='scale-sim-v2/configs/google.cfg',
            topology='scale-sim-v2/topologies/conv_nets/'+ topo,
            input_type_gemm=gemm
        )
        p = Process(target=s.run_scale, args=(path,))
        procs += [p]
        p.start()

    for p in procs:
        p.join()

google()