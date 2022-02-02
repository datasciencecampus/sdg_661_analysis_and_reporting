# Colab Guide

The reporting makes use of Google Earth Engine and Google Drive. Therefore it is convenient
to run the code in the Google Colab environment. This environment already has most
of the required libraries installed so users are able to get up and running
quickly.

There is, however, some amount of user-configuration required and this guide
is intended to walk users through the necessary steps.

## Clone Repository

1. Go to colab.research.google.com and sign in to your account.
2. You should see a window in which you are prompted to select a notebook. In
the botton-right select `New notebook`. If no such prompt appears you can select `File -> New notebook` from the Colab menu bar.
3. In the notebook there is a panel on the left-hand side; click the folder icon to expand and see the Files panel.
Click the `Mount Drive` button at the top of the panel (the folder with the Google Drive logo). You will then have access
to your drive at `/drive/MyDrive`.
4. In the notebook cell run the following code to clone the `sdg_661_analysis_and_reporting`
repository to your Google Drive.

    ```python
    !git clone https://github.com/datasciencecampus/sdg_661_analysis_and_reporting.git /content/drive/MyDrive/sdg_661_analysis_and_reporting
    ```

    You should now be able to see this new directory in the Files panel.
You may need to refresh using the `Refresh` button next to `Mount Drive`.
5. This notebook has now served its purpose and can be closed. It will be stored in a
`Colab Notebooks` directory in your Drive and can be deleted from there.

## UK Reporting Setup
1. In your Google Drive navigate to your repository folder and double-click UK_reporting.ipynb to open the notebook in Colab.
2. Run the cells under the **Setup** section. These step through some important processes:
   1. Install missing libraries
   2. Import required libraries
   3. Mount Google Drive
   4. Change workspace to the `sdg_661_analysis_and_reporting` repository. If the repository
   was cloned to a different location it can be changed in the cell
       ```python
       repo_dir_name = 'sdg_661_analysis_and_reporting'
       ```
   5. Import the custom funtions from `GSWE_Reporting`
   6. Parse and display the versions of GWSE data that will be used in the analysis.
   7. Authenticate and initialise Google Earth Engine
3. Examine the contents of the cell under User Settings. Ensure you are happy with
the settings, particularly that the date range covers your intended time frame. Run the cell
when you are happy.

This concludes the setup process.

## Extract GSWE Imagery
Run the cells in this section to process and download the imagery for your specified
time frame. Note that the cell will finish executing but the imagery will not be available for some time.
You should check the link provided to track the progress.

A new directory will have been created at the root of your Drive using the
naming convention `gswe_exports_YYYYmmddHHMMSS`. Imagery will be
added to this directory as they are processed.

## Preparing HydroBASIN boundary
These cells step through the processing required to clip and reproject the hydrobasins data.

> **NOTE**
> 
> These cells can be run while you are waiting for the imagery to process.

## Preparing GSWE outputs
The first cell can be executed while the images are in the process of being
exported. It will report the number of images found and confirm
the path of the export folder.

>**WARNING**
>
>Only proceed with the next steps if you are satisifed that the GSWE imagery has successfully finished downloading.

All the remaining cells in this section and below can now be executed. To execute them you can
select `Runtime -> Run after` from the menu bar. Note that this will run all cells after
the currently select cell - so make sure you select the cell imediately above the first cell you want executed before selecting `Run after`.

The remaining cells will be executed sequentially run and generate the output files.
Scroll down the notebook and ensure that cells have executed successfully - they will have a green tick to the left of them.

Alternatively, users are encouraged to step through the remaining cells to get familiar with the process
and to quickly identify any issues.