This contains the data from the (WikiQA effort)[https://aclweb.org/anthology/D15-1237], and the matching of WikiQA answer sentences to (Concretely Annotated Wikipedia (CAW))[https://archive.data.jhu.edu/dataset.xhtml?persistentId=doi:10.7281/T1/D06YVM].

WikiQA
------

WikiQA/WikiQA-{train|dev|test}.tsv(.gz) : the train, dev, test split

WikiQA/LICENSE.pdf is the original license file from Microsoft for the WikiQA data, which is included here in accordance to that license.  At the time of this writing, the original WikiQA dataset in its entirety could be found at:

(https://www.microsoft.com/en-us/download/details.aspx?id=52419)[https://www.microsoft.com/en-us/download/details.aspx?id=52419]


WikiQA-match
------------

WikiQA-match/{train|dev|test}-match.tsv -- each corresponding to the specific portion of the WikiQA dataset, where the column format is:

```
<WikiQA Sentence ID>    <CAW Article Title> <CAW Article Title:Section Number:Sentence Number>  <Sentence UUID> <Label>
```

This data results from:

```
@InProceedings{chen-vandurme:2017:EACLshort,
  author    = {Chen, Tongfei  and  {Van Durme}, Benjamin},
  title     = {Discriminative Information Retrieval for Question Answering Sentence Selection},
  booktitle = {Proceedings of the 15th Conference of the European Chapter of the Association for Computational Linguistics: Volume 2, Short Papers},
  month     = {April},
  year      = {2017},
  address   = {Valencia, Spain},
  publisher = {Association for Computational Linguistics},
  pages     = {719--725},
  url       = {http://www.aclweb.org/anthology/E17-2114}
}
```