RSYNC=rsync -zcav \
	--exclude=\*~ --exclude=.\* \
	--delete-excluded --delete-after \
	--no-owner --no-group \
	--progress --stats

doc: .sphinx-stamp

doc-upload:
	$(RSYNC) build/doc/ wrobell@dcmod.org:~/public_html/atimer

.sphinx-stamp:
	PYTHONPATH=. sphinx-build doc build/doc
