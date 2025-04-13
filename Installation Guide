## To find motifs of a fasta file 
# MEME Suite
# Ubuntu -> download meme-5.5.7 file from https://meme-suite.org/meme/doc/download.html
tar zxf meme-5.5.7.tar.gz
cd meme-5.5.7
./configure --prefix=~/meme_install --enable-build-libxml2 --enable-build-libxslt
make
make install
~/meme_install/bin/meme -version
# output: 5.5.7
#FIMO
~/meme_install/bin/fimo --oc output ~/Zma_TF_binding_motifs.meme ~/Zea_mays.fa  
