#TopoSum: Topographic Summary
#Rob Sowby
#11/14/2015

import math

DEM = []        # DEM begins as an empty list
SLOPE = []
ASPECT = []

size_i = 300
size_j = 300

def ReadDEM():
    DEM_file = open('UU_DEM.txt','r')

    # Read elevation values from textfile into a 2D array
    for line in DEM_file:
        #Set all to elevation just for structure; replace later
        DEM.append(line.split())
        SLOPE.append(line.split())
        ASPECT.append(line.split())
    DEM_file.close()
    for i in range(size_i):
        for j in range(size_j):
            DEM[i][j] = float(DEM[i][j])
            SLOPE[i][j] = float(SLOPE[i][j])
            ASPECT[i][j] = float(ASPECT[i][j])
    print 'DEM read complete. Size:',len(DEM[0]),'x',len(DEM)
    print ''
    
def calc_dem_bins():
    elev_max = 0
    elev_min = 10000
    elev_range = 0
    for i in range(size_i):
        for j in range(size_j):
            if DEM[i][j] > elev_max:
                elev_max = DEM[i][j]
            if DEM[i][j] < elev_min:
                elev_min = DEM[i][j]
                
    elev_range = elev_max - elev_min
    
    #Define bins
    bin_size = elev_range/5
    bin1 = elev_min + bin_size
    bin2 = bin1 + bin_size
    bin3 = bin2 + bin_size
    bin4 = bin3 + bin_size
    bin5 = elev_max
        
    #Initialize counters
    bin1count,bin2count,bin3count,bin4count,bin5count = 0,0,0,0,0
    count = 0.0
    
    for i in range(size_i):
        for j in range(size_j):
            count += 1
            if DEM[i][j] <= bin1:
                bin1count += 1
            elif DEM[i][j] <= bin2:
                bin2count += 1
            elif DEM[i][j] <= bin3:
                bin3count += 1
            elif DEM[i][j] <= bin4:
                bin4count += 1
            elif DEM[i][j] <= bin5:
                bin5count += 1
            else:
                print "Error"
    
    #Calculate percentages
    bin1pct = round(100*bin1count/count,1)
    bin2pct = round(100*bin2count/count,1)
    bin3pct = round(100*bin3count/count,1)
    bin4pct = round(100*bin4count/count,1)
    bin5pct = round(100*bin5count/count,1)
    
    print 'Elevation range:',elev_min,'to',elev_max
    print 'Difference:',elev_range
    print 'Bin size:',bin_size
    print 'Bin 1 (',elev_min,'to',bin1,'):',bin1pct,'%'
    print 'Bin 2 (',bin1,'to',bin2,'):',bin2pct,'%'
    print 'Bin 3 (',bin2,'to',bin3,'):',bin3pct,'%'
    print 'Bin 4 (',bin3,'to',bin4,'):',bin4pct,'%'
    print 'Bin 5 (',bin4,'to',bin5,'):',bin5pct,'%'
    print ''

def calc_slope_aspect():
    d = 10 #set spacing to 10 m
    for r in range(1, size_i - 1): #row
        for c in range(1, size_j - 1): #column
            bb = (DEM[r-1][c+1] + 2*DEM[r][c+1] + DEM[r+1][c+1] - DEM[r-1][c-1] - 2*DEM[r][c-1] - DEM[r+1][c-1])/(8*d)
            cc = (DEM[r-1][c-1] + 2*DEM[r-1][c] + DEM[r-1][c+1] - DEM[r+1][c-1] - 2*DEM[r+1][c] - DEM[r+1][c+1])/(8*d)
            s = math.degrees(math.atan(math.sqrt(bb**2 + cc**2)))
            
            #replace each row and column with slope value
            SLOPE[r][c] = s            
            
            if cc == 0: #Preempt division by zero
                a = -1
            else:
                a = math.degrees(math.atan(bb/cc)) #Pre-aspect
            
            if cc > 0:
                a += 180
            if cc < 0 and bb > 0:
                a += 360
            if cc == 0 and bb == 0:
                a = -1            
            
            #replace each row and column with aspect value            
            ASPECT[r][c] = a    
    
    #trim borders
    for i in range(size_i):
        for j in range(size_j):
            SLOPE[0][j] = None #top edge
            SLOPE[size_i - 1][j] = None #bottom edge
            SLOPE[i][0] = None #left edge
            SLOPE[i][size_j - 1] = None #right edge
            
            ASPECT[0][j] = None
            ASPECT[size_i - 1][j] = None
            ASPECT[i][0] = None
            ASPECT[i][size_j - 1] = None
        
    print 'Slope calculated.'    
    print ''
    print 'Aspect calculated.'
    print ''
    
        
