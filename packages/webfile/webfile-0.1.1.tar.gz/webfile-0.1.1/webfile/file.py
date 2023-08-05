$def with (body,dirname)
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /$dirname/</title>
</head>

<script>
    function change(){  
        document.getElementById("file_name").value=document.getElementById("file_content").value;  
    }  
</script>



<body>


<h1>Directory listing for /$dirname/</h1>

<hr>

<form method="post"  enctype="multipart/form-data">
    <div class="col-sm-4">  

        <input type="file" class="form-control" id="file_content" name="file_content"  
               style="display: none;" onchange="change();">  
        <input type="text" class="form-control" id="file_name" name="file_name"  
               readonly="readonly" onclick="file_content.click(); ">  
        <button type="button" class="btn btn-primary" id="select_file"  
                onclick="file_content.click();">Scan file  
        </button>  
        <input type="submit" value="Submit file" />

    </div>  
    
</form>
</hr>
<hr>
<form method="post"  enctype="multipart/form-data">
    <div class="col-sm-4">  
        <input type="submit" value="Download files" /></br>
        $for i,j in body:
            <label><input name="$i" type="checkbox" value=""/><a href="$i">$j</a></label> </br>
    </div>  
    
</form>

</hr>
</body>
</html>
