# download each booklet
wget -P booklets/ -i booklet_urls.txt

# normalise file names (only keep year)
for f in booklets/*.pdf; 
    do mv "$f" booklets/"$(echo "$f" | sed s/[^0-9]//g)".pdf; 
done
mv booklets/20150.pdf booklets/2015.pdf # edge case