def calc_slope_bins():
    slope_max = 0
    slope_min = 10000
    for i in range(1, size_i - 1):
        for j in range(1, size_j - 1):
            if SLOPE[i][j] > slope_max:
                slope_max = SLOPE[i][j]
                y,x = i,j
            if SLOPE[i][j] < slope_min:
                slope_min = SLOPE[i][j]
                
    #Initialize counters
    bin1count,bin2count,bin3count,bin4count = 0,0,0,0
    count = 0.0
    
    for i in range(1, size_i - 1):
        for j in range(1, size_j - 1):
            count += 1
            if SLOPE[i][j] < 10:
                bin1count += 1
            elif SLOPE[i][j] < 20:
                bin2count += 1
            elif SLOPE[i][j] < 30:
                bin3count += 1
            elif SLOPE[i][j] >= 30:
                bin4count += 1
            else:
                print "Error"
    
    #Calculate percentages
    bin1pct = round(100*bin1count/count,1)
    bin2pct = round(100*bin2count/count,1)
    bin3pct = round(100*bin3count/count,1)
    bin4pct = round(100*bin4count/count,1)
    
    print 'Slope range:',round(slope_min,1),'deg to',round(slope_max,1),'deg'
    print 'Bin 1 (< 10 deg)',bin1pct,'%'
    print 'Bin 2 (10 to 20 deg):',bin2pct,'%'
    print 'Bin 3 (20 to 30 deg):',bin3pct,'%'
    print 'Bin 4 (> 30 deg ):',bin4pct,'%'
    print ''    

def calc_aspect_bins():
    
    #Define compass directions            
    compass_tuple = ('NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW','N')
    compass_dir = {'NNE':22.5,'NE':45.0,'ENE':67.5,'E':90.0,'ESE':112.5,'SE':135.0,'SSE':157.5,'S':180.0,'SSW':202.5,'SW':225.0,'WSW':247.5,'W':270.0,'WNW':292.5,'NW':315.0,'NNW':337.5,'N':360.0}
    
    #Initialize counters
    compass_count = {'NNE':0,'NE':0,'ENE':0,'E':0,'ESE':0,'SE':0,'SSE':0,'S':0,'SSW':0,'SW':0,'WSW':0,'W':0,'WNW':0,'NW':0,'NNW':0,'N':0} 
    count = 0.0
    
    for i in range(1, size_i - 1):
        for j in range(1, size_j - 1):
            count += 1
            #Is there a better way to loop through compass points here???
            if ASPECT[i][j] < compass_dir['NNE']:
                compass_count['NNE'] += 1
            elif ASPECT[i][j] < compass_dir['NE']:
                compass_count['NE'] += 1
            elif ASPECT[i][j] < compass_dir['ENE']:
                compass_count['ENE'] += 1 
            elif ASPECT[i][j] < compass_dir['E']:
                compass_count['E'] += 1
            elif ASPECT[i][j] < compass_dir['ESE']:
                compass_count['ESE'] += 1                    
            elif ASPECT[i][j] < compass_dir['SE']:
                compass_count['SE'] += 1                    
            elif ASPECT[i][j] < compass_dir['SSE']:
                compass_count['SSE'] += 1                    
            elif ASPECT[i][j] < compass_dir['S']:
                compass_count['S'] += 1                    
            elif ASPECT[i][j] < compass_dir['SSW']:
                compass_count['SSW'] += 1                
            elif ASPECT[i][j] < compass_dir['SW']:
                compass_count['SW'] += 1
            elif ASPECT[i][j] < compass_dir['WSW']:
                compass_count['WSW'] += 1                 
            elif ASPECT[i][j] < compass_dir['W']:
                compass_count['W'] += 1                     
            elif ASPECT[i][j] < compass_dir['WNW']:
                compass_count['WNW'] += 1                     
            elif ASPECT[i][j] < compass_dir['NW']:
                compass_count['NW'] += 1
            elif ASPECT[i][j] < compass_dir['WNW']:
                compass_count['WNW'] += 1
            elif ASPECT[i][j] < compass_dir['N']:
                compass_count['N'] += 1                         
    
    for key in compass_dir:
        compass_count[key] = 100*compass_count[key]/count #replace with percentages
    
    print 'Aspect breakdown:'
    for key in compass_tuple:
        print key,':',round(compass_count[key],1),'%'

def main():
    
    ReadDEM()
   
    calc_dem_bins()
    
    calc_slope_aspect()
    
    calc_slope_bins()
    calc_aspect_bins()
  
main()
