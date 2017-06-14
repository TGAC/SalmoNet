.PHONY : clean template data hugo_generate prepare_deploy_repo copy_site_to_dist deploy_github travis dev_data serve

clean:
	rm -rf scripts/temp_data
	mkdir -p scripts/temp_data
	rm -rf SalmoNet/content/protein
	mkdir -p SalmoNet/content/protein
	rm -rf SalmoNet/public
	mkdir -p SalmoNet/public
	rm -rf dist
	mkdir -p dist

template:
	cd template; \
		npm install; \
		grunt build; \
		cp dist/js/app.js ../SalmoNet/themes/SalmoNet/static/js/app.js; \
		cp dist/css/style.css ../SalmoNet/themes/SalmoNet/static/css/style.css; \
		cp node_modules/uikit/dist/fonts/* ../SalmoNet/themes/SalmoNet/static/css/fonts/

data:
	cd scripts; \
		python3 deploy.py

dev_data: clean
	cd scripts; \
		python3 deploy.py dev

hugo_generate: data template
	cd SalmoNet; \
		hugo --uglyURLs

prepare_deploy_repo: hugo_generate deploy_config
	mkdir -p dist
	git clone git@github.com:TGAC/SalmoNet.git dist
	cd dist; \
		git checkout gh-pages; \
		git rm -rf *

copy_site_to_dist: prepare_deploy_repo
	cp -r SalmoNet/public/* dist
	echo "salmonet.org" > dist/CNAME

deploy_github: copy_site_to_dist
	cd dist; \
		git add --all; \
		git commit -am "automatic deploy"; \
		git push origin gh-pages

travis: deploy_github
	ssh-add -D

serve: dev_data template
	cd SalmoNet; \
		hugo serve --uglyURLs
