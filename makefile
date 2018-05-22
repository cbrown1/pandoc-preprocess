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
	python src/pandoc_preprocessor_syllabus_dates.py -o build/test_dates.md -y 2017 test/test_dates.md
	pandoc -o out/test_dates.pdf build/test_dates.md

test_insertlines: test/test_file_lines_data.md
	mkdir -p build
	mkdir -p out
	python src/pandoc_preprocessor_insert_lines.py -o build/test_data.md -d test/test_file_lines_data.md test/test_file_lines_source.md
	pandoc -o out/test_data.pdf build/test_data.md

test_questionorders: test/index.html
	mkdir -p build
	mkdir -p out
	python src/pandoc_preprocessor_insert_lines.py -o out/new_index.html -x test/Unit1_q_order_A.txt -x test/Unit1_q_order_B.txt test/index.md

clean:
	-rm -rf build
	-rm -rf out

install:
	install -D src/pandoc_preprocessor_criticmarkup.py /usr/local/bin/pandoc_preprocessor_criticmarkup.py
	install -D src/pandoc_preprocessor_macros.py /usr/local/bin/pandoc_preprocessor_macros.py
	install -D src/pandoc_preprocessor_syllabus_dates.py /usr/local/bin/pandoc_preprocessor_syllabus_dates.py
	install -D src/pandoc_preprocessor_insert_lines.py /usr/local/bin/pandoc_preprocessor_insert_lines.py
	install -D src/pandoc_preprocessor_question_orders.py /usr/local/bin/pandoc_preprocessor_question_orders.py
	ln -s /usr/local/bin/pandoc_preprocessor_criticmarkup.py /usr/local/bin/pandoc_preprocessor_criticmarkup
	ln -s /usr/local/bin/pandoc_preprocessor_macros.py /usr/local/bin/pandoc_preprocessor_macros
	ln -s /usr/local/bin/pandoc_preprocessor_syllabus_dates.py /usr/local/bin/pandoc_preprocessor_syllabus_dates
	ln -s /usr/local/bin/pandoc_preprocessor_insert_lines.py /usr/local/bin/pandoc_preprocessor_insert_lines
	ln -s /usr/local/bin/pandoc_preprocessor_question_orders.py /usr/local/bin/pandoc_preprocessor_question_orders

uninstall:
	-rm /usr/local/bin/pandoc_preprocessor_criticmarkup
	-rm /usr/local/bin/pandoc_preprocessor_macros
	-rm /usr/local/bin/pandoc_preprocessor_syllabus_dates
	-rm /usr/local/bin/pandoc_preprocessor_insert_lines
	-rm /usr/local/bin/pandoc_preprocessor_question_orders
	-rm /usr/local/bin/pandoc_preprocessor_criticmarkup.py
	-rm /usr/local/bin/pandoc_preprocessor_macros.py
	-rm /usr/local/bin/pandoc_preprocessor_syllabus_dates.py
	-rm /usr/local/bin/pandoc_preprocessor_insert_lines.py
	-rm /usr/local/bin/pandoc_preprocessor_question_orders.py
