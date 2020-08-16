#define PY_SSIZE_T_CLEAN

#include <cstdlib>
#include <iostream>
#include <fstream> 
#include <vector>
#include <string> 

#include <gclue-simple.h>

/*
 * Fetches the geolocation of the device. 
 * 
 * Currently the geolocation part is working. 
 * todo: finish up its interface with the intended program (cache files). 
 */

int main(int argc, char** argv){
    std::string desktopID; 
    std::string runDir; 
    std::string cacheDir; 
    std::vector<std::string> argV; 
    int refreshInterval; 
    /*
     * Command line options: 
     * -i desktopID
     * -d cache file directory
     * -r refresh time, in seconds
     */
    runDir = argv[0];
    int c;  
    while ((c=getopt(argc, argv, "i:d:r:"))!=-1){
        switch (c){
        case 'i': 
            desktopID = optarg; 
            break; 
        case 'd': 
            cacheDir = optarg; 
            break; 
        case 'r': 
            refreshInterval = atoi(optarg); 
            break; 
        case '?': 
            if (optopt=='d'){
                std::cout << "-d requires an argument for cache directory." << std::endl; 
            }else if (optopt=='r'){
                std::cout << "-r requires an argument for refresh interval." << std::endl;
            }else if (isprint(optopt)){ 
                std::cout << "unknown option -" << c << std::endl;
            }
            std::cout << "Abort." << std::endl; 
            return 1; 
        }
    }
    std::cout << desktopID << std::endl; 
    std::cout << cacheDir << std::endl; 
    std::cout << refreshInterval << std::endl; 
    

    //Hardcoded here so that it cannot be changed at runtime
    GClueAccuracyLevel accuracy = GCLUE_ACCURACY_LEVEL_CITY; 
    GCancellable* cancellablePtr = NULL; 
    GError** errorPtr = NULL; 
    gpointer usrDataPtr; 

    GClueSimple* gclueService = gclue_simple_new_sync(
        desktopID.c_str(), 
        accuracy, 
        cancellablePtr, 
        errorPtr
    ); 

    GValue* rstPtr = NULL; 

    GClueLocation* locPtr; 
    
    //Gets geographical info, writes it into the cache file periodically 
    //  according to the interval specified. 
    locPtr = gclue_simple_get_location(gclueService);
    gdouble latitude = gclue_location_get_latitude(locPtr); 
    gdouble longtitude = gclue_location_get_longitude(locPtr); 

    std::ofstream cache (cacheDir, std::ofstream::trunc);
    std::string latS = "lat: " + std::to_string(latitude); 
    std::string lonS = "lon: " + std::to_string(longtitude); 
    cache << latS << "\n" << lonS << std::endl; 
    cache.close(); 
}