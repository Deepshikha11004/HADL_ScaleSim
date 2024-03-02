import configparser
from scalesim.scale_sim import scalesim
cp = configparser.ConfigParser()
from multiprocessing import Process
import os
gemm = False
topo_files = ['alexnet.csv', 'frcnn.csv', 'googlenet.csv', 'resnet18.csv', 'mobilenet.csv', 'yolo_tiny.csv']

def get_eyeriss():
    eyeriss = [
            scalesim(
                save_disk_space=True, verbose=True,
                config='eyeriss.cfg',
                topology=topo,
                input_type_gemm=gemm
            ) 
            for topo in topo_files
        ]
    for i in range(len(eyeriss)):
        eyeriss[i].run_scale(top_path=f'./eyeriss/{topo_files[i]}')
        print('Finished running topology: ', topo_files[i])

def get_google():
    google = [
            scalesim(
                save_disk_space=True, verbose=True,
                config='google.cfg',
                topology=topo,
                input_type_gemm=gemm
            ) 
            for topo in topo_files
        ]
    for i in range(len(google)):
        google[i].run_scale(top_path=f'./google/{topo_files[i]}')
        print('Finished running topology: ', topo_files[i])

def get_scale():
    scale = [
            scalesim(
                save_disk_space=True, verbose=True,
                config='scale.cfg',
                topology=topo,
                input_type_gemm=gemm
            ) 
            for topo in topo_files
        ]
    for i in range(len(scale)):
        scale[i].run_scale(top_path=f'./scale/{topo_files[i]}')
        print('Finished running topology: ', topo_files[i])

def get_variants():
    cfg = open('scale-sim-v2/configs/eyeriss.cfg')
    cp.read_file(cfg)

    net_names = ['FasterRCNN']
    flows = ['ws', 'is', 'os']
    srams = [60, 84, 108, 132, 156]
    pe_array = [(12, 14), (18, 21), (24, 28), (30, 35), (36, 42)]

    procs = []
    for net in net_names:
        topo = net + '.csv'
        for flow in flows:
            path = f'variant/{net}_{flow}'
            if os.path.exists(path):
                continue
            cp.set('architecture_presets', 'Dataflow', flow)
            with open('variant.cfg', 'w') as f:
                cp.write(f)
            s = scalesim(
                save_disk_space=True, verbose=True,
                config='variant.cfg',
                topology='scale-sim-v2/topologies/conv_nets/'+ topo,
                
                input_type_gemm=False
            )
            # s.run_scale(path)
            p = Process(target=s.run_scale, args=(path,))
            procs += [p]
            p.start()
        cp.read_file(cfg)
        for sram in srams:
            path = f'variant/{net}_IfmapSramSzkB{sram}'
            if os.path.exists(path):
                continue
            cp.set('architecture_presets', 'IfmapSramSzkB', str(sram))
            with open('variant.cfg', 'w') as f:
                cp.write(f)
            s = scalesim(
                save_disk_space=True, verbose=True,
                config='variant.cfg',
                topology='scale-sim-v2/topologies/conv_nets/'+ topo,
                
                input_type_gemm=False
            )
            # s.run_scale(path)
            p = Process(target=s.run_scale, args=(path,))
            procs += [p]
            p.start()
        cp.read_file(cfg)
        for sram in srams:
            path = f'variant/{net}_FilterSramSzkB{sram}'
            if os.path.exists(path):
                continue
            cp.set('architecture_presets', 'FilterSramSzkB', str(sram))
            with open('variant.cfg', 'w') as f:
                cp.write(f)
            s = scalesim(
                save_disk_space=True, verbose=True,
                config='variant.cfg',
                topology='scale-sim-v2/topologies/conv_nets/'+ topo,
                input_type_gemm=False
            )
            p = Process(target=s.run_scale, args=(path,))
            procs += [p]
            p.start()
            # s.run_scale(path)
        cp.read_file(cfg)
        for sram in srams:
            path = f'variant/{net}_OfmapSramSzkB{sram}'
            if os.path.exists(path):
                continue
            cp.set('architecture_presets', 'OfmapSramSzkB', str(sram))
            with open('variant.cfg', 'w') as f:
                cp.write(f)
            s = scalesim(
                save_disk_space=True, verbose=True,
                config='variant.cfg',
                topology='scale-sim-v2/topologies/conv_nets/'+ topo,
                input_type_gemm=False
            )
            # s.run_scale(path)
            p = Process(target=s.run_scale, args=(path,))
            procs += [p]
            p.start()
        cp.read_file(cfg)
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
        
        
        
# get_eyeriss()
# get_google()
# get_scale()
get_variants()