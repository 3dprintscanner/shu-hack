for f in *.pdf
do
    pdf2txt.py ${f} > ${f}.txt
done
