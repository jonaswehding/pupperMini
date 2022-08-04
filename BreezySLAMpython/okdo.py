from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import Okdo as LaserModel
import okdoLidar
from PIL import Image
MAP_SIZE_PIXELS         = 300
MAP_SIZE_METERS         = 15

slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

while True:
    angles,distances = okdoLidar.getFrame()
    slam.update(distances[0:360], scan_angles_degrees=angles[0:360])
    x, y, theta = slam.getpos()
    #print(theta,x,y)
    slam.getmap(mapbytes)
    image = Image.frombuffer('L', (MAP_SIZE_PIXELS, MAP_SIZE_PIXELS), mapbytes, 'raw', 'L', 0, 1)
    image.save('/home/pi/stream/pips.jpg')
  
