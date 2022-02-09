To calculate the soil moisture using NDVI and Sentinel1 data, first we need to extract the relationship between NDVI and the backscatter difference from minimum at the same dates.
To do so, first we preprocess Sentinel1 data which includes applying orbit file, thermal noise removal, calibration, speckle filtering, terrain correction, resampling and converting to dB.
Then, we calculate the minimum and maximum backscatter for each pixel in the timeseries we have (which is the whole year of 2020). 
Next, the minimum is subtracted from backscatters in different dates. On the other hand, NDVI is calculated for different dates. 
For the common dates between NDVI and Sentinel1, a plot is drawn between NDVI and difference backscatter for each pixel. 
Finally, the regression relation for NDVI and backscatter is extracted which is in this form: Δσmax=f(NDVI)=a NDVI+Δσ(baremax)
