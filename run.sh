# python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/eyeriss.cfg" -t "scale-sim-v2/topologies/conv_nets/mobilenet.csv" -p "archs/mobilenet/eyeriss" 
# python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/google.cfg" -t "scale-sim-v2/topologies/conv_nets/mobilenet.csv" -p "archs/mobilenet/google" 
# python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/scale.cfg" -t "scale-sim-v2/topologies/conv_nets/mobilenet.csv" -p "archs/mobilenet/scale" 


python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/eyeriss.cfg" -t "scale-sim-v2/topologies/conv_nets/yolo_tiny.csv" -p "archs/yolotiny/eyeriss" 
python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/google.cfg" -t "scale-sim-v2/topologies/conv_nets/yolo_tiny.csv" -p "archs/yolotiny/google" 
python3 "scale-sim-v2/scalesim/scale.py" -c "scale-sim-v2/configs/scale.cfg" -t "scale-sim-v2/topologies/conv_nets/yolo_tiny.csv" -p "archs/yolotiny/scale" 