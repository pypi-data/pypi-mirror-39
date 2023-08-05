
dmethylation
-----------

Dmethylation is a Django app to store the Illumina methylation data. It can be used for Illumina Infinium 
HumanMethylation450 BeadChip and Infinium MethylationEPIC BeadChip 

Quick start
-----------

1. Add "dgenome" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dgenome',
        'dmethylation',
    ]

2. Include the dgenome URLconf in your project urls.py like this::

    url(r'^dmethylation/', include((dmethylation.urls, 'dmethylation'), namespace='dmethylation')),

3. Run `python manage.py makemigrations dgenome` to create the dgenome tables.

4. Run `python manage.py makemigrations dmethylation` to create the dmethylation tables.

5. Run `python manage.py migrate` to create the dmethylation models.

6. Insert the Illiumina HumanMethylation450 or MethylationEPIC CSV file with the 
script: bin/load_annotation_HumanMethylation450.py

7. See available API endpoints:

   /dmethylation/api/

