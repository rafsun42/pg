pyinstaller -F src/pg.py

# Copies the binary to the directory provided
# in the .installdir file. It must have a single
# line.
cp ./dist/pg $(cat ./.installdir)
