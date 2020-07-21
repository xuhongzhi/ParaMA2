# ParaMA2
An supervised morphological analyzer based on language typological information. ParaMA2 is an improved version of [ParaMA](https://github.com/xuhongzhi/ParaMA).

## Description
This is an unsupervised tool for analyzing suffixation morphology for any languages given a list of words. The details of the algorithm can be found in the following paper:

Hongzhi Xu, Jordan Kodner, Mitch Marcus, Charles Yang. 2020. Unsupervised Learning of Language Morphology by Exploring Language Typology. In *Proceedings of the 58th Annual Conference of Association for Computational Linguistics (ACL)*. pages 6672–6681. 

## Segment a word list
Use the following command to segment a word list (each line: \<word\> \<freq\>), and save it to a file. 
```
python3 main.py my_data.txt -o my_data_seg.txt
```

If you have a training word list and a test word list, you can use the following.
```
python3 main.py training_data.txt -o training_seg.txt -ti test_data.txt -to test_seg.txt
```

You can check ***main.py*** for more details.

The output also gives the derivational chain information. For example, the word _sterilizing_ is derivated by sterilize, deleting _e_ and plus _-ing_, which is then derived from _sterile_, deleting _e_ and plus _-ize_. The line will be like the following except that there will be no brackets.

sterilizing \<\t\> steril iz ing \<\t\> (sterile X $) (sterile X_\<ize\> del:e:r) (steril__ize X_\<ing\> del:e:r)
