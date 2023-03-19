# NVIDIA_GPU_MONITOR
NVIDIA GPU monitoring tools on ubuntu computers

## Requirement
GPU: Only single GPU from NVIDIA supported

OS:　Confirmed to run with Ubuntu 20.04 or higher

## Install
First, install the NVIDIA driver and make sure 'nvidia-smi' can run.
```
$ git clone https://github.com/Yujisuper/NVIDIA_GPU_MONITOR.git
$ pip3 install tkinter
$ pip3 install matplotlib
$ pip3 install pandas
```
After installation, it is recommended to set up shortcuts as follows

Settings -> Keyboard Shortcuts -> + 

```
Name: Any
Command: python3 (absolute path)/NVIDIA_GPU_MONITOR/nvidia_gpu_monitor.py
Shortcut: Any

```

Name: Any

Command: python3 (absolute path)/NVIDIA_GPU_MONITOR/nvidia_gpu_monitor.py

Shortcut: Any

## Usage
Use the shortcut or run the following command.
```
$ cd absolute path)/NVIDIA_GPU_MONITOR/
$ python3 nvidia_gpu_monitor.py
```
Running the program will display the GPU usage status.

Click 'Save CSV file' button to save the GPU status displayed in csv format.

## Note
The times shown in the graphs are approximate.

When used as a graph, plotting a plot saved in csv is more accurate in time than the GUI display.
