Code to download the data:

**FMA (Free Music Archive):**
```
cd FMA

# Download metadata for all FMA files
wget https://os.unil.cloud.switch.ch/fma/fma_metadata.zip
unzip fma_metadata.zip
rm fma_metadata.zip

# Download 30s audios a small subset of the FMA
wget https://os.unil.cloud.switch.ch/fma/fma_small.zip
unzip fma_small.zip
rm fma_small.zip
```

**MSD (Million Song Dataset):**

```
cd MSD

# Download track indexes that have at least 1 similar track associated
wget http://millionsongdataset.com/sites/default/files/lastfm/tracks_with_similar.txt

# Download a subset of lastfm songs
wget http://millionsongdataset.com/sites/default/files/lastfm/lastfm_subset.zip
unzip lastfm_subset.zip 
rm lastfm_subset.zip
```