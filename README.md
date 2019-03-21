# reach

## Prerequis
Installation des libs nécessaires

    pip install -r requirements.txt
    
## USAGE
- Parameters are defined in file **"properties.config"**

- Launch the search:
    
      reach.py <username>
    
## Steps
INFO : *<category.property>* from  properties.config

1) Get *<googleimages.limit>* METADATA from username, corresponding to the first 'x' google image results\
[API: https://github.com/hardikvasa/google-images-download#arguments]
    - "username.json" is stored in "./logs"
    
    
2) Get google images from each line of metadata file
    - each image is saved in *<googleimages.limit>*/"username"/1-xxxxxxx.jpg
    - all image are prefixed with index
    
## Trick
Change "twitterCredential" and hide the changes to git:
     
    git update-index --assume-unchanged twitter/twitterCredentials.txt
    
To track the changes again:

    git update-index --no-assume-unchanged <file>