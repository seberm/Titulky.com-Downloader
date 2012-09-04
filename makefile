NOSE=/usr/bin/nosetests3


clean:
	git clean -Xfd

test:
	$(NOSE) ./tests/*
