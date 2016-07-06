#/bin/bash

invoke template.deploy
invoke data.copy_deploy
invoke data.export_protein_pages
invoke dist_clone
invoke deploy
invoke clean_all
