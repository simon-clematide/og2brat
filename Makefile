
PYTHON:=/opt/local/bin/python2.7

test1: test/17608565/brat.txt test/17608565/brat.ann
#%brat.txt: %inputfilter_novartistxt_lingpipe_out.xml
#	$(PYTHON) lib/driver.py -f $< $(@D)/$$(basename $@ .txt)

%brat.ann %brat.txt: %inputfilter_novartistxt_termmatcher_ann_out.xml %chunker_out.xml %parser_out.xml %inputfilter_novartistxt_idfy_out.xml
	rm $@ || true
#	$(PYTHON) lib/driver.py -t $(word 1,$^) -c $(word 2,$^) -s $(word 3,$^) $(@D)/$$(basename $@ .ann)
	$(PYTHON) lib/driver.py -f  $(word 4,$^)  -t $(word 1,$^)  -c $(word 2,$^) -s $(word 3,$^) $(@D)/brat
