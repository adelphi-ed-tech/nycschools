Installing in Google Colab
==========================

Link to the data resources from your Google Drive
-------------------------------------------------
1. Sign into your Google Account
2. Open the link to our source data files: <https://drive.google.com/drive/folders/1Yf7ZbK0S8HyYR7kL9_MUNePWj6a7GwbL?usp=share_link>
3. Create a shortcut to the data in your drive

```{image} res/add-gdrive.gif
:alt: menu navigation to add link to gdrive
:class: border p-2
```

Installing `nycschools`
----------------------
Open a new Colab notebook and then add this code at the start of your program:

```bash
# install the package and its requirements
!pip install nycschools
```
```python
# discover the data in your Google Drive, or download it to the local Colab
# if no suitable data is found
from nycschools import dataloader
dataloader.download_data()
```

The `dataloader` will prompt you for permission to look in your Google Drive for the data folder. If you do not allow access, the program will attempt to download the data locally. You will have to download the data for each session when using this notebook.
