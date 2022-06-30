# CMORPH

## Overview
The NOAA CPC MORPHing technique produces global precipitation analyses at very high spatial and temporal resolution. 
The following description is from the [NOAA Climate Data Record CMORPH dataset page](https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00948):

This data set is for the bias-corrected, reprocessed CPC Morphing technique (CMORPH) high-resolution global satellite precipitation estimates. The CMORPH satellite precipitation estimates are created in two steps. First, the purely satellite-based global fields of precipitation are constructed through integrating Level 2 retrievals of instantaneous precipitation rates from all available passive microwave measurements aboard low earth orbiting platforms. Bias in these integrated satellite precipitation estimates is then removed through comparison against CPC daily gauge analysis over land and adjustment against the Global Precipitation Climatology Project (GPCP) merged analysis of pentad precipitation over ocean. 
The bias corrected CMORPH satellite precipitation estimates are created on an 8 km by 8 km grid over the global domain from 60 degrees S to 60 degrees N and in a 30-minute interval from January 1998 to present. Due to the delay of some input data sets, this formal version (Version 1) bias corrected CMORPH is produced manually once a month at a latency of 3-4 months. 

More information is available from the [NCEI website](https://www.ncei.noaa.gov/products/climate-data-records/precipitation-cmorph) and from the [NCAR Climate Data Guide](https://climatedataguide.ucar.edu/climate-data/cmorph-cpc-morphing-technique-high-resolution-precipitation-60s-60n) website.

## Data download

The data is downloaded from the [RDA data server](https://rda.ucar.edu/data/ds502.2/). 
Updates are run regularly via the [accessdev Jenkins server](https://accessdev.nci.org.au/jenkins/job/aus-ref-clim-data-nci/job/CMORPH/). 
The code used is python based and it is a modification of a RDA server download code. 
To see all the options:
    python cmorph.py --help
A record of updates is kept in `update_log.txt`.

## Data location

We've downloaded CMORPH v1.0 data to

```
/g/data/ia39/aus-ref-clim-data-nci/cmorph/data/v1.0/30min/8km/<yr>/<mn>/<files>
```

## License

Use liability: NOAA and NCEI cannot provide any warranty as to the accuracy, reliability, or completeness of furnished data. Users assume responsibility to determine the usability of these data. The user is responsible for the results of any application of this data for other than its intended purpose.

## Data citation

Xie, Pingping; Joyce, Robert; Wu, Shaorong; Yoo, S.-H.; Yarosh, Yelena; Sun, Fengying; Lin, Roger, NOAA CDR Program (2019): NOAA Climate Data Record (CDR) of CPC Morphing Technique (CMORPH) High Resolution Global Precipitation Estimates, Version 1 Full resolution data. NOAA National Centers for Environmental Information. https://doi.org/10.25921/w9va-q159 [access date]

  
## References

Xie, P., R. Joyce, S. Wu, S. Yoo, Y. Yarosh, F. Sun, and R. Lin, 2017: Reprocessed, Bias-Corrected CMORPH Global High-Resolution Precipitation Estimates from 1998 J. Hydrometeor., 18, 1617-1641 (DOI: 10.1175/JHM-D-16-0168.1).

Joyce, R. J., J. E. Janowiak, P. A. Arkin, and P. Xie, 2004: CMORPH: A Method that Produces Global Precipitation Estimates from Passive Microwave and Infrared Data at High Spatial and Temporal Resolution Journal of Hydrometeorology, 5, 487-503 (DOI: 10.1175/1525-7541(2004)005<0487:CAMTPG>2.0.CO;2).

## Acknowledgement

No statement provided.

## Author note


## Assistance

For assistance with CMORPH data on NCI, open a new issue at https://github.com/aus-ref-clim-data-nci/CMORPH/issues
