NOSE=/usr/bin/nosetests3

# On Fedora:
#NOSE=/usr/bin/nosetests-3.2

clean:
	git clean -Xfd

test:
	$(NOSE) ./tests/*
