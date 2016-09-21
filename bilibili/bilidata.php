<?php 

$link = mysqli_connect('localhost:3306', 'root', '');
mysqli_select_db($link,'test');
mysqli_set_charset($link,'utf8');
$limit = $_GET['limit'] ? $_GET['limit'] : 15;//up数量
$by = $order = $_GET['order'] ? $_GET['order'] : 'play';//排序字段
$average = $_GET['average'];
$fields = array("play"=>"播放量","coin"=>"硬币数","collect"=>"收藏数","danmu"=>"弹幕数");
if(!isset($fields[$order])){
	echo 0;
	die;
}
if($average){
	$by = 'avg'.$order;
}
$sql = "SELECT author_name,count('*') as 'avNum', AVG(`{$order}`) as avg{$order},sum(`{$order}`) as {$order} FROM `bilibili` group by author order by {$order} DESC limit {$limit}";


$result = mysqli_query($link,$sql);
file_put_contents("a.txt", $sql);

$data['name'] = $average ? "平均每视频".$fields[$order] :$fields[$order];
while($row = mysqli_fetch_array($result))
{
	if($average){
		$num = intval($row['avg'.$order]);
	}else{
		$num = intval($row[$order]);
	}
	$sort[] = $num;
	$tmp = array($row['author_name'],$num);
	$data['data'][] = $tmp;
}

array_multisort($data['data'],SORT_ASC ,SORT_NUMERIC ,$sort);
$callback = $_GET['callback'] ? $_GET['callback'] :"callback";

echo "{$callback}(".json_encode($data).")";