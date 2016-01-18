# Writeup for fridginator

> Solves: 52
> 
> Fridginator 10k - Web/Crypto - 200 pts - realized by clZ
  My brother John just bought this high-tech fridge which is all flashy and stuff, but has also added some kind of security mechanism which means I can't steal his food anymore... I'm not sure I can survive much longer without his amazing yoghurts. Can you find a way to steal them for me?
  [The fridge is here](http://fridge.insomnihack.ch/)

### ENG

### PL
Strona zawierała dwa formularze, jeden do rejestracji, drugi do logowania:

![Screenshot_1.png](Screenshot_1.png)![Screenshot_2.png](Screenshot_2.png)

Po utworzeniu konta i zalogowaniu, pokazywał się następujący widok:

![Screenshot_3.png](Screenshot_3.png)

Przy próbie wyszukania jogurtu Johna i wzięcia go z lodówki, niestety dostawaliśmy informację, że nie jesteśmy uprawnienie do zabrania jego rzeczy.

![Screenshot_4.png](Screenshot_4.png)
![Screenshot_5.png](Screenshot_5.png)

Każda próba wyszukiwania przenosiła nas na podstronę o url, przykładowo taki:
`http://fridge.insomnihack.ch/search/67d4b8f78c33d07cbdc7293b9cd93b8f37231e5001982893f5c3a6494d14bbba/`

Stwierdziliśmy, że to czego wyszukujemy jest kodowane, następnie przeniesieni zostajemy na podstronę z wygenerowanym w url zakodowanym zapytaniem. Musi tam więc nastąpić dekodowanie hasha z url, a następnie wyszukiwanie na podstawie zdekodowanych wartości.

Po kilku próbach wysyłania zapytań, ustaliliśmy, że na jeden 32 znakowy hash, składa się maksymalnie 16 znaków. A także, że kodowanie wygląda następująco.
[przedrostek][nasze zapytanie][przyrostek]. Ustaliliśmy również, że [przedrostek] składa się z 7 znaków. A [przyrostek], zależnie od tego czy wyszukujemy użytkowników, czy produktów, z 11 lub 13 znaków. [przedrostek] wyglądał nam od razu na wartość `search=` sprawdziliśmy i zgadzało się. [przyrostek] musiał posiadać informację w jakiej tabeli następuje wyszukiwanie. Napisalismy mały półautomatyczny skrypt [brute.py](brute.py), który pomógł nam litera po literze poznać wartość przyrostka, dla produktów wyglądał następująco `|type=object%01` (%01 to oczywiście 1 znak Start of Heading po zdekodowaniu).

Pozostało nam więc zapełnić 1. blok znaków do 16 liter, czyli pamiętając, że 7 znaków pochłonie `search=` przesłać 9 dowolnych znaków. Następnie przesłać nasz kod, który chcemy wykonać, który musiał mieć długość równą wielokrotności liczby 16, aby nie pomieszać się z przyrostkiem.



* Filename (name for created file)
* Content (content for created file, with limit to 7 chars only)

Looking into source reveals:
```html
    <!DOCTYPE html>
    <!--[if lt IE 7]> <html class="lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
    <!--[if IE 7]> <html class="lt-ie9 lt-ie8" lang="en"> <![endif]-->
    <!--[if IE 8]> <html class="lt-ie9" lang="en"> <![endif]-->
    <!--[if gt IE 8]><!-->
    <html lang="en"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>TinyHosting</title>
        <link rel="stylesheet" href="css/style.css">
        <!--[if lt IE 9]><script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    </head>
    <body>
    <!-- <a href="./?src=">src</a>-->
    <form method="post" action="" class="login">
        <p>
            <label for="login">Filename:</label>
            <input type="text" name="filename" >
        </p>
        <p>
            <label for="password">Content:</label>
            <input type="text" name="content" maxlength="7">
        </p>
        <p class="login-submit">
            <button type="submit" class="login-button">Create!</button>
        </p>
            </form>

    </body>
    </html>
```

We saw that one line is commented, so we tried to use `get` parameter with `src` name. Url looked like `http://136.243.194.53/?src=anything`. When we looked at the new source, we had PHP code as well.

```php
<?php
$savepath="files/".sha1($_SERVER['REMOTE_ADDR'].$_SERVER['HTTP_USER_AGENT'])."/";
if(!is_dir($savepath)){
    $oldmask = umask(0);
    mkdir($savepath, 0777);
    umask($oldmask);
    touch($savepath."/index.html");
}
if((@$_POST['filename']) && (@$_POST['content']) ){
    $fp = fopen("$savepath".$_POST['filename'], 'w');
    fwrite($fp, substr($_POST['content'],0,7) );
    fclose($fp);
    $msg = 'File saved to <a>'.$savepath.htmlspecialchars($_POST['filename'])."</a>";
}
?>
    <!DOCTYPE html>
    <!--[if lt IE 7]> <html class="lt-ie9 lt-ie8 lt-ie7" lang="en"> <![endif]-->
    <!--[if IE 7]> <html class="lt-ie9 lt-ie8" lang="en"> <![endif]-->
    <!--[if IE 8]> <html class="lt-ie9" lang="en"> <![endif]-->
    <!--[if gt IE 8]><!-->
    <html lang="en"> <!--<![endif]-->
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title>TinyHosting</title>
        <link rel="stylesheet" href="css/style.css">
        <!--[if lt IE 9]><script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script><![endif]-->
    </head>
    <body>
    <!-- <a href="./?src=">src</a>-->
    <form method="post" action="" class="login">
        <p>
            <label for="login">Filename:</label>
            <input type="text" name="filename" >
        </p>
        <p>
            <label for="password">Content:</label>
            <input type="text" name="content" maxlength="7">
        </p>
        <p class="login-submit">
            <button type="submit" class="login-button">Create!</button>
        </p>
        <?php if(@$msg) echo $msg;?>
    </form>

    </body>
    </html>

<?php if(@$_GET['src']) show_source("index.php");?>
```

Quick analysis of the script and used functions gave us these conclusions:

* We can save the file with any name and extension
* File really can contain only 7 bytes (`substr` is safe function)
* We cannot append content to existing file, because `fwrite` with `w` option saves content always from the first byte

We concluded that the only way to do anything useful is to create an executable file, which will have at most
7 bytes of content. 

First we checked whether PHP files are executed. We submitted a new file:

* filename: `x.php`
* content: `<?=a?>` (`<?=` is a shorthand for `<?php echo`)

After submit, script returns a link to our created link, like:

`http://136.243.194.53/files/27725b3e4b3edf013480032fe2b318ffff4d04c7/x.php`

File printed only `a` without PHP tags, so we knew that the files are interpreted. Next step was to see if we can
call the server console command. So we can create this content ``<?=`w`;`` (`w` is the shortest shell command, showing
who is logged in and what they are doing, while backticks are short for `shell_exec()`).

Result:

`18:27:23 up 1:28, 1 user, load average: 0.08, 0.04, 0.05 USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT root pts/0 197.0.75.43 16:59 1:27m 0.02s 0.02s`

So we can create interpreted PHP files and we can use server command, but are limited to 7 bytes, with 6 bytes being
reserved for PHP boilerplate. Thus, we have only 1 character for command. We found we can use `*`, which if called,
executes command made of concatenation of filenames in current directory in alphabetical order. From the script we knew that folder always contained file `index.html`, so we can use only commands lexicographically smaller than `index.html`. 

So we created new PHP file:

* filename: `x.php`
* content: ``<?=`*`;``

Next we created this file:

* filename: `bash`
* content: `anythin`

and this one:

* filename: `c.sh`
* content: `ls -R /` (this command lists all files recursively starting with `/`)

Result was as though we executed `bash c.sh`:

`/bin /dev /file_you_want ... a lot of files`

We noticed file `/file_you_want` so we replaced command `ls -R /` with `cat /f*` by submitting file:

* filename: `c.sh`
* content: `cat /f*`

and finally we had the flag from content of file `/file_you_want`.
