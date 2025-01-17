
import numpy as np
import matplotlib.pyplot as plt
import os 
import skimage as ski
import skimage.feature
import matplotlib.pyplot as plt
import nibabel                      as nib
import nibabel.freesurfer.mghformat as mgh
from scipy.ndimage import zoom
from glob import glob
def processmgz(path_of_mgz):
    brains=[]
    files = glob(os.path.join(path_of_mgz, '*.mgz'))
    print(len(files))
    for file in files:
        mgh_file = mgh.load(file)# for each mgz file
        data = np.asarray(mgh_file.dataobj, dtype=np.uint8)
        new_array = zoom(data, (0.5, 0.5, 0.5))
        #data = np.resize(data, 256,256,256) 
        brains.append(new_array)
    
    brains=np.asarray(brains)
    
    SIZE = 128
    X=np.asarray(brains)
    coord=[]
    for i in range(X.shape[0]):
      buf=X[i, :, :, :]
      buf=buf.reshape((SIZE,SIZE,SIZE))
      xmin=0
      xmax=0
      ymin=0
      ymax=0
      zmin=0
      zmax=0
      for xm in range(0, SIZE):
        if np.sum(buf[xm, :, :])>50:
          xmin=xm
          break
      for xm in range(0, SIZE):
        if np.sum(buf[SIZE-1-xm, :, :])>50:
          xmax=SIZE-1-xm
          break
      for ym in range(0,SIZE):
        if np.sum(buf[:, ym, :])>50:
          ymin=ym
          break
      for ym in range(0, SIZE):
        if np.sum(buf[:, SIZE-1-ym, :])>50:
          ymax=SIZE-1-ym
          break
      for zm in range(0, SIZE):
        if np.sum(buf[:, :, zm])>50:
          zmin=zm
          break
      for zm in range(0, SIZE):
        if np.sum(buf[:, :, SIZE-1-zm])>50:
          zmax=SIZE-1-zm
          break
      td=[]
      td.append(abs(xmax+xmin)/2)
      td.append(abs(ymax+ymin)/2)
      td.append(abs(zmax+zmin)/2)
      coord.append(td)
    
    x_range=82
    y_range=86
    z_range=100
    date1=[]
    data_new=[]
    label=[]
    id_list=[]
    for i in range(X.shape[0]):
      buf=X[i, :, :, :]
      co=coord[i]
      buf=buf.reshape((SIZE,SIZE,SIZE))
      data_new.append(buf[int(int(co[0])-(x_range/2)):int(int(co[0])+(x_range/2)), int(int(co[1])-(y_range/2)):int(int(co[1])+(y_range/2)), int(int(co[2])-(z_range/2)):int(int(co[2])+(z_range/2))])
    data_new = np.expand_dims(data_new, axis=4) # reshape the brain MRI from 3D to 4D
    return data_new
    
# if __name__ == '__main__':
#     tmp=np.zeros((82, 86, 100))
#     data = process_brain_mgz(tmp)
    #return 0