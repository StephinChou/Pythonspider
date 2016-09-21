<?php 

$link = mysqli_connect('localhost:3306', 'root', '');
mysqli_select_db($link,'test');

$result = mysqli_query($link,"select * from `bili_online` order by `ctime`");

$data = array();
while($row = mysqli_fetch_array($result))
{
	//js插件默认是标准时间 ，我们给他 + 8个小时
	$tmp = array(intval($row['ctime'])*1000 + 8*3600000,intval($row['online']));
	$data[] = $tmp;
}
$callback = $_GET['callback'] ? $_GET['callback'] :"callback";

echo "{$callback}(".json_encode($data).")";