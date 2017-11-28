set +e

source activate blog
make html
cp -r output/* ../hgrif.github.io/
