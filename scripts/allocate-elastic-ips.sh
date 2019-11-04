for i in {0..33}
do
 string=`aws ec2 allocate-address | grep AllocationId | awk 'BEGIN { FS=":" } /1/ { print $2 }' | sed 's/\"//g' | sed 's/\,//' | sed 's/\\s//g' | sed -e "s/ //g"`
 echo $string
done
