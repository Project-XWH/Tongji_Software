![](https://github.com/igemsoftware2019/Tongji_Software/blob/master/media/img/Pathlab-black.png)
<br>
# <a href="https://2019.igem.org/Team:Tongji_Software"> Tongji_Software </a>
Here is Pathlab, as the name show, a pathway laboratory. Pathlab is a web software, you will fun with the convient use. You can use it online, the address is <a href="www.pathlab.top">`www.pathlab.top`</a>.

## Functions
### 1. Pathway Search
We provide the function of pathway search in the databse by `orignial search` and `novel search`, which mean that you can get more possible about waht you want to do. 
### 2. Enzyme Selection
You can also do the `enzyme selection` after pathway serach or select enzyme for just one reaction.
### 3. Parts Browser
This is a browser tool for you to search parts you need existed in the <a href="igem.org">`iGEM`</a> parts database.

## Requirements
If you want to use our tool locally, you should pay attention to theses requirements:<br>
* `Python >= 3.5`
* `Django >= 1.10.6`
* `rdkit` : a collection of cheminformatics software, used for SMILES calculation
* `sklearn` : a simple and effective tools for data mining and analysis, used for random forest

## Download and Use

* download source data
```Shell
 $ git clone https://github.com/igemsoftware2019/Tongji_Software.git
```
* start up the server
```Shell
 $ cd $PATH_Download/Pathlab
 
 $ python manage.py runserver 
```
![](https://github.com/igemsoftware2019/Tongji_Software/blob/master/media/img/django.png)

Enter `http://127.0.0.1:8000/` in the browser (`chrom` is better), and use our tool locally.

## Advance Information
To know more about Pathlab, you can come to iGEM <a href="https://2019.igem.org/Team:Tongji_Software">`wiki`</a> page. What's more, here is a demonstration <a href="https://2019.igem.org/Team:Tongji_Software/Project#Demonstrate">`viedo`</a> which can be a user guid for you to use Pathlab.

## Contact Us
If you have any advice for us, you can send your suggestion to 1194189468@qq.com.

