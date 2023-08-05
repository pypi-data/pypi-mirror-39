# jingyun

## 0.5.4
jy-jingd-usermod 支持新建账户

## 0.5.2
jy-jingd-reanalysis 当seq_files和流程中定义的不一致时打印出来

## 0.5.1
add jy-jingd-reanalysis

## 0.4.7
fix jy-server-port exit code

## 0.4.6
jy-server-port -s 增加可选项registry port[5000-5010]

## 0.4.5
add jy-server-ip

## 0.4.3
add jy-server-port

## 0.4.2
add jy-sql-link

## 0.4.1
add jy-sql-table 支持新建视图等，-f 支持后面跟多个参数，支持--file-prefix

## 0.3.9
fix bug jy-jingd-usermod -a

## 0.3.8
add jy-sql-table

## 0.3.6
jy-oss-download  添加参数 --allow-custom

## 0.3.5
fix jy-docker-compose bug

## 0.3.4
fix jy-docker-compose bug

## 0.3.3
jy-docker-compose

## 0.2.9
jy-supervisord jy-supervisorctl 执行前，先进行source .bash_profile

## 0.2.8
jy-oss-download 添加参数 -f --force 无论要下载的文件是否已存在，都进行下载

## 0.2.7
jy-oss-download 添加参数 -n --name  下载后保存的文件名，仅在下载文件只有一个时有效，超过一个下载文件将忽略该参数

## 0.2.6
jy-oss-download下载时如果文件存在将不进行下载

## 0.2.5
jy-supervisord
jy-supervisorctl

## 0.2.2
add jy-jingd-usermod
udpate jy-conf-read 添加参数 -i --ignore

## 0.2.1
add jy-conf-read

## 0.1.10
add jy-ssh-nonkey

## 0.1.9
jy-conf-format 支持遍历和筛选整个目录下的文件

## 0.1.8
jy-conf-format add mode params

## 0.1.7
add jy-conf-format

## 0.1.6
jy-key add --only-value 只打印密钥要打印的密钥中的属性值，不打印属性

## 0.1.5
fix not include jingyun_cli/key

## 0.1.4
key cli 上线 jy-key

## 0.1.3
oss cli 上线 jy-oss-download

## 0.1
json cli 上线 json-merge