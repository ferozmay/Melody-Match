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

# Download a 1% subset of all MSD
wget http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz

# Download only metadata from MSD
wget http://millionsongdataset.com/sites/default/files/AdditionalFiles/msd_summary_file.h5

# Download low-level features from MSD
wget https://www.ifs.tuwien.ac.at/mir/msd/downloads/msd-jmir-spectral-all-all-v1.0.arff.gz
gunzip msd-jmir-spectral-all-all-v1.0.arff.gz
wget https://www.ifs.tuwien.ac.at/mir/msd/downloads/msd-jmir-mfcc-all-v1.0.arff.gz
gunzip msd-jmir-mfcc-all-v1.0.arff.gz
wget https://www.ifs.tuwien.ac.at/mir/msd/downloads/msd-jmir-spectral-all-derivatives-all-v1.0.arff.gz
gunzip msd-jmir-spectral-all-derivatives-all-v1.0.arff.gz
# Get timbral features
wget https://www.ifs.tuwien.ac.at/mir/msd/downloads/msd-marsyas-timbral-v1.0.arff.gz
gunzip msd-marsyas-timbral-v1.0.arff.gz

# Get genres
wget https://www.tagtraum.com/genres/msd_tagtraum_cd1.cls.zip
unzip msd_tagtraum_cd1.cls.zip
rm msd_tagtraum_cd1.cls.zip

```