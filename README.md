# watchdicom
Small Script that observes the arrival of dicom file a tries to send it to a PACS. 
## How To Use
1. Dependencies
    * watchdog
    * pydicom
    * pynetdicom
2. Set your credntials

![image](https://user-images.githubusercontent.com/50750666/192873361-f8d29eb5-610d-481d-b3a8-ff2ebcab74f0.png)

3. Run the script. While running, watchdog dicom will listen the creation of DICOM files on the folder that it is in. It listens to sub-folders as well.
