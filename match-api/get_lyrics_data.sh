# Get lyrics data

pip install fasttext
cd match-api/

# Download lyrics dataset
cd data/stored_data/
wget http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_train.txt.zip
wget http://millionsongdataset.com/sites/default/files/AdditionalFiles/mxm_dataset_test.txt.zip
cd ../../

# 1st time it will download the fasttext model and exit. It'll take a while
python -m index.lyrics_expansion_init

# Move to appropriate folder
mv cc.en.300.bin models/

# 2nd time it will create all necessary dataframes. It should only take a few mins
python -m index.lyrics_expansion_init

Then you should have everything installed for query expansion