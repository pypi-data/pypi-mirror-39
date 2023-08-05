DIR=$1
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"/..

mkdir $DIR/data

curl https://files.pythonhosted.org/packages/6f/ed/9c755d357d33bc1931e157f537721efb5b88d2c583fe593cc09603076cc3/nltk-3.4.zip > $DIR/data/nltk-3.4.zip
unzip $DIR/data/nltk-3.4.zip -d $DIR/data/
mv $DIR/data/nltk-3.4/nltk/ $DIR/
rm -r $DIR/data/nltk-3.4/
rm $DIR/data/nltk-3.4.zip

curl https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo > $DIR/data/hp.obo
python $DIR/hpo_syns.py $DIR/data/hp.obo > $DIR/data/tmp
python $DIR/standardize_syn_map.py $DIR/data/tmp > $DIR/data/hpo_synonyms.txt
rm $DIR/data/tmp
python $DIR/hpo_names.py $DIR/data/hp.obo > $DIR/data/hpo_term_names.txt 

#cat $DIR/data/hpo_synonyms.txt | cut -f1 | grep -vf $DIR/data/common_phenotypes.txt | sort -u > $DIR/data/rare_phenotypes.txt
