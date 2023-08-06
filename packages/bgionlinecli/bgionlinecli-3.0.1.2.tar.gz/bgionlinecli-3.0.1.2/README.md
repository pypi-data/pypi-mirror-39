bgionline-cli
=======
bgionline 数据交付工具

## 安装

```bash
线上环境
pip install bgionlinecli 
```

```bash
开发环境
pip install -e ./
使用
bo login --host 112.74.38.235
登录
```

## 运行环境
```
Python (requires Python 2.7)
```

## 概要

- 登入功能

    ```bash
    bo login
           Username:
           Password:
    usage: bo login [-h] [--token TOKEN] [--noprojects]
    optional arguments:
        -h, --help     show this help message and exit
        --token TOKEN  Authentication token to use
        --noprojects   Do not select available projects
    ```
- 退出功能
    ```bash
    bo logout
    ```
- 新建功能
 - 新建用户
         ```bash
         
        bo new user username
        usage: bo new user [-h] [--password PASSWORD] [--email EMAIL] name
        optional arguments:
            -h, --help           show this help message and exit
            --password PASSWORD  password for new user, default=<random generated>
            --email EMAIL        email address of new user, default=<random generated>
       
         ```
 - 新建项目
        ```
        
        bo new project  projectname
        usage: bo new project [-h] [--desc DESC] [-s] name
        optional arguments:
            -h, --help    show this help message and exit
            --desc DESC   description of the new project
            -s, --select  choose this new created as working project
        ```
- 选择项目功能
 - 列表选择
        ```bash 
        
        bo select
        Available projects:
        ---------------------------------------------------------------
          index                project id                project name
        ---------------------------------------------------------------
            0     1c06c29e-e4e9-4a19-9ce3-ab71544dd883        A
            1     72dd9e43-0022-41db-a50a-d3b9382b5c0e        B
        ---------------------------------------------------------------
        Pick a numbered choice [5]:  index
        
        ```
 - 直接选择
        ```bash
        
            bo select  project
            usage: bo select [-h] [project]
            positional arguments:
            project     Name or ID of a project to switch to; if not provided a list
                        will be provided for you
        ```
- 获取当前目录功能
    ```bash
    bo pwd
    ```
- 树形文件显示功能
    ```bash
    bo tree
    usage: bo tree [-h] [--id] [-f] [path]
    List folders and objects in a tree
    positional arguments:
      path          Folder (possibly in another project) to list the contents of,
                    default is the current directory in the current project.
                    Syntax: projectID:/folder/path
    
    optional arguments:
      -h, --help    show this help message and exit
      --id          show file ID
      -f, --folder  Show only the folder
    ```
- 显示文件功能
    ```bash
    bo ls
    usage: bo ls [-h] [-f] [--id] [path]
    positional arguments:
        path        Folder (possibly in another project) to list the contents of,
                    default is the current directory in the current project. Syntax:
                    projectID:/folder/path

    optional arguments:
        -h, --help  show this help message and exit
        --folders   show only folders
        --id        show file ID
    ```
- 切换项目路径功能
    ```bash
    bo cd path
    usage: bo cd [-h] path
    positional arguments:                                                         
        path      Folder (possibly in another project) to which to change the     
                  current working directory)
    ```
- 创建新文件夹功能
    ```bash
    bo mkdir path
    usage: bo mkdir [-h] [-p] path
    positional arguments:
        path           Paths to folders to create
        
    optional arguments:
        -h, --help     show this help message and exit
        -p, --parents  no error if existing, create parent directories as needed
    ```
- 删除文件及文件夹功能
    ```bash
    bo rm -i Id or path
    usage: bo rm [-h] [-i ID] [path]
    positional arguments:
        path          Remove file or directory by path,path end with "/" means
                      download directory, and path end without "/" means download
                      file
        
    optional arguments:
        -h, --help      show this help message and exit
        -i ID, --id ID  Remove file or directory ID
    ```
- 移动文件及文件夹功能
    ```
    bo mv
    usage: bo mv [-h] source destination
    positional arguments:
    path                    download file or directory by path,path end with "/"
                            means download directory, and path end without "/"
                            means download file(default uses current BGIonline
                            project and folder if not provided)
    
    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            Local filename or directory to be used ("-" indicates
                            stdout output); if not supplied or a directory is
                            given, the object's name on the platform will be used,
                            along with any applicable extensions
      -f, --force           Force to download, never prompt
      -t TYPE, --type TYPE  Download File type
      --concurrent CONCURRENT
                            The number of concurrent tasks, the default is 1, the
                            maximum is 20
    ```
- 上传文件功能
    ```bash
    bo upload localPath
    usage: bo upload [-h] [--concurrent CONCURRENT] [-m METADATA] [--path PATH] filename
    positional arguments:
        filename              Local file or directory to upload

    optional arguments:
        -h, --help            show this help message and exit
        --concurrent CONCURRENT
                        The number of concurrent tasks, the default is 5, the
                        maximum is 20
        -m METADATA, --metadata METADATA
                        key1=value1 ,Meta data to be associated (can have
                        multiple -m options)
        --path PATH  
                        BGIonline path to upload file(s) to (default uses
                        current project and folder if not provided)
    ```
- 下载文件功能
    ```
    bo download
    usage: bo download [-h] [-o OUTPUT] [-f] [-t TYPE] [--concurrent CONCURRENT] [path]
    positional arguments:
    path                download file or directory by path,path end with "/"
                        means download directory, and path end without "/"
                        means download file(default uses current BGIonline
                        project and folder if not provided)
    
    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                        Local filename or directory to be used ("-" indicates
                        stdout output); if not supplied or a directory is
                        given, the object's name on the platform will be used,
                        along with any applicable extensions
    -f, --force         Force to download, never prompt
    -t TYPE, --type TYPE  Download File type
    --concurrent CONCURRENT
                        The number of concurrent tasks, the default is 1, the
                        maximum is 20
    ```
- 转移项目功能
    ```
    bo transfer username
    usage: bo transfer [-h] [-p PROJECT] [--remain] username
    positional arguments:
    username              Accept the username
    
    optional arguments:
    -h, --help            show this help message and exit
    -p PROJECT, --project PROJECT
                        Need transfer project ID,default uses current
                        BGIonline project if not provided
    --remain            Remain in your project
    
    bo transfer: error: too few arguments
    ```
- 查找功能
    ```
    bo find
    usage: bo find [-h] [--path PATH] [-m METADATA] [--name NAME]
    Print current working directory
    optional arguments:
      -h, --help            show this help message and exit
      --path PATH           Folder in which to restrict the resultsdefault is "/"
                            in the current project
      -m METADATA, --metadata METADATA
                            Key-value pair of a metadata or simply a metadata key;
                            if only a key is metadata, matches a result that has
                            the key with any value; repeat as necessary, e.g. "--
                            metadata key1=val1 --metadata key2
      --name NAME           Name of the object
    
    ```