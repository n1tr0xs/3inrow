# Pyinstaller template

## How to use:
1. Set `env.app_name` (`app_name` must be same as in `build.spec`).
2. `build.spec` must be in `src` folder.
3. `requirements.txt` (create empty file if u don't have requirements) must be in repo root directory.

## Mainloop:
1. Push commits
2. Create and push tag
```
git tag -f <tagname> && git push origin <tagname>
```
3. Fast tag repush:
```
git push origin :<tagname> & git tag -f <tagname> & git push -f origin <tagname>
```
