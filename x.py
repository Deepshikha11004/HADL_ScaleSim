import configparser
from scalesim.scale_sim import scalesim
cp = configparser.ConfigParser()
from multiprocessing import Process
import os
gemm = False
topo_files = ['alexnet.csv', 'frcnn.csv', 'googlenet.csv', 'resnet18.csv', 'mobilenet.csv', 'yolo_tiny.csv']




def eyeriss():
    cfg  = open('scale-sim-v2/configs/eyeriss.cfg')
    cp.read_file(cfg)
    
    procs = []
    
    for topo in topo_files:
        net = topo.split('.')[0]
        path = f'Part1/eyeriss/{net}'
        if os.path.exists(path):
            continue
        s = scalesim(
            save_disk_space=True, verbose=True,
            config='scale-sim-v2/configs/eyeriss.cfg',
            topology='scale-sim-v2/topologies/conv_nets/'+ topo,
            input_type_gemm=gemm
        )
        p = Process(target=s.run_scale, args=(path,))
        procs += [p]
        p.start()

    for p in procs:
        p.join()



""" def get_variants():
    cfg = open('scale-sim-v2/configs/eyeriss.cfg')
    cp.read_file(cfg)

    net_names = ['mobilenet', 'resnet18', 'frcnn']
    flows = ['ws', 'is', 'os']
    srams = [60, 84, 108, 132, 156]
    pe_array = [(12, 14), (18, 21), (24, 28), (30, 35), (36, 42)]

    procs = []
    for net in net_names:
        topo = net + '.csv'
        
        for pe in pe_array:
            path = f'variant/{net}_pe{pe[0]}x{pe[1]}'
            if os.path.exists(path):
                continue
            cp.set('architecture_presets', 'ArrayHeight', f'{pe[0]}')
            cp.set('architecture_presets', 'ArrayWidth', f'{pe[1]}')
            with open('variant.cfg', 'w') as f:
                cp.write(f)
            s = scalesim(
                save_disk_space=True, verbose=True,
                config='variant.cfg',
                topology=topo,
                input_type_gemm=False
            )
            # s.run_scale(path)
            p = Process(target=s.run_scale, args=(path,))
            procs += [p]
            p.start()

    for p in procs:
        p.join()
 """        
        
        
# get_eyeriss()
# get_google()
# get_scale()
# get_variants()

eyeriss()