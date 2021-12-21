# inkbxm

INKscape BoXMaster Extension

# Coding

```bash
rm -rf inkbxm
git clone git@github.com:grettke/inkbxm.git
cd -
````

# Deployment

## macOS

```bash
cd /Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions
rm inkbxm.inx
rm inkbxm.py
ln -s ~/src/inkbxm/inkbxm.inx inkbxm.inx
ln -s ~/src/inkbxm/inkbxm.py inkbxm.py
cd -
```
