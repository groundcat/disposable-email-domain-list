<?php

// Retrieve full domain list from sources
$listA = file_get_contents('https://raw.githubusercontent.com/ivolo/disposable-email-domains/master/index.json');
$listB = file_get_contents('https://raw.githubusercontent.com/ivolo/disposable-email-domains/master/wildcard.json');
$listC = file_get_contents('https://gist.githubusercontent.com/michenriksen/8710649/raw/e09ee253960ec1ff0add4f92b62616ebbe24ab87/disposable-email-provider-domains');
$list = $listA . $listB . $listC;

// Clean format
$list = str_replace(array(',', '"', '[', ']', ' '), '' , $list);

// Explode
$list = explode("\n", $list);

// Remove duplicates
$list = array_unique($list);

// Sort
usort($list, "strcasecmp");

// Implode
$list = implode("\n",$list);

// Remove empty lines
$list = preg_replace("/(^[\r\n]*|[\r\n]+)[\s\t]*[\r\n]+/", "\n", $list);

// Overwrite all unvalidated domains to data/all-domains.txt
file_put_contents('domains-unvalidated.txt', $list);

// Empty domains.txt
file_put_contents('domains.txt', "");

// Validate domains

function mxrecordValidate($domain) {
    $arr = dns_get_record($domain, DNS_MX);
    if ($arr[0]['host'] == $domain && !empty($arr[0]['target'])) {
        return $arr[0]['target'];
    }
}

$file = fopen("domains-unvalidated.txt", "r");
$i=0;

while(! feof($file))
{
    $domain = fgets($file); // Read one line
    $domain = str_replace(array("\n", "\r"), '', $domain);

    if (mxrecordValidate($domain)) {
        // This MX records exists. Valid Email Domain.
        $outputline = $domain."\n";
    } else {
        // No MX record exists. Invalid Email Domain.
        $outputline ="";
    }
    echo $outputline;
    $outputfile="domains.txt";
    $handle=fopen($outputfile,"a+");

    $str=fwrite($handle, $outputline);
    fclose($handle);

    $i++;

}

fclose($file);

// Delete domains-unvalidated.txt
unlink('domains-unvalidated.txt');

// Convert domains.txt into domains.json

header('Content-type: application/json');
$fp    = 'domains.txt';
// get the contents of file in array
$conents_arr   = file($fp,FILE_IGNORE_NEW_LINES);
foreach($conents_arr as $key=>$value)
{
    $conents_arr[$key]  = rtrim($value, "\r");
}
var_dump($conents_arr);
$json_contents = json_encode($conents_arr);
// echo $json_contents;
file_put_contents('domains.json', $json_contents);

?>