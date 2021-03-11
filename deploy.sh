#/bin/bash

###
set -e

# decrypt deploy key
# openssl aes-256-cbc -K $encrypted_56a395b73f83_key -iv $encrypted_56a395b73f83_iv -in travisci_rsa.enc -out travisci_rsa -d
# chmod 600 travisci_rsa
# eval `ssh-agent -s`
# ssh-add travisci_rsa
# rm travisci_rsa

# config git
# git config user.name "Travis CI"
# git config user.email "$COMMIT_AUTHOR_EMAIL"
# git config --global user.email "$COMMIT_AUTHOR_EMAIL"
# git config --global user.name "Travis CI"
# git config push.default tracking
# GITHUB_REPO_URL=`git remote -v | grep -m1 '^origin' | sed -Ene's#.*(https://[^[:space:]]*).*#\1#p'`
# GITHUB_USER=`echo $GITHUB_REPO_URL | sed -Ene's#https://github.com/([^/]*)/(.*).git#\1#p'`
# GITHUB_REPO=`echo $GITHUB_REPO_URL | sed -Ene's#https://github.com/([^/]*)/(.*).git#\2#p'`
# GITHUB_REPO_SSH_URL="git@github.com:$GITHUB_USER/$GITHUB_REPO.git"
# git remote set-url origin $GITHUB_REPO_SSH_URL

# generate template
# cd template
# npm install
# grunt build
# cp dist/js/app.js ../SalmoNet/themes/SalmoNet/static/js/app.js
# cp dist/css/style.css ../SalmoNet/themes/SalmoNet/static/css/style.css
# cp node_modules/uikit/dist/fonts/* ../SalmoNet/themes/SalmoNet/static/css/fonts/
# cd ..

# process data
echo " 1/5 - process data"
rm -rf dist/
cd scripts
python3 deploy.py
cd ..

# prepare deploy repo
echo " 2/5 - prepare deploy repo"
mkdir -p dist
git clone git@github.com:korcsmarosgroup/SalmoNet2.git dist
cd dist
git checkout gh-pages
git rm -rf *
cd ..

# generate static site
echo " 3/5 - generate static site"
cd SalmoNet
hugo
cd ..

# copy site to dist
echo " 4/5 - copy site to dist"
cd scripts
python3 _change_ortholog_ids.py
cd ..
rm -rf SalmoNet/public/download/*.csv
rm -rf SalmoNet/public/download/*.cys
cp -r SalmoNet/public/* dist
# echo "salmonet.org" > dist/CNAME

# deploy
echo " 5/5 - deploy"
cd dist
git add --all
git commit -am "automatic deploy"
git push origin gh-pages
cd ..

#remove deploy key
# ssh-add -D
