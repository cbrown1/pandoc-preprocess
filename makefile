test_critic: test/test_critic.md
	mkdir -p build
	mkdir -p out
	python src/pandoc_preprocessor_criticmarkup.py -p show -o build/test_critic_revised.md test/test_critic.md
	python src/pandoc_preprocessor_criticmarkup.py -p hide -o build/test_critic_original.md test/test_critic.md
	python src/pandoc_preprocessor_criticmarkup.py -p show -o build/test_critic_tracked.md \
	--addition="\textcolor{green}{@str}" --deletion="\textcolor{red}{@str}" --comment="\textcolor{blue}{[@str]}" \
	--substitution="\textcolor{yellow}{@str}" --highlight="\textcolor{magenta}{@str}" test/test_critic.md
	python src/pandoc_preprocessor_criticmarkup.py -p list test/test_critic.md > out/critic_changes.yaml
	pandoc -o out/test_critic_revised.pdf build/test_critic_revised.md
	pandoc -o out/test_critic_original.pdf build/test_critic_original.md
	pandoc -o out/test_critic_tracked.pdf build/test_critic_tracked.md

test_macros: test/test_macros.md
	python src/pandoc_preprocessor_macros.py -o build/test_macros.md test/test_macros.md
	pandoc -s -o build/test_macros.tex build/test_macros.md
	pdflatex -output-directory=build build/test_macros.tex
	cp build/test_macros.tex out/
	cp build/test_macros.pdf out/

test_dates: test/test_dates.md
	mkdir -p build
	mkdir -p out
	python pandoc_preprocessor_syllabus_dates.py -o build/test_dates.md -y 2017 test/test_dates.md
	pandoc -o out/test_dates.pdf build/test_dates.md

clean:
	-rm -rf build
	-rm -rf out

install:
	install -D src/pandoc_preprocessor_criticmarkup.py /usr/local/bin/pandoc_preprocessor_criticmarkup.py
	install -D src/pandoc_preprocessor_macros.py /usr/local/bin/pandoc_preprocessor_macros.py
	install -D src/pandoc_preprocessor_syllabus_dates.py /usr/local/bin/pandoc_syllabus_dates.py
	ln -s /usr/local/bin/pandoc_preprocessor_criticmarkup.py /usr/local/bin/pandoc_preprocessor_criticmarkup
	ln -s /usr/local/bin/pandoc_preprocessor_macros.py /usr/local/bin/pandoc_preprocessor_macros
	ln -s /usr/local/bin/pandoc_preprocessor_syllabus_dates.py /usr/local/bin/pandoc_preprocessor_syllabus_dates

uninstall:
	-rm /usr/local/bin/pandoc_preprocessor_criticmarkup
	-rm /usr/local/bin/pandoc_preprocessor_macros
	-rm /usr/local/bin/pandoc_preprocessor_syllabus_dates
	-rm /usr/local/bin/pandoc_preprocessor_criticmarkup.py
	-rm /usr/local/bin/pandoc_preprocessor_macros.py
	-rm /usr/local/bin/pandoc_preprocessor_syllabus_dates.py

