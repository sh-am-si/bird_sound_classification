#!/bin/sh

touch .git/hooks/pre-commit
echo "#!/bin/sh" > .git/hooks/pre-commit
echo >> .git/hooks/pre-commit
# echo "chmod 777 src/*.ipynb" >> .git/hooks/pre-commit # requires root user
echo "chmod 777 *.ipynb" >> .git/hooks/pre-commit # requires root user
echo >> .git/hooks/pre-commit
echo "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace src/*.ipynb" >> .git/hooks/pre-commit
echo >> .git/hooks/pre-commit
echo "git add ." >> .git/hooks/pre-commit

chmod +x .git/hooks/pre-commit 