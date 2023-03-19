#v1.0.0
import tkinter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import subprocess
import pandas as pd
import time

gpu_name        = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout
driver_ver      = subprocess.run(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout
memory_total    = int(subprocess.run(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)

if subprocess.run(['nvidia-smi', '--query-gpu=power.limit', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout != '[N/A]':
    pwr_max     = float(subprocess.run(['nvidia-smi', '--query-gpu=power.limit', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)
else:
    pwr_max     = -1

TIME_RANGE = 60000 #[ms]
DIFF = 500 #[ms]
DATA_ROW_N = int(TIME_RANGE/DIFF)

columns = ['timestamp', 'util_gpu', 'memory_used', 'gpu_temp', 'pwr_used', 'util_vram', 'util_pwr']
df = pd.DataFrame(np.zeros((DATA_ROW_N + 1, len(columns))), columns=columns)

fig = plt.figure('NVIDIA GPU MONITOR')
ax_1 = fig.add_subplot(2,2,1)
ax_2 = fig.add_subplot(2,2,2)
ax_3 = fig.add_subplot(2,2,3)
ax_4 = fig.add_subplot(2,2,4)

fig = plt.figure()
t = np.linspace(-TIME_RANGE/1000, 0, DATA_ROW_N + 1)
ax_1 = fig.add_subplot(2,2,1)
ax_2 = fig.add_subplot(2,2,2)
ax_3 = fig.add_subplot(2,2,3)
ax_4 = fig.add_subplot(2,2,4)
line_1, = ax_1.plot(t, np.zeros(DATA_ROW_N + 1), 'green')
line_2, = ax_2.plot(t, np.zeros(DATA_ROW_N + 1), 'blue')
line_3, = ax_3.plot(t, np.zeros(DATA_ROW_N + 1), 'red')
line_4 = ax_4.plot()


ax_1.set_xlim(-TIME_RANGE/1000, 0)
ax_1.set_ylim(0, 100)
ax_1.set_xlabel('time[s]')
ax_1.set_ylabel('GPU_Usage[%]')
ax_1.grid()

ax_2.set_xlim(-TIME_RANGE/1000, 0)
ax_2.set_ylim(0, 100)
ax_2.set_xlabel('time[s]')
ax_2.set_ylabel('VRAM_Usage[%]')
ax_2.grid()

ax_3.set_xlim(-TIME_RANGE/1000, 0)
ax_3.set_ylim(0, 100)
ax_3.set_xlabel('time[s]')
ax_3.set_ylabel('PowerUsage[%]')
ax_3.grid()

ax_4.spines['right'].set_visible(False)
ax_4.spines['top'].set_visible(False)
ax_4.spines['bottom'].set_visible(False)
ax_4.spines['left'].set_visible(False)
ax_4.tick_params('x', length=0, which='major')
ax_4.tick_params('y', length=0, which='major')
ax_4.xaxis.set_visible(False)
ax_4.yaxis.set_visible(False)
info_txt = ''
text_4 = ax_4.text(0.5, 0.5, info_txt, va='center', ha='center', transform=ax_4.transAxes)
fig.tight_layout()

def quit_mainloop():
    root.quit()
    root.destroy()
def update(frame):
    start_time = time.time()
    for j in range(DATA_ROW_N):
        df['timestamp'][j]       =   df['timestamp'][j+1]
        df['util_gpu'][j]       =   df['util_gpu'][j+1]
        df['memory_used'][j]    =   df['memory_used'][j+1]
        df['gpu_temp'][j]       =   df['gpu_temp'][j+1]
        df['pwr_used'][j]       =   df['pwr_used'][j+1]
        df['util_vram'][j]      =   df['util_vram'][j+1]
        df['util_pwr'][j]       =   df['util_pwr'][j+1]

    df['util_gpu'][DATA_ROW_N]      =   int(subprocess.run(['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)
    df['memory_used'][DATA_ROW_N]   =   int(subprocess.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)
    df['gpu_temp'][DATA_ROW_N]      =   int(subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)
    df['util_vram'][DATA_ROW_N]     =   (df['memory_used'][DATA_ROW_N] / memory_total) * 100
    df['util_pwr'][DATA_ROW_N]      =   (df['pwr_used'][DATA_ROW_N] / pwr_max) * 100

    if subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout != '[N/A]':
        df['pwr_used'][DATA_ROW_N]  =   float(subprocess.run(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], capture_output=True, text=True).stdout)
    else:
        df['pwr_used'][DATA_ROW_N]  =   -1
    
    end_time = time.time()
    calc_time = end_time - start_time
    df['timestamp'][DATA_ROW_N]     =   start_time + calc_time/2
    
    info_txt_1 = 'GPU Name: ' + gpu_name + '\n'
    info_txt_2 = 'Driver Version: ' + driver_ver + '\n'
    info_txt_3 = 'GPU Usage: ' + str(df['util_gpu'][DATA_ROW_N]) + '[%]' + '\n'
    info_txt_4 = 'VRAM Usage: ' + str(df['memory_used'][DATA_ROW_N]) + '/' + str(memory_total) + '[MiB]' + '\n'
    info_txt_5 = 'Power Usage: ' + str(df['pwr_used'][DATA_ROW_N]) + '/' + str(pwr_max) + '[W]' + '\n'
    info_txt_6 = 'GPU Temperature: ' + str(df['gpu_temp'][DATA_ROW_N]) + '[°C]'
    info_txt = info_txt_1 + info_txt_2 + info_txt_3 + info_txt_4 + info_txt_5 + info_txt_6
    text_4.set_text(info_txt)

    line_1.set_ydata(df['util_gpu'])
    line_2.set_ydata(df['util_vram'])
    line_3.set_ydata(df['util_pwr'])
    return line_1,line_2,line_3,text_4

def save_csv():
    filename = tkinter.filedialog.asksaveasfilename(filetypes=[('CSV', '.csv')],)
    try:
        df.to_csv(filename)
    except:
        pass
root = tkinter.Tk()
root.wm_title('NVIDIA GPU MONITOR')
root.geometry('800x450')
root.minsize(width=800, height=450)

button = tkinter.Button(root, text='Save CSV file', command=save_csv)
button.pack(side=tkinter.BOTTOM)
canvas = FigureCanvasTkAgg(fig, master=root)
ani = animation.FuncAnimation(fig, update, interval=DIFF, blit=True)
canvas.get_tk_widget().pack(expand=1, fill='both')
root.protocol('WM_DELETE_WINDOW', quit_mainloop)
root.mainloop